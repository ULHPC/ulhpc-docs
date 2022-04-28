
[![](http://www.stata.com/includes/images/stata-fb.jpg){: style="width:300px;float: right;" }](https://www.stata.com//)


[Stata](https://www.stata.com/) is a commercial statistical package, which provides a complete solution for data analysis, data management, and graphics.

The University of Luxembourg contributes to a campus-wide license -- see SIU / Service Now [Knowledge Base ticket on Stata MP2](https://service.uni.lu/sp?id=kb_article&sysparm_article=KB0010885)


## Available versions of Stata on ULHPC platforms

To check available versions of Stata at ULHPC, type `module spider stata`.

```bash
math/Stata/<version>
```

Once loaded, the modules brings to you the following binaries:

| Binary      | Description                                                                                                                                   |
|-------------|----------------------------------------------------------------------------------------------------------------------------------------------- |
| `stata`     | Non-graphical standard Stata/IC. For better performance and support for larger databases, `stata-se` should be used.                          |
| `stata-se`  | Non-graphical Stata/SE designed for large databases. Can be used to run tasks automatically with the batch flag `-b` and a Stata '`*.do` file |
| `xstata`    | Graphical standard Stata/IC. For better performance and support for larger databases, xstata-se should be used.                               |
| `xstata-se` | Graphical Stata/SE designed for large databases. Can be used interactively in a similar working environment to Windows and Mac versions.      |

## Interactive Mode

To open a Stata session in [interactive](../../jobs/interactive.md) mode, please follow the following steps:

(_eventually_) [connect](../../connect/access.md) to the ULHPC login node with the `-X` (or `-Y`) option:

=== "Iris"
    ```bash
    ssh -X iris-cluster   # OR on Mac OS: ssh -Y iris-cluster
    ```
=== "Aion"
    ```bash
    ssh -X aion-cluster   # OR on Mac OS: ssh -Y aion-cluster
    ```

Then you can reserve an [interactive job](../../jobs/interactive.md), for instance with 2 cores. **Don't forget to use the `--x11` option if you intend to use the GUI**.

```bash
$ si --x11 -c2      # You CANNOT use more than 2 cores

# Load the module Stata and needed environment
(node)$ module purge
(node)$ module load math/Stata

# Non-Graphical version (CLI)
(node)$ stata
  ___  ____  ____  ____  ____ ®
 /__    /   ____/   /   ____/      17.0
___/   /   /___/   /   /___/       BE—Basic Edition

 Statistics and Data Science       Copyright 1985-2021 StataCorp LLC
                                   StataCorp
                                   4905 Lakeway Drive
                                   College Station, Texas 77845 USA
                                   800-STATA-PC        https://www.stata.com
                                   979-696-4600        stata@stata.com

Stata license: Unlimited-user network, expiring 31 Dec 2022
Serial number: <serial>
  Licensed to: University of Luxembourg
               Campus License - see KB0010885 (Service Now)

.
# To quit Stata
. exit, clear

# To run the GUI version, over X11
(node)$ stata &
```

## Location of your ado files

Run the `sysdir` command to see the search path for ado files:

```
. sysdir
   STATA:  /opt/apps/resif/<cluster>/<version>/<arch>/software/Stata/<stataversion>/
    BASE:  /opt/apps/resif/<cluster>/<version>/<arch>/software/Stata/<stataversion>/ado/base/
    SITE:  /opt/apps/resif/<cluster>/<version>/<arch>/software/Stata/<stataversion>/software/Stata/ado/
    PLUS:  ~/ado/plus/
PERSONAL:  ~/ado/personal/
```

You should thus store ado files in `$HOME/ado/personal. For more see this document.

## Batch mode

To run Stata in batch mode, you need to create do-files which contain the series of commands you would like to run.
With a do file (`filename.do`) in hand, you can run it from the shell in the command line with:

```
stata -b do filename.do
```

With the `-b` flag, outputs will be automatically saved to the outputfile `filename.log`.

=== "Serial Stata"
    ```bash
    #!/bin/bash -l
    #SBATCH -J Stata
    ###SBATCH -A <project_name>
    #SBATCH --ntasks-per-node 1
    #SBATCH -c 1
    #SBATCH --time=00:30:00
    #SBATCH -p batch

    # Load the module Stata
    module purge
    module load math/Stata

    srun stata -b do INPUTFILE.do
    ```

=== "Parallel Stata (Stata/MP)"
    ```bash
    #!/bin/bash -l
    #SBATCH -J Stata
    ###SBATCH -A <project_name>
    #SBATCH --ntasks-per-node 1
    #SBATCH -c 2
    #SBATCH --time=00:30:00
    #SBATCH -p batch

    # Load the module Stata
    module purge
    module load math/Stata

    # Use stata-mp to run across multiple cores
    srun -c $SLURM_CPUS_PER_TASK stata-mp -b do INPUTFILE.do
    ```


## Running Stata in Parallel

### Stata/MP

You can use [Stata/MP](https://www.stata.com/statamp/) to advantage of the advanced multiprocessing capabilities of Stata/MP.
Stata/MP provides the most extensive multicore support of any statistics and data management package.

Note however that **the current license limits the maximum number of cores (to 2 !)**.
Example of interactive usage:

```bash
$ si --x11 -c2      # You CANNOT use more than 2 cores

# Load the module Stata and needed environment
(node)$ module purge
(node)$ module load math/Stata

# Non-Graphical version (CLI)
(node)$ stata-mp

  ___  ____  ____  ____  ____ ®
 /__    /   ____/   /   ____/      17.0
___/   /   /___/   /   /___/       MP—Parallel Edition

 Statistics and Data Science       Copyright 1985-2021 StataCorp LLC
                                   StataCorp
                                   4905 Lakeway Drive
                                   College Station, Texas 77845 USA
                                   800-STATA-PC        https://www.stata.com
                                   979-696-4600        stata@stata.com

Stata license: Unlimited-user 2-core network, expiring 31 Dec 2022
Serial number: <serial>
  Licensed to: University of Luxembourg
               Campus License - see KB0010885 (Service Now)
. set processors 2     # or use env SLURM_CPU_PER_TASKS
. [...]
. exit, clear
```

Note that using the `stata-mp` executable, Stata will automatically use the requested number of cores from Slurm's `--cpus-per-task` option.
This implicit parallelism does not require any changes to your code.



### User-packages parallel and gtools

User-developed Stata packages can be installed from a login node using one of the Stata commands

      net install <package>

These packages will be installed in your home directory by default.

Among others, the [`parallel`](https://github.com/gvegayon/parallel) package implements parallel for loops.
Also, the [`gtools`]( https://github.com/mcaceresb/stata-gtools) provides faster alternatives to some Stata commands when working with big data.

```bash
(node)$ stata
# installation
. net install parallel, from(https://raw.github.com/gvegayon/parallel/stable/) replace
checking parallel consistency and verifying not already installed...
installing into /home/users/svarrette/ado/plus/...
installation complete.

# update index of the installed packages
. mata mata mlib index
.mlib libraries to be searched are now
    lmatabase;lmatasvy;lmatabma;lmatapath;lmatatab;lmatanumlib;lmatacollect;lmatafc;lmatapss;lmat
> asem;lmatamixlog;lmatamcmc;lmatasp;lmatameta;lmataopt;lmataado;lmatagsem;lmatami;lmatapostest;l
> matalasso;lmataerm;lparallel

# initial - ADAPT with SLURM_CPU_PER_TASKS
. parallel initialize 4, f   # Or (better) find a way to use env SLURM_CPU_PER_TASKS
N Child processes: 4
Stata dir:  /mnt/irisgpfs/apps/resif/iris/2020b/broadwell/software/Stata/17/stata

. sysuse auto
(1978 automobile data)

. parallel, by(foreign): egen maxp = max(price)
Small workload/num groups. Temporarily setting number of child processes to 2
--------------------------------------------------------------------------------
Parallel Computing with Stata
Child processes: 2
pll_id         : bcrpvqtoi1
Running at     : /mnt/irisgpfs/users/svarrette
Randtype       : datetime

Waiting for the child processes to finish...
child process 0002 has exited without error...
child process 0001 has exited without error...
--------------------------------------------------------------------------------
Enter -parallel printlog #- to checkout logfiles.
--------------------------------------------------------------------------------

. tab maxp

       maxp |      Freq.     Percent        Cum.
------------+-----------------------------------
      12990 |         22       29.73       29.73
      15906 |         52       70.27      100.00
------------+-----------------------------------
      Total |         74      100.00

. exit, clear
```
