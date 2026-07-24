import json
import socket
import os
from pathlib import Path

from easybuild.tools.options import set_up_configuration
from easybuild.framework.easyconfig.easyconfig import process_easyconfig
from easybuild.framework.easyconfig.parser import EasyConfigParser
import pandas as pd

#-----------------------------------------
# Run only with Easybuild versions 5.3.x or above
# Define available software releases
# Add only software in "release" modules! Only one build number in release.

cluster_info = {
    'releases' : [
        "2025a",
        "2024a",
        "2023b",
    ],

    'build' : "rhel810-20260107",

    'architectures' : {
        'epyc' : "AMD EPYC",
        'broadwell' : "Intel Broadwell",
        'skylake' : "Intel Skylake",
        'saphirerapids' : "Intel Sapphire Rapids",
        'gpu' : "NVIDIA Tesla",
    },

    'base_path' : "/opt/apps/easybuild/systems/"
}

#-----------------------------------------

###############################
## EXTRACT EASYCONFIGS INFO ##
###############################

def get_software_stack(software_path, hwd_data):
    stack = []

    for eb in software_path.rglob("*.eb"):
        if "reprod" in eb.parts:
            continue
        
        print(eb)
        extract_easyconfigs_info(eb, software_path, stack, hwd_data)

    return stack


def extract_easyconfigs_info(eb, software_path, stack, hwd_data):
    if eb.is_relative_to(software_path / "EasyBuild"):
        return stack

    try:
        parser = EasyConfigParser(filename = str(eb))
        ec = parser.get_config_dict(validate = False)

        package = {
            "Name": ec.get("name"),
            "Version": ec.get("version"),
            "Homepage": ec.get("homepage"),
            "Architectures": cluster_info["architectures"][hwd_data[1]],
            "Clusters" : hwd_data[0],
            "Description": ec.get("description"),
            "Category": ec.get("moduleclass"),
        }

        stack.append(package)

    except Exception as excpt:
        print(f"Failed: {eb}: {excpt}")

    return stack

#-----------------------------------------

##########################
## CLEAN AND MERGE DATA ##
##########################

def homepage_link(text, url):
    if pd.notna(url) and url:
        return f"[{text}]({url})"
    return text

def get_software_table(stack):
    df = pd.DataFrame(stack)

    # Clean software descriptions
    df["Description"] = (df["Description"]
        .fillna("")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip())
        
    # Combine versions for the same software
    df = df.groupby(
            ["Name",
             "Homepage",
             "Architectures",
             "Clusters",
             "Category",
             "Description"],
            as_index=False
        ).agg({
            "Version": ( lambda x: "<br>".join(sorted(list(set(x)))) ),
        })

    # Create Markdown hyperlinks
    df["Software"] = df.apply(
        lambda row: homepage_link(row["Name"], row["Homepage"]),
        axis=1,
    )
    
    return df

def merge_dataframes(stack, collapse_descr = True):
    # Take all df corresponding to the same release
    df = pd.concat(stack, ignore_index=True)

    # Group software available in different clusters and arch
    merged_result = (
        df.groupby(
            ["Software", "Version", "Category", "Description"],
            as_index=False,
        )
        .agg({
            "Architectures": lambda s:", ". join(sorted(set(s))),
            "Clusters": lambda s:", ". join(sorted(set(s))),
        })
    )

    # Reorder data for Markdown table
    merged_result = merged_result[
        [
            "Software",
            "Version",
            "Architectures",
            "Clusters",
            "Category",
            "Description",
        ]
    ]

    if collapse_descr == True:
        merged_result["Description"] = merged_result["Description"].apply(
            lambda d: (
                "<details>"
                "<summary>Show</summary>"
                f"{d}"
                "</details>"
            )
        )

    return merged_result


#-----------------------------------------

#####################
## MAIN FUNCTIONS ###
#####################

def get_sotfware_tables(save_data = True):
    clusters = os.listdir(cluster_info['base_path'])
    clusters.remove('binary')

    stack = {}
    for rel in cluster_info['releases']:
        stack[rel] = []
        for cl in clusters:
            hwd_data = [cl, None]
            archs = os.listdir(str(Path(cluster_info['base_path']) / cl / cluster_info['build'] / rel))
            for arch in archs:
                hwd_data[1] = arch
                full_path = f"{cluster_info['base_path']}{cl}/{cluster_info['build']}/{rel}/{arch}/software/"
                tmp_stack = get_software_stack(Path(full_path), hwd_data)
                stack[rel].append(get_software_table(tmp_stack))
        result = merge_dataframes(stack[rel])

        if save_data == True:
            with open(f"{rel}.md", "w") as f:
                f.write(result.to_markdown(index = False))

## Keep JSON too
#df.to_json("stack.json", orient="records", indent=2)

#-----------------------------------------

def main():
    options, cfg_settings = set_up_configuration(args=[])
    get_sotfware_tables()
                        
if __name__ == "__main__":
    main()

