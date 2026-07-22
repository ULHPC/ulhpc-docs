from easybuild.tools.options import set_up_configuration
from easybuild.framework.easyconfig.easyconfig import process_easyconfig
from pathlib import Path
import pandas as pd
import json

# Add only software in "release" modules! Only one build number in release.
software = {
    "aion": {
        "epyc": {
            "2026a": "rhel810-20260107",
            "2025a": None,
            "2024a": None,
            "2023b": None,
        },
    },
    "iris": {
        "broadwell": {
            "2026a": None,
            "2025a": None,
            "2024a": None,
            "2023b": None,
        },
        "skylake": {
            "2026a": None,
            "2025a": None,
            "2024a": None,
            "2023b": None,
        },
        "gpu": {
            "2026a": None,
            "2025a": None,
            "2024a": None,
            "2023b": None,
        },
        "hopper": {
            "2026a": None,
            "2025a": None,
            "2024a": None,
            "2023b": None,
        },
    },
}
base_path = Path("/opt/apps/easybuild/systems/")

def extract_easyconfigs_info(eb, software_path, stack):
    if eb.is_relative_to(software_path / "EasyBuild"):
        return stack

    try:
        ecs = process_easyconfig(str(eb), validate = False)

        for ecdict in ecs:
            ec = ecdict["ec"]

            package = {
                "name": ec["name"],
                "version": ec["version"],
                "homepage": ec["homepage"],
                "description": ec["description"],
                "moduleclass": ec["moduleclass"],
            }

            stack.append(package)

    except Exception as excpt:
        print(f"Failed: {eb}: {excpt}")

    return stack

def get_software_stack(software_path):
    stack = []
    options, cfg_settings = set_up_configuration(args=[])

    for eb in software.rglob("*.eb"):
        #print(eb)
        extract_easyconfigs_info(eb, software_path, stack)

    return stack


# with open("stack.json", "w") as fp:
#     json.dump(stack, fp, indent=2, default=str)

#stack = pd.read_json("stack.json")

def homepage_link(text, url):
    if pd.notna(url) and url:
        return f"[{text}]({url})"
    return text

def get_softare_table(stack):
    df = pd.DataFrame(stack)

    # Clean software descriptions
    df["description"] = df["description"]
        .fillna("")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip()

    # Combine versions for the same software
    df = df.groupby(
            ["name", "homepage", "moduleclass", "description"],
            as_index=False
        ).agg({
            "version": ( lambda x: "<br>".join(sorted(list(set(x)))) ),
        })

    # Create Markdown hyperlinks
    df["software"] = df.apply(
        lambda row: homepage_link(row["name"], row["homepage"]),
        axis=1,
    )

    # Reorder columns
    df = df[
        [
            "software",
            "version",
            "moduleclass",
            "description",
        ]
    ]

    # Sort alphabetically
    df = df.sort_values(["software", "version"])

    return df

def set_nested_map(mp, entries, value):
    if len(entries) == 0:
        return dict()

    entry = entries.pop(0)
    if len(entries) == 0:
        mp[entry] = value
        return mp

    if len(mp) == 0:
        mp[entry] = dict()

    val = setup_map(mp[entry], entries, value)
    mp[entry] = val

    return mp

def get_software_tables():
    software_tables = dict()

    for machine in software.keys():
        for arch in software[machine].keys():
            for version in software[machine][arch].keys():
                if software[machine][arch][version] is not None:
                    build_number = software[machine][arch][version]
                    software_path = base_path / machine / arch / version / build_number / "software"
                    stack = get_software_stack(software_path)
                    table = get_softare_table(stack)

                    # One build per (machine, arch, version) in release!
                    software_tables = set_nested_map(software_tables, [machine, arch, version], table)

    return software_tables

## Write Markdown
#with open("stack.md", "w") as f:
#    f.write(df.to_markdown(index=False))

## Keep JSON too
#df.to_json("stack.json", orient="records", indent=2)
