#!/usr/bin/env python3

import subprocess
import re
import pandas as pd
import argparse
import pathlib
import pprint
import itertools
from functools import reduce

###
# HELPERS
###
def get_catlongname(cat):

        ''' Return a long name (if known) for a given category. '''
        knowncats = {'bio':"Biology", 'cae':"CFD/Finite element modelling",
                     'chem':"Chemistry", 'compiler':"Compilers", 'data':"Data processing",
                     'debugger':"Debugging", 'devel':"Development", 'geo':"Weather modelling", 
                     'lang': "Programming Languages", 'lib':"Libraries",  'math':"Mathematics",
                     'mpi': "MPI", 'numlib':"Numerical libraries", 'perf':"Performance measurements",
                     'phys':"Physics", 'system':"System-level software", 'toolchain':"Toolchains (software stacks)",
                     'tools':"Utilities", 'vis':"Visualisation"}
        if cat is None: return knowncats
        if cat in knowncats.keys(): return knowncats[cat]
        else: return cat.upper()

# Deep Dictionary Merge from https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
def dict_merge(dct, merge_dct):

    dct = dct.copy()

    for k, v in merge_dct.items():
        if (k in dct and isinstance(dct[k], dict) and isinstance(merge_dct[k], dict)):
            dct[k] = dict_merge(dct[k], merge_dct[k])
        else:
            if (bool(dct) and k in dct.keys() and isinstance(dct[k], list)):
                dct[k] = list(set(dct[k] + merge_dct[k]))
            else:
                dct[k] = merge_dct[k]

    return dct

# Deep dictionary searching with filters
def dict_contains(dct, fkey, fvalue):

    for k, v in dct.items():
        if k == fkey:
            # Simple check if the key is present (no value comparison)
            if fvalue is None:
                return True
            # Check presence of the value in the corresponding list
            if isinstance(v, list):
                if v[0] in fvalue:
                    return True
            # Check if the value is a key
            if isinstance(v, dict):
                if list(v.keys())[0] in fvalue:
                    return True
            if v == fvalue:
                return True

        # We continue to dig into the dictionary if we can continue to go down
        if isinstance(v, dict):
            if dict_contains(v, fkey, fvalue):
                return True

    return False

# Create and return the created path/folder object
def create_output_path(path):
    folder = pathlib.Path(path)
    if not folder.exists():
        folder.mkdir(parents=True)
    return folder

###
# Get module information based on its LUA filepath
# Return module dictionary with description, category, ... if succesfully retrieved
# Return False is failed
###
def get_module_details_from_file(mfpath, filters):

    try:

        if "/opt/apps/resif/" not in mfpath:
            raise Exception('File provided does not come from /opt/apps/resif')
        
        path_splitted = mfpath.split('/')
        path_splitted.pop(0)

        if path_splitted[-1].split('.')[-1] != 'lua':
            raise Exception('File provided does not have the LUA extension')

        # Read provided file
        f = open(mfpath, 'r')
        raw = f.readlines()
        f.close()

        # Get information from filepath
        category_name = path_splitted[8].lower()
        software_name = path_splitted[9]
        cluster = path_splitted[3]
        arch = path_splitted[5]
        swset = path_splitted[4]

        # Parse the file to retrieve description and www page
        # The description is split between many lines, get them in a list
        desc = []
        version = ""
        isDescLine = False
        for line in raw:
            line = line.strip()
            if line.startswith("whatis([[Description:") or line.startswith("whatis([==[Description:"): isDescLine = True
            if line.startswith("whatis([[Homepage:") or line.startswith("whatis([==[Homepage:"): 
                isDescLine = False    # description ends before www whatis block
                match_homepage = line
            if isDescLine and (line != ''): desc.append(line)
            if line.startswith("setenv(\"EBVERSION"):
                version = re.search('setenv\("EBVERSION.*", "(.+)\"\)', line).group(1)

        desc[0] = desc[0].replace('whatis([[Description: ',"").replace('whatis([==[Description: ',"").replace('whatis([==[Description:',"")
        desc[-1] = desc[-1].replace(']])','').replace(']==])','')
        full_desc = (" ".join(filter(None, desc)))

        www = match_homepage.replace('whatis([[Homepage: ',"").replace('whatis([==[Homepage: ',"").replace(']])',"").replace(']==])',"")

        module_details = {
            category_name: {
                software_name: {
                    "www": www,
                    "desc": full_desc,
                    "versions": {
                        version: {
                            "swsets": {
                                swset: {
                                    "clusters": [cluster],
                                    "archs": [arch],
                                }
                            }
                        }
                    }
                }
            }
        }

        # Excluding the result if the module does not correspond to filters
        for filter_key, filter_value in filters.items():
            if not dict_contains(module_details, filter_key, filter_value):
                return False

        return module_details
    
    except Exception as e:
        print(e)
        return False

###
# Iterate and deepmerge over list of module filepath to generate a map
###
def collect_softwares(paths, filters=None):

    collected_softwares = {}

    for filepath in paths:
        module_details = get_module_details_from_file(filepath.rstrip(), filters)
        # If the module is found and corresponds to filters we gave, then we add it to the returned map
        if module_details:
            collected_softwares = dict_merge(collected_softwares, module_details)

    return collected_softwares


###
# Write into markdown files software details, usaully given by the collect command
# /all_software.md will contains generic informations, 1 line per software
# /swset.md will contains all software and version included into the current software set (can contain multiple line for a single software, but with different versions)
# /category/software.md contains all versions and software set available for this specific software
###
def render_markdown_from_collect(collected_softwares, output_path="./software_list"):

    output_folder = create_output_path(output_path)
    all_softwares={}
    category={}
    softwares_swset={}

    for category_name, category_softwares in collected_softwares.items():
        category_folder = create_output_path(output_folder / category_name)

        for software_name,  software_details in category_softwares.items():
            software_file = category_folder / (software_name + ".md")

            # Flattening software details so we can easily parse and retrieve data from the nested dict
            # Using '|' as separator as other caracters such as '_', '-' or '.' can be used in a version label
            software_details_flatten = pd.json_normalize(software_details, sep='|').to_dict(orient='records')[0]

            # Append website to software name in a markdown manner for later use (table indexing)
            software_key = "[{1}]({0})".format(software_details['www'] if software_details['www'] else '#', software_name)

            # Retrieve generic information of a software (all_software.md) formatted to be usable in a DataFrame
            software_without_details = {
                software_key: []
            }

            # Getting versions, swsets, archs, clusters, long category name and description
            available_versions = software_details["versions"].keys()
            software_without_details[software_key].append(', '.join(available_versions)) # Versions

            software_without_details[software_key].append(
                ', '.join(
                    pd.unique(
                        list(map(
                                lambda x: x.split('|')[3],
                                filter(
                                    lambda key: bool(re.search('versions\|.+\|swsets\|.+', key)),
                                    software_details_flatten.keys()
                                )
                            ))
                        ).tolist()
                    )
            ) # Swets

            software_without_details[software_key].append(
                ', '.join(
                    pd.unique(
                        list(itertools.chain.from_iterable(map(
                            lambda x: x[1],
                            filter(
                                lambda item: bool(re.search('versions\|.+\|swsets\|.+\|archs', item[0])),
                                software_details_flatten.items()
                            ))))
                    ).tolist()
                )
            ) # Archs
            software_without_details[software_key].append(
                ', '.join(
                    pd.unique(
                        list(itertools.chain.from_iterable(map(
                            lambda x: x[1],
                            filter(
                                lambda item: bool(re.search('versions\|.+\|swsets\|.+\|clusters', item[0])),
                                software_details_flatten.items()
                            ))))
                    ).tolist()
                )
            ) # Clusters

            software_without_details[software_key].append(get_catlongname(category_name)) #Category
            software_without_details[software_key].append(software_details['desc']) #Description

            # Retrieve detailed information of a software (category/software.md) formatted to be usable in a DataFrame
            detailed_software_array = []
            for v in available_versions:

                # Get all swsets available for the given version
                available_swsets = pd.unique(
                    list(map(
                        lambda x: x.split('|')[3],
                        filter(
                            lambda key: bool(re.search('versions\|' + re.escape(v) + '\|swsets\|.+', key)),
                            software_details_flatten.keys()
                        )
                    ))
                ).tolist()

                for s in available_swsets:

                    # Get clusters and archs for a given (version, swset) of the current software
                    keys = list(filter(
                        lambda key: bool(re.search('versions\|' + re.escape(v) + '|swsets\|' + re.escape(s), key)),
                        software_details_flatten.keys()
                    ))
                    cluster_key = list(filter(lambda key: 'clusters' in key ,keys))[0]
                    archs_key = list(filter(lambda key: 'archs' in key ,keys))[0]

                    detailed_software_array.append([
                        v,
                        s,
                        ', '.join(software_details_flatten[archs_key]),
                        ', '.join(software_details_flatten[cluster_key])
                    ])

                    # Taking advantage of parsing all swset to add the current version of this software to the corresponding swset structure (swset.md)
                    if s not in softwares_swset:
                        softwares_swset[s] = {}
                    softwares_swset[s][software_key + ' ' + v] = [
                        ', '.join(software_details_flatten[archs_key]),
                        ', '.join(software_details_flatten[cluster_key]),
                        get_catlongname(category_name),
                        software_details['desc']
                    ]

            # Writing into category/software.md information we gathered
            df = pd.DataFrame(detailed_software_array, columns=['Version','Swset','Architectures','Clusters'])
            with software_file.open("w") as fd:
                lines = [
                    '# ' + software_key,
                    '- **Description**: ' + software_details['desc'],
                    '- **Category**: ' + get_catlongname(category_name)
                ]
                fd.write('\n'.join(lines))
                fd.write('\n')

            with software_file.open("a") as fd:
                df.to_markdown(fd)

            # Make sure we keep generic information for all_softwares.md
            all_softwares = {**all_softwares, **software_without_details}


    # Write into SWSET.md (example: 2020b.md) all included softwares information
    for swset_label, swset_list_softwares in softwares_swset.items():
        df = pd.DataFrame.from_dict(swset_list_softwares, orient="index", columns=['Architectures','Clusters','Category','Description'])
        df.index.name='Software'
        df.sort_values(by=['Software'], inplace=True)
        with (output_folder / (swset_label + ".md")).open("w") as fd:
            df.to_markdown(fd)

    # Write generic software information we gathered in all_software.md
    df = pd.DataFrame.from_dict(all_softwares, orient="index", columns=['Versions','Swsets','Architectures','Clusters','Category','Description'])
    df.index.name='Software'
    df.sort_values(by=['Software'], inplace=True)
    with (output_folder / "all_softwares.md").open("w") as fd:
        df.to_markdown(fd)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="resif3_module2markdown.py")
    subparser = parser.add_subparsers(dest='command')

    parser_collect = subparser.add_parser('collect', help='Generate a (filtered) map of ULHPC SWSet')

    parser_render = subparser.add_parser('render', help='Generate software informations files (example: ./resif3_module2markdown.py render --output $(pwd)/software_list --clusters iris --swsets 2019b 2020b --arch gpu)')
    parser_render.add_argument('--output', type=str, nargs=1, help='Secify the output folder for your generated markdown files ($(pwd)/software_list/ by default).', required=False)

    for p in [parser_collect, parser_render]:
        p.add_argument('--clusters', type=str, nargs='+', help='Filter output by cluster (example: "iris"). All clusters will be displayed by default.)', required=False)
        p.add_argument('--archs', type=str, nargs='+', help='Filter output by arch (example: "gpu"). All archs will be displayed by default.)', required=False)
        p.add_argument('--swsets', type=str, nargs='+', help='Filter output by software set (example: "2020b"). All swset will be displayed by default.)', required=False)
        p.add_argument('--paths', type=str, nargs='+', help='Path to modules\' LUA definition files, files in /opt/apps/resif/[iris,aion] are used by default', required=False)

    args = parser.parse_args()

    filters = {}
    paths = ''
    if args.paths:
        paths = args.paths
    else:
        # Get all released swset definition file if no path is specified
        paths = subprocess.check_output("""find /opt/apps/resif/iris /opt/apps/resif/aion -type d \( -iname ebfiles_repo -o -iname software \) -prune -false -o -type f \( -iname '*.lua'  ! -iname '.*' \)""", shell=True).decode('utf-8').split()
    if args.clusters:
        filters['clusters'] = args.clusters
    if args.archs:
        filters['archs'] = args.archs
    if args.swsets:
        filters['swsets'] = args.swsets

    if args.command == 'collect':
        pprint.pprint(collect_softwares(paths, filters))

    if args.command == 'render':
        output_path = './software_list'
        if args.output:
            output_path = args.output[0]
        render_markdown_from_collect(collect_softwares(paths, filters), output_path)