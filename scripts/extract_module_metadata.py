import yaml
import argparse
import typing
import pandas as pd
import itertools
import functools
import pathlib
from easybuild.framework.easyconfig.parser import EasyConfigParser

#-----------------------------------------
# Run only with Easybuild versions 5.3.x or above
# Add only software in "release" modules! Only one build number in release.

def toolchain_to_maybe_string(toolchain):
    if toolchain['name'] == "system":
        return "system"

    return "{name}-{version}".format(name = toolchain['name'], version = toolchain['version'])

def add_package_if_module_exists(package, installation_path, stack):
    module_filename = package['Version']
    if package['Toolchain'] != "system":
        module_filename += '-'
        module_filename += package['Toolchain']
    module_filename += '.lua'

    module_path = installation_path / "modules" / "all" / package['Category'] / package['Name'] / module_filename

    if module_path.exists():
        stack.append(package)

def extract_easyconfig_info(eb, installation_path, stack):
    try:
        parser = EasyConfigParser(filename = str(eb))
        ec = parser.get_config_dict(validate = False)

        package = {
            'Name': ec['name'],
            'Version': ec['version'],
            'Homepage': ec['homepage'],
            'Description': ec['description'],
            'Toolchain': toolchain_to_maybe_string(ec['toolchain']),
            'Category': ec.get('moduleclass'),
        }

        add_package_if_module_exists(package, installation_path, stack)

    except Exception as excpt:
        print(f"Failed: {eb}> {excpt}")

    return stack

def get_installation_target_package_list(installation_path):
    software_path = installation_path / "software"

    nested_report_ebs = (p.glob("*.eb") for p in software_path.glob("*/*/easybuild/reprod") if p.is_dir())
    report_ebs = itertools.chain.from_iterable(nested_report_ebs)

    stack = list()
    for eb in report_ebs:
        extract_easyconfig_info(eb, installation_path, stack)

    return stack

def homepage_link(text, url):
    if pd.notna(url) and url:
        return f"[{text}]({url})"
    return text

def clean_software_description(software_table, collapse_descr = True):
    software_table['Description'] = (software_table['Description']
        .fillna("")
        .str.replace(r"\s+", " ", regex=True)
        .str.strip())

    if collapse_descr == True:
        software_table['Description'] = software_table['Description'].apply(
            lambda d: (
                "<details>"
                "<summary>Show</summary>"
                f"{d}"
                "</details>"
            )
        )

def generate_installation_target_package_table(stack, collapse_descr = True):
    df = pd.DataFrame(columns=['Name', 'Version', 'Homepage', 'Description', 'Toolchain', 'Category'])

    if len(stack) > 0:
        df = pd.concat([df, pd.DataFrame(stack)], ignore_index=True)
    clean_software_description(df, collapse_descr)

    if len(df) > 0:
        df['Software'] = df.apply(
            lambda row: homepage_link(row['Name'], row['Homepage']),
            axis=1,
        )
    else:
        df['Software'] = pd.Series()

    df = df[['Name', 'Version', 'Software', 'Toolchain', 'Category', 'Description']]

    return df

def get_build_software_tables(base_path: pathlib.Path, build_number: str, releases: dict[str, dict[str, dict[str, list[str]]]]):
    software_tables = dict()

    release = releases.get(build_number)
    if release is None:
        return software_tables

    for cluster in release.keys():
        for arch in release[cluster].keys():
            for release_id in release[cluster][arch]:
                target_installation_path = base_path / cluster / arch / release_id / build_number
                stack = get_installation_target_package_list(target_installation_path)
                table = generate_installation_target_package_table(stack)

                # One build per (cluster, arch) in release!
                software_tables[(cluster, arch, release_id)] = table

    return software_tables

class ArchitectureBuilds(typing.NamedTuple):
    architecture: str
    toolchains: set[str]

    def __str__(self) -> str:
        toolchain_list = ", ".join(self.toolchains)
        return self.architecture + "(" + toolchain_list + ")"

    def __hash__(self) -> int:
        return hash(self.architecture)

class ClusterBuilds(typing.NamedTuple):
    cluster: str
    architecture_builds: set[ArchitectureBuilds]

    def __str__(self) -> str:
        res = "<tr>"
        res += "<th>" + self.cluster + "</th>"
        res += "<td>" + ", ".join(map(lambda s: str(s), self.architecture_builds)) + "</td>"
        res += "</tr>"
        return res

    def __hash__(self) -> int:
        return hash(self.cluster)

class RelaseBuilds(typing.NamedTuple):
    cluster_builds: set[ClusterBuilds]

    def __str__(self) -> str:
        res = "<details><summary>Show</summary> <table><tbody> "
        res += " ".join(map(lambda s: str(s), self.cluster_builds))
        res += " </tbody></table> </details>"
        return res

    def __hash__(self) -> int:
        return hash("_".join(self.cluster_builds))

def merge_release_package_installations(tables):
    df = pd.concat(tables, ignore_index=True)

    if len(df) == 0:
        df = pd.DataFrame(columns=['Name', 'Version', 'Software', 'Category', 'Description', 'Built instances'])
        return df

    descriptions = df.apply(lambda row: {row['Description']}, axis=1)
    categories = df.apply(lambda row: {row['Category']}, axis=1)
    df = df[['Name', 'Version', 'Software', 'Cluster', 'Architecture', 'Toolchain']]
    df['Description'] = descriptions
    df['Category'] = categories

    df = df.groupby(
        ['Name', 'Version', 'Software', 'Cluster', 'Architecture'],
        as_index=False,
    ).aggregate(
        {
            'Toolchain': (lambda s: set(s)),
            'Category': (lambda s: functools.reduce(lambda acc, v: acc | v, s, set())),
            'Description': (lambda s: functools.reduce(lambda acc, v: acc | v, s, set())),
        }
    )

    architecture_builds = df.apply(lambda row: ArchitectureBuilds(architecture=row['Architecture'], toolchains=row['Toolchain']), axis=1)
    df = df[['Name', 'Version', 'Software', 'Cluster', 'Category', 'Description']]
    df['ArchitectureBuilds'] = architecture_builds

    df = df.groupby(
        ['Name', 'Version', 'Software', 'Cluster'],
        as_index=False,
    ).aggregate(
        {
            'ArchitectureBuilds': (lambda s: set(s)),
            'Category': (lambda s: functools.reduce(lambda acc, v: acc | v, s, set())),
            'Description': (lambda s: functools.reduce(lambda acc, v: acc | v, s, set())),
        }
    )

    cluster_builds = df.apply(lambda row: ClusterBuilds(cluster=row['Cluster'], architecture_builds=row['ArchitectureBuilds']), axis=1)
    df = df[['Name', 'Version', 'Software', 'Category', 'Description']]
    df['ClusterBuilds'] = cluster_builds

    df = df.groupby(
        ['Name', 'Version', 'Software'],
        as_index=False,
    ).aggregate(
        {
            'ClusterBuilds': (lambda s: set(s)),
            'Category': (lambda s: functools.reduce(lambda acc, v: acc | v, s, set())),
            'Description': (lambda s: functools.reduce(lambda acc, v: acc | v, s, set())),
        }
    )

    release_builds = df.apply(lambda row: RelaseBuilds(cluster_builds=row['ClusterBuilds']), axis=1)
    df = df[['Name', 'Version', 'Software', 'Category', 'Description']]
    df['Built instances'] = release_builds.apply(lambda r: str(r))

    if functools.reduce(lambda acc, v: max(acc, v), df['Category'].apply(len), 1) != 1:
        raise Exception(f"Ambigious category definitions in software set.")
    if functools.reduce(lambda acc, v: max(acc, v), df['Description'].apply(len), 1) != 1:
        raise Exception(f"Ambigious description definitions in software set.")

    df['Category'] = df['Category'].apply(lambda x: x.pop())
    df['Description'] = df['Description'].apply(lambda x: x.pop())

    df = df.sort_values(by=['Name', 'Version'])

    return df

def merge_build_tables_per_release(build_tables):
    tables_listed_per_release = dict()
    for release in build_tables.keys():
        cluster, arch, release_id = release
        table = build_tables[release]
        table['Cluster'] = pd.Series([cluster for i in range(len(table))])
        table['Architecture'] = pd.Series([arch for i in range(len(table))])

        if tables_listed_per_release.get(release_id) is None:
            tables_listed_per_release[release_id] = [table]
        else:
            tables_listed_per_release[release_id].append(table)

    return { release: merge_release_package_installations(tables) for release, tables in tables_listed_per_release.items() }

def get_build_tables_per_release(base_path: pathlib.Path, build_number: str, releases: dict[str, dict[str, dict[str, list[str]]]]):
    build_tables = get_build_software_tables(base_path, build_number, releases)
    build_tables_per_release = merge_build_tables_per_release(build_tables)

    return build_tables_per_release

def save_build_tables_per_release(build_tables_per_release, output_path: pathlib.Path):
    for release, table in build_tables_per_release.items():
        output_file = output_path / (release + ".md")
        with open(str(output_file), "w") as file:
            file.write(
            table[
                [
                     'Software',
                     'Version',
                     'Category',
                     'Built instances',
                     'Description',
                ]
            ].to_markdown(index = False))

def get_software_installation_config(config_path: pathlib.Path) -> dict:
    with open(str(config_path), 'r') as config_file:
        config = yaml.safe_load(config_file)
    return config

def get_releases(config: dict) -> dict[str, dict[str, dict[str, list[str]]]]:
    return config['sofware']

def get_base_path(config: dict) -> pathlib.Path:
    path: str = config['base_path']
    return pathlib.Path(path)

def create_build_table_pages_per_release(
    configuration: pathlib.Path,
    build_number: str,
    output_path: pathlib.Path
):
    config = get_software_installation_config(configuration)

    releases = get_releases(config)
    base_path = get_base_path(config)

    build_tables = get_build_tables_per_release(base_path, build_number, releases)
    save_build_tables_per_release(build_tables, output_path)

def main():
    parser = argparse.ArgumentParser(
        prog = "extract_module_metadata",
        description = "Collect the modules installed with the easybuild stack in a set of pages for easy search in the UL HPC documentation"
    )
 
    parser.add_argument("configuration", type=pathlib.Path, help="a YAML file with the configurations that will be processed")
    parser.add_argument("release", type=str, help="the release in the configuration file for which the sfoftware tables will be generated")
    parser.add_argument("output_path", type=pathlib.Path, help="path to the directory where the software list will be stored")

    args = parser.parse_args()

    create_build_table_pages_per_release(args.configuration, args.release, args.output_path)

if __name__ == "__main__":
    main()

def set_nested_map(mp, entries, value):
    if len(entries) == 0:
        return dict()

    entry = entries.pop(0)
    if len(entries) == 0:
        mp[entry] = value
        return mp

    if len(mp) == 0:
        mp[entry] = dict()

    val = set_nested_map(mp[entry], entries, value)
    mp[entry] = val

    return mp

# e.g. software_tables = set_nested_map(software_tables, [cluster, arch, version], table)

