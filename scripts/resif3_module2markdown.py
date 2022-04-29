#!/usr/bin/env python3
# Time-stamp: <Fri 2022-04-29 22:14 svarrette>
###############################################################################

"""
Collect and analyse the current RESIF3 software set available on the ULHPC
platform -- see https://github.com/ULHPC/sw

Render (i.e.) generate output markdown files reflecting the available software
and modules to be integrated into the current hpc-docs.uni.lu site.
"""

import subprocess
import re
import pandas as pd
import click    # prefered for CLI
import confuse
import sys
import os
import logging
import logging.config
import argparse
import pathlib
import pprint
import socket
import itertools
import yaml
from functools import reduce

APPNAME = 'resif3_module2markdown'
__version__ = '1.0.0'

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
DEFAULT_SETTINGS = {
    'clusters': [
        'iris',
        'aion'
    ],
    'archs':    [
        'broadwell',
        'skylake',
        'gpu',
        'epyc'
    ],
    'swsets_versions':  [
        '2019b',
        '2020b'
    ],
    'resif_root_path': '/opt/apps/resif',
    'yamlfile':   'resif_modules.yaml',
    'output_dir': 'docs/software/swsets',
    'categories': {
        'bio':       "Biology",
        'cae':       "CFD/Finite element modelling",
        'chem':      "Chemistry",
        'compiler':  "Compilers",
        'data':      "Data processing",
        'debugger':  "Debugging",
        'devel':     "Development",
        'geo':       "Weather modelling",
        'lang':      "Programming Languages",
        'lib':       "Libraries",
        'math':      "Mathematics",
        'mpi':       "MPI",
        'numlib':    "Numerical libraries",
        'perf':      "Performance measurements",
        'phys':      "Physics",
        'system':    "System-level software",
        'toolchain': "Toolchains (software stacks)",
        'tools':     "Utilities",
        'vis':       "Visualisation"
    }
}

def dict_merge(dct, merge_dct):
    """
    Deep Dictionary Merge
    see https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
    """
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

###
# GENERIC SETTINGS / LOGS Management
###
## settings management with confuse
class ConfigValueNotFound(Exception):
    pass
confuse.NotFoundError = ConfigValueNotFound
settings = dict_merge(confuse.Configuration(APPNAME, __name__).get(),
                      DEFAULT_SETTINGS)

## logging
FORMATTER = logging.Formatter("[%(name)s] %(asctime)s — %(levelname)s: %(message)s")

def get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(FORMATTER)
    return console_handler
# def get_file_handler():
#    file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
#    file_handler.setFormatter(FORMATTER)
#    return file_handler
def get_logger(logger_name):
   logger = logging.getLogger(logger_name)
   logger.setLevel(logging.INFO)
   logger.addHandler(get_console_handler())
   # logger.addHandler(get_file_handler())
   # with this pattern, it's rarely necessary to propagate the error up to parent
   logger.propagate = False
   return logger

log = get_logger(APPNAME)

###
# UTILS HELPERS
###

def dict_contains(dct, fkey, fvalue):
    """
    Deep dictionary searching with filters
    """
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

def create_output_path(path):
    """
    Create and return the created path/folder object
    """
    folder = pathlib.Path(path)
    if not folder.exists():
        folder.mkdir(parents=True)
    return folder

def get_catlongname(cat):
        """
        Return a long name (if known) for a given category.
        """
        knowncats = settings['categories']
        if cat is None: return knowncats
        if cat in knowncats.keys(): return knowncats[cat]
        else: return cat.upper()





#################### COLLECT #####################

def get_module_details_from_file(mfpath, filters):
    """
    Get module information based on its LUA filepath

    Args:
       mfpath  (str):  path to resif root directory
       filters (dict): eventual filters to apply

    Return module dictionary with description, category, ... if succesfully retrieved
    Return False is failed
    """

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


def collect_softwares(paths, filters=None):
    """
    Iterate and deepmerge over list of module filepath to generate a map

    Args:
       paths   (str): resif root path to analyse
       filters (dict): eventual list of filters to apply ('archs','clusters' or 'swsets')
                       Default: None

    Return dict of collected software
    """
    collected_softwares = {}

    for filepath in paths:
        module_details = get_module_details_from_file(filepath.rstrip(), filters)
        # If the module is found and corresponds to filters we gave, then we add it to the returned map
        if module_details:
            collected_softwares = dict_merge(collected_softwares, module_details)

    return collected_softwares

#################### RENDER #####################

###
# Render markdown files from collected software list
##
def render_markdown_from_collect(collected_softwares,
                                 output_path='docs/software/swsets',
                                 filters=None):
    """
    Write into markdown files software details taken out from the available
    software modules analysed by the 'collect' action (invoking
    collect_softwares(...)) aimed to be displayed in the mkdocs[-material]
    website
    This will typically generate the following file structure:

    <output_path>/all_softwares.md
    ├── all_softwares.md   list of all software ever built
    ├── <version>.md       software list in RESIF swset <version>
    ├── <category>.md      list of all software belonging to category '<category>'
    └── <category>/
    .   ├── <software>.md    short summary and available version for software <software>
    .   └── [...]            belonging to category <category>

    Args:
       collected_softwares (dict): dictionnary of all collected software (typically loaded
                                   from a yaml file)
       output_path (str): where to store the generated markdown files
       filters (dict): eventual filters to apply
    """
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
            if filters['categories'] and category_name not in filters['categories']: continue
            if filters['swsets']: continue
            log.info(f'Generating markdown file { software_file }')
            df = pd.DataFrame(detailed_software_array, columns=['Version','Swset','Architectures','Clusters'])
            with software_file.open("w") as fd:
                fd.write("### %s\n" % software_key)
                fd.write("\n")
                fd.write("* [official website](%s)\n" % software_details['www'])
                fd.write("* __Category__: %s (%s)\n" %  (get_catlongname(category_name), category_name))
                fd.write("\n")
                fd.write("Available versions of %s on ULHPC platforms:\n" % software_key)
                fd.write("\n")
            with software_file.open("a") as fd:
                df.to_markdown(fd)
            with software_file.open("a") as fd:
                fd.write("\n\n")
                fd.write("> %s\n" % software_details['desc'])


            # Make sure we keep generic information for all_softwares.md
            all_softwares = {**all_softwares, **software_without_details}

    # Write into SWSET.md (example: 2020b.md) all included softwares information
    for swset_label, swset_list_softwares in softwares_swset.items():
        if (not filter) or (filters['swsets'] and swset_label in filters['swsets']):
            log.info(f'Generating markdown file { output_folder }/{ swset_label }.md')
            df = pd.DataFrame.from_dict(swset_list_softwares, orient="index", columns=['Architectures','Clusters','Category','Description'])
            df.index.name='Software'
            df.sort_values(by=['Software'], inplace=True)
            with (output_folder / (swset_label + ".md")).open("w") as fd:
                df.to_markdown(fd)

    df = pd.DataFrame.from_dict(all_softwares, orient="index",
                                columns=['Versions',
                                         'Swsets',
                                         'Architectures',
                                         'Clusters',
                                         'Category',
                                         'Description'])
    df.index.name='Software'
    df.sort_values(by=['Software'], inplace=True)
    # Write generic software information we gathered in all_software.md
    if (not filter):
        log.info(f'Generating markdown file { output_folder }/all_software.md')
        with (output_folder / "all_softwares.md").open("w") as fd:
            df.to_markdown(fd)

    # restart focusing on software category
    # Write into <category>.md (Ex: bio.md) all associated softwares information
    df.sort_values(by=['Category'], inplace=True)
    for category_name in collected_softwares.keys():
        if filters['categories'] and category_name not in filters['categories']:
            continue
        category_df = df[df['Category'] ==  get_catlongname(category_name)]
        #pprint.pprint(category_df)
        category_file = output_folder / (category_name + ".md")
        if not category_df.empty:
            log.info(f'Generating markdown file { category_file }')
            with (category_file).open("w") as fd:
                fd.write("## %s (%s)\n" % (get_catlongname(category_name), category_name))
                fd.write("\n")
                fd.write("Alphabetical list of available ULHPC software ")
                fd.write("belonging to the '%s' category\n" % category_name)
                fd.write("\n")
            with (category_file).open("a") as fd:
                category_df.sort_values(by=['Software']).to_markdown(fd)


###############################################################################
# Command line interface with click
@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
@click.option('-V', '--version', flag_value=True, help='Return the version of this script.')
@click.option('-v', '--verbose', count=True,      help='Verbosity level')
@click.option('--debug', is_flag=True, default=False, help='Debug mode')
@click.option('--noop', '--dry-run', is_flag=True, default=False, help='Dry run mode')
def cli(ctx, version, verbose, debug, noop):
    """
    Main command line interface
    """
    if noop: settings['noop'] = True
    if debug:
        settings['debug'] = True
        log.setLevel(logging.DEBUG)
    if (verbose > 0): log.setLevel(logging.DEBUG)
    if ctx.invoked_subcommand is None:
        if version:
            click.echo("This is " + os.path.basename(__file__) + " version " + __version__)
        else:
            click.echo(ctx.get_help())
    # pprint.pprint(settings)

# sub command 'collect'
@cli.command()
@click.pass_context
@click.option('-a', '--arch', type=click.Choice(settings['archs'], case_sensitive=False),
              help='Filter output by RESIF architecture')
@click.option('-c', '--cluster', type=click.Choice(settings['clusters'], case_sensitive=False),
              help='Filter output by cluster')
@click.option('-s', '--swset', multiple=True, metavar='YYYY{a|b}',
              default=settings['swsets_versions'], show_default=True,
              help='Filter output by RESIF software set version (Ex: 2020b)')
@click.option('-p', '--resif-root-path', type=click.Path(exists=True), default=settings['resif_root_path'],
              help='set RESIF root path. In particular, modules and software installed by RESIF' +
              'can be found under PATH/<cluster>/<version>/<arch>/{software,modules}')
@click.option('-o', '--output', type=click.File('w'), metavar='YAMLFILE',
              default=None, help="Set output file for the dict (Default output to STDOUT)")
def collect(ctx,
            arch,      # type: Union['broadwell','skylake','gpu','epyc']
            cluster,   # type: Union['iris', 'aion']
            swset,    # type: Array[str]
            resif_root_path,  # type: str (directory path)
            output     # type: Union[None, str] (writable file path)
            ):
    """
    Collect meta-data dict of the RESIF3 modules installed and
    (eventually) export them as YAML

    /!\ IMPORTANT: you probably want to run this operation on the cluster
    to access the resif directories

    Use 'make resif-collect' for that purpose
    """
    log.info('Collect meta-data for the available RESIF modules')
    log.debug(f'click context:\n {  pprint.pformat(ctx.params) } ')
    log.info(f'RESIF root path: { resif_root_path }')
    if bool(re.match('.*(iris|aion)-cluster\.uni\.lux$', socket.getfqdn())):
        default_search_paths = "%s/iris %s/aion" % (resif_root_path, resif_root_path)
    else:
        default_search_paths = "%s" % resif_root_path
    log.info(f'default searched path: { default_search_paths }')
    find_cmd = [
        "find",
        default_search_paths,
        " -type d",
        "\( -name ebfiles_repo -o -name software \)",
        "-prune",
        "-false",
        "-o",
        "-type f  \( -iname '*.lua'  ! -iname '.*' \)"
    ]
    log.info(f'Find command to collect lua module files in production:\n     { " ".join(find_cmd) }')
    # Python 3.6 on iris/aion -- starting 3.7, it is recommended to use
    #        subprocess.run([ ... ], capture_output=True)
    if sys.version_info < (3, 7):
        lualist = subprocess.check_output(f'{ " ".join(find_cmd) }',  shell=True).decode('utf-8').split()
    else:
        lualist = subprocess.run(f'{ " ".join(find_cmd) }', capture_output=True).stdout.decode('utf-8').split()
    # log.debug(f'List of LUA files to analyse:\n    { pprint.pformat(lualist) }')

    filters = {}
    if arch    is not None: filters['archs'] = arch
    if cluster is not None: filters['clusters'] = cluster
    if swset   is not None: filters['swsets'] = swset
    log.debug(f'Filters to apply: {  pprint.pformat(filters) }')
    result = collect_softwares(lualist, filters)
    pprint.pprint(type(result))
    log.info(f'Resulting collected dict: \n{ pprint.pformat(result) }')
    if output is not None:
        yaml.dump(result, output, allow_unicode=True, default_flow_style=False)
        output.close()

# sub command 'render'
@cli.command(short_help='Generate markdown files summarizing available ULHPC modules')
@click.pass_context
@click.option('-i', '--input', type=click.File('r'), metavar='YAMLFILE',
              default='data/%s' % settings['yamlfile'], show_default=True,
              help="Set YAML input file for the dict storing resif module informations (generated by the 'collect' subcommand)")
@click.option('-o', '--output-dir', type=click.Path(exists=True), metavar='DIR',
              default=settings['output_dir'], show_default=True,
              help="Set output directory where to generate the markdown files")
@click.option('-s', '--swset', multiple=True, metavar='YYYY{a|b}', default=None,
              help='generate only markdown for the specified software set (Ex: 2020b)')
@click.option('-c', '--category', multiple=True, metavar='NAME',
              type=click.Choice(settings['categories'].keys()),
              help='generate only markdown for the specified category (Ex: bio)')
def render(ctx, input, output_dir, swset, category):
    """
    Generate/Render markdown files summarizing the available software modules
    under <output_path>/
    """
    log.info('Render meta-data for the available RESIF modules')
    log.debug(f'click context:\n {  pprint.pformat(ctx.params) } ')

    log.info(f'Load input resif module information from file { input }')
    resif_modules = yaml.load(input, Loader=yaml.SafeLoader)
    # pprint.pprint(resif_modules)
    filters = {}
    if swset    is not None: filters['swsets'] = swset
    if category is not None: filters['categories'] = category
    render_markdown_from_collect(resif_modules, output_dir, filters)


if __name__ == "__main__":
    cli()
