# Compiling/Building your own software

We try to provide within the [ULHPC software sets](../software/swsets/index.md) the most used application among our users.
It may however happen that you may find a given software you expect to use to be either missing among the [available software sets](../software/swsets/all_softwares.md), or provided in a version you considered not enough recent.

In that case, the **RECOMMENDED** approach is to rely on [Easybuild](../environment/easybuild.md) to **EXTEND** the available software set.
Below are guidelines to support that case.

Alternatively, you can of course follow the installation guidelines provided on the software website to compile it the way it should be. For that case, you **MUST** rely on the provided [toolchains](../software/swsets/toolchain.md) and [compilers](software/swsets/compiler.md).

!!! important ""
    In all cases, **NEVER compile or build softawre from the ULHPC frontends!**
    Always perform these actions from the expected compute node, either reserved within an [interactive job](../jobs/interactive.md) or through a [passive submission](../jobs/submit.md)

## Missing or Outdated Software

You should first search if an existing Easyconfig exists for the software:

```bash
# Typical check for user on ULHPC clusters
$ si    # get an interactive job - use 'si-gpu' for GPU nodes on iris
$ module load tools/EasyBuild
$ eb -S <name>
```

It shoud match the available software set versions summarized below:

{%
   include-markdown "../environment/modules.md"
   start="<!--table-swsets-toolchains-versionning-start-->"
   end="<!--table-swsets-toolchains-versionning-end-->"
%}

You will then be confronted to the following cases.

### An existing easyconfigs exists for the target toolchain version

You're lucky but this is very likely to happen (and justify to rely on [streamline Easyconfigs](https://github.com/easybuilders/easybuild-easyconfigs/tree/develop))

* Typical Example:
    - `CMake-<version>-GCCcore-<gccversion>.eb`: depends on GCCcore, thus common to both `foss` and `intel`. The same happens with `GCC`
    - `Go-<version>.eb` (no dependency on any toolchain)
    - `Boost-<version>-{gompi,iimpi}-<toolchainversion>.eb`, derived toolchains, compliant with `foss` (resp. `intel`) ones;
    - `GDAL-<version>-{foss,intel}-<toolchainversion>-Python-<pythonversion>.eb`

In that case, you **MUST** test the build in your home or in a shared project using the `resif-load-{home,project}-swset-{prod,devel}` helpers to set a consistent environment for your builds compilant with the ULHPC software sets layout (in particular with regards the `$EASYBUILD_PREFIX` and `$MODULEPATH` environment variables). See [below](#using-easybuild-to-build-software-in-your-home) for building instructions.

### An outdated easyconfig exists

Then the easiest way is to _adapt_ the existing easyconfig file for the target softare version **AND** one of the **available** toolchain version. You may want also to ensure an [ongoing Pull-Request](https://github.com/easybuilders/easybuild-easyconfigs/pulls) is not dealing with the version you're looking for.

Assuming you're looking for the software `<name>` (first letter `<letter` (in lower case), for instance if `<name>=NWChem`, then `<letter>=n`), first copy the existing easyconfig file in a convenient place

```bash
# Create host directory for your custom easyconfigs
$ mkdir -p ~/easyconfigs/<letter>/<name>

$ eb -S <name>` # find the complete path to the easyconfig file
CFGS1=[...]/path/to/easyconfigs
* $CFGS1/<letter>/<name>/<name>-<oldversion>[...].eb
* $CFGS1/<letter>/<name>/<name>-[...].patch     # Eventual Patch file

# copy/paste the definition of the CFGS1 variable (top line)
CFGS1=[...]/path/to/easyconfigs
# copy the eb file
cp $CFGS1/<letter>/<name>/<name>-<oldversion>[...].eb ~/easyconfigs/<letter>/<name>
```

Now (_eventually_) check on the software website for the most up-to-date version `<version>` of the software released. Adapt the filename of the copied easyconfig to match the target version / toolchain

```bash
cd ~/easyconfigs/<letter>/<name>
mv <name>-<oldversion>[...].eb <name>-<version>[...].eb
```

!!! example "Example"
    ```bash
    cd ~/easyconfigs/n/NWCHem
    mv NWChem-7.0.0-intel-2019b-Python-3.7.4.eb NWChem-7.0.2-intel-2021b.eb  # Target 2021b intel toolchain, no more need for python suffix
    ```

Now you shall edit the content of the easyconfig -- you'll typically have to adapt the version of the dependencies and the checksum(s) to match the static versions set for the target toolchain, enforce https urls etc.

Below is a past complex exemple illustrating the adaptation done for GDB

```diff
--- g/GDB/GDB-8.3-GCCcore-8.2.0-Python-3.7.2.eb	2020-03-31 12:17:03.000000000 +0200
+++ g/GDB/GDB-9.1-GCCcore-8.3.0-Python-3.7.4.eb	2020-05-08 15:49:41.000000000 +0200
@@ -1,31 +1,36 @@
 easyblock = 'ConfigureMake'

 name = 'GDB'
-version = '8.3'
+version = '9.1'
 versionsuffix = '-Python-%(pyver)s'

-homepage = 'http://www.gnu.org/software/gdb/gdb.html'
+homepage = 'https://www.gnu.org/software/gdb/gdb.html'
 description = "The GNU Project Debugger"

-toolchain = {'name': 'GCCcore', 'version': '8.2.0'}
+toolchain = {'name': 'GCCcore', 'version': '8.3.0'}

 source_urls = [GNU_SOURCE]
 sources = [SOURCELOWER_TAR_XZ]
-checksums = ['802f7ee309dcc547d65a68d61ebd6526762d26c3051f52caebe2189ac1ffd72e']
+checksums = ['699e0ec832fdd2f21c8266171ea5bf44024bd05164fdf064e4d10cc4cf0d1737']

 builddependencies = [
-    ('binutils', '2.31.1'),
-    ('texinfo', '6.6'),
+    ('binutils', '2.32'),
+    ('texinfo', '6.7'),
 ]

 dependencies = [
     ('zlib', '1.2.11'),
     ('libreadline', '8.0'),
     ('ncurses', '6.1'),
-    ('expat', '2.2.6'),
-    ('Python', '3.7.2'),
+    ('expat', '2.2.7'),
+    ('Python', '3.7.4'),
 ]

+preconfigopts = "mkdir obj && cd obj && "
+configure_cmd_prefix = '../'
+prebuildopts = "cd obj && "
+preinstallopts = prebuildopts
+
 configopts = '--with-system-zlib --with-python=$EBROOTPYTHON/bin/python --with-expat=$EBROOTEXPAT '
 configopts += '--with-system-readline --enable-tui --enable-plugins --disable-install-libbfd '
```

__Note on dependencies version:__ typically as in the above  example, the version to use for dependencies are not obvious to guess (Ex: `texinfo`, `expat` etc.) and you need to be aware of the matching toolchain/GCC/binutils versions for the available `prod` or `devel` software sets recalled before -- use `eb -S <dependency>` to find the appropriate versions.


### None (or only very old/obsolete) easyconfigs are suggested

Don't panic, it simply means that the  **official** repositories do not hold any recent reciPY for the considered software.
 You _may_ find a __pending [Pull-request](https://github.com/easybuilders/easybuild-easyconfigs/pulls)__ addressing the software you're looking for.

Otherwise, you can either try to create a new easyconfig file, or simply follow the installation guildes for the considered software to build it.


## Using Easybuild to Build software in your Home

See also [Technical documentation](https://hpc-docs.uni.lu/environment/easybuild/#ulhpc-easybuild-configuration) to better understand the Easybuild configuration.

!!! warning ""
    If upon Dry-run builds (`eb -Dr [...]`) you find most dependencies **NOT** satisfied, you've likely made an error and may be trying to build a software against a toolchain/software set not supported either as `prod` or `devel`.

```bash
# BETTER work in a screen or tmux session ;)
$ si[-gpu] [-c <threads>]   # get an interactive job
$ module load tools/EasyBuild
# /!\ IMPORTANT: ensure EASYBUILD_PREFIX is correctly set to [basedir]/<cluster>/<environment>/<arch>
#                and that MODULEPATH is prefixed accordingly
$ resif-load-home-swset-{prod | devel}  # adapt environment
$ eb -S <softwarename>   # confirm <filename>.eb == <softwarename>-<version>[-<toolchain>][-<suffix>].eb
$ eb -Dr <filename>.eb   # check dependencies, normally most MUST be satisfied
$ eb -r  <filename>.eb
```

From that point, the compiled software and associated module is available in your home and can be used as follows in [launchers](../slurm/launchers.md) etc. -- see [ULHPC launcher Examples](../slurm/launchers.md)

```bash
#!/bin/bash -l # <--- DO NOT FORGET '-l' to facilitate further access to ULHPC modules
#SBATCH -p <partition>
#SBATCH -N 1
#SBATCH --ntasks-per-node <#sockets * s>
#SBATCH --ntasks-per-socket <s>
#SBATCH -c <thread>

print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
# Safeguard for NOT running this launcher on access/login nodes
module purge || print_error_and_exit "No 'module' command"

resif-load-home-swset-prod  # OR  resif-load-home-swset-devel
module load <softwarename>[/<version>]
[...]
```

## Using Easybuild to Build software in the <project> project

Similarly to the above home builds, you should repeat the procedure this time using the helper script `resif-load-project-swset-{prod | devel}`.
Don't forget [Project Data Management instructions](../data/project.md#project-directory-modification): to avoid quotas issues, you have to use [`sg`](https://linux.die.net/man/1/sg)

```bash
# BETTER work in a screen or tmux session ;)
$ si[-gpu] [-c <threads>]   # get an interactive job
$ module load tools/EasyBuild
# /!\ IMPORTANT: ensure EASYBUILD_PREFIX is correctly set to [basedir]/<cluster>/<environment>/<arch>
#                and that MODULEPATH is prefixed accordingly
$ resif-load-project-swset-{prod | devel} $PROJECTHOME/<project> # /!\ ADAPT environment and <project> accordingly
$ sg <project> -c "eb -S <softwarename>"   # confirm <filename>.eb == <softwarename>-<v>-<toolchain>.eb
$ sg <project> -c "eb -Dr <filename>.eb"   # check dependencies, normally most MUST be satisfied
$ sg <project> -c "eb -r  <filename>.eb"
```

From that point, the compiled software and associated module is available in the project directoryand can be used by all project members as follows in [launchers](../slurm/launchers.md) etc. -- see [ULHPC launcher Examples](../slurm/launchers.md)

```bash
#!/bin/bash -l # <--- DO NOT FORGET '-l' to facilitate further access to ULHPC modules
#SBATCH -p <partition>
#SBATCH -N 1
#SBATCH --ntasks-per-node <#sockets * s>
#SBATCH --ntasks-per-socket <s>
#SBATCH -c <thread>

print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
# Safeguard for NOT running this launcher on access/login nodes
module purge || print_error_and_exit "No 'module' command"

resif-load-project-swset-prod  $PROJECTHOME/<project> # OR resif-load-project-swset-devel $PROJECTHOME/<project>
module load <softwarename>[/<version>]
[...]
```

## Contribute back to Easybuild

If you developped new easyconfig(s), you are expected to contribute them back to the Easybuilders community!
Consider creating a Pull-Request. You can even do it by command-line assuming you have [setup your Github integration](https://easybuild.readthedocs.io/en/latest/Integration_with_GitHub.html#requirements).  On `iris` or `aion`, you will likely need to install the possibly-insecure, alternate keyrings `keyrings.alt` packages -- see https://pypi.org/project/keyring/


```bash
# checking code style - see https://easybuild.readthedocs.io/en/latest/Code_style.html#code-style
eb --check-contrib <ebfile>
eb --new-pr <ebfile>
```

You can can also consider using the script `PR-create` provided as part of the [RESIF 3](https://github.com/ULHPC/sw) project.

Once the pull request is merged, you can inform the ULHPC team to consider adding the submitted Easyconfig as part of the ULHPC bundles and see it deployed within the next [ULHPC software set release](../environment/modules.md#ulhpc-toolchains-and-software-set-versioning).
