#!/usr/bin/env python3

import os
import sys
import getopt
import glob
import time
import subprocess as SP
import re
import pandas as pd
import argparse
import pathlib

def get_modulefile_whatis(mfpath):
    ''' Read a EasyBuild LUA modulefile, get and return the description and web address from the whatis blocks. '''
    try:
        f = open(mfpath, 'r')
        raw = f.readlines()
        f.close()
    except Exception as e:
        desc = "No description available."
        www = ""
        return desc, www
    
    desc = []

    # The description is split between many lines, get them in a list
    isDescLine = False
    for line in raw:
        line = line.strip()
        if line.startswith("whatis([[Description:") or line.startswith("whatis([==[Description:"): isDescLine = True
        if line.startswith("whatis([[Homepage:") or line.startswith("whatis([==[Homepage:"): 
            isDescLine = False    # description ends before www whatis block
            match_homepage = line
        if isDescLine and (line != ''): desc.append(line)

    desc[0] = desc[0].replace('whatis([[Description: ',"").replace('whatis([==[Description: ',"").replace('whatis([==[Description:',"")
    desc[-1] = desc[-1].replace(']])','').replace(']==])','')
    www = match_homepage.replace('whatis([[Homepage: ',"").replace('whatis([==[Homepage: ',"").replace(']])',"").replace(']==])',"")
    # If the description is in UTF-8, convert to ASCII (ignore what can't be converted)
    full_desc = (" ".join(filter(None, desc)))#.decode('utf-8').encode('ascii', 'ignore')
    return full_desc, www

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


def collect(lst):
    softwares={}
    all_sw_versions=set()
    all_bundles=set()
    with open(lst,'r') as fd:
        for cnt, line in enumerate(fd):
            if not re.match(r'^#',line):
                software_description,url=get_modulefile_whatis(line.rstrip())
                row = line.split("/")
                software_version=row[-1].split(".lua")[0]
                software_name="<p><a href={0}>{1}</a></p>".format(url,row[-2])
                if row[-2].startswith("ULHPC"):
                    all_bundles.add(software_name)
                software_categorie="<p>{0}</p>".format(get_catlongname(row[-3]))
                software_cluster=row[4]
                
                software_swset=row[5]
                all_sw_versions.add(software_swset)


                software_archi=row[6]
                #if softwares.get(software_name,None) is None:
                softwares[software_name]=["<p>{0}</p>".format(software_version),"<p>{0}</p>".format(software_swset),"<p>{0}</p>".format(software_archi),software_categorie,"<p>{0}</p>".format(software_cluster),software_description]
                #else:
                #    softwares[software_name][0] = softwares[software_name][0].replace("</p>","<br>{0}</p>".format(software_version))  
                #    softwares[software_name][1] = softwares[software_name][1].replace("</p>","<br>{0}</p>".format(software_swset))  
                #    softwares[software_name][2] = softwares[software_name][2].replace("</p>","<br>{0}</p>".format(software_archi))  
    df=pd.DataFrame.from_dict(softwares,orient="index",columns=['Version','Swset','Architecture','Category','Clusters','Description'])
    df.index.name="Software"
    df.sort_values(['Software','Version'], ascending=[False,True], inplace=True)


    folder=pathlib.Path("/tmp/software_list")
    if not folder.exists():
        folder.mkdir(parents=True)

    all_softwares=folder / "all_softwares.md"
    with all_softwares.open("w") as fd:
        df.to_markdown(fd)
        
    all_categories=get_catlongname(None)
    for version in all_sw_versions: 
     folder_version = folder / "{0}".format(version)
     if not folder_version.exists():
        folder_version.mkdir(parents=True)
     for cat in all_categories:
         cat_softwares = folder_version / "{0}-{1}.md".format(version,cat)
         with cat_softwares.open("w") as fd:
             df[(df['Category']=="<p>{0}</p>".format(all_categories[cat])) &  (df['Swset']=="<p>{0}</p>".format(version))].to_markdown(fd)

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="resif3_module2markdown.py")
    parser.add_argument("collect", type=str, help="Collect software info. Should be executed remotely")
    args = parser.parse_args()
    if args.collect is not None:
        collect(args.collect)
