[![](https://www.vasp.at/images/logo.png){: style="width:300px;float: right;" }](https://www.vasp.at/)

[VASP](https://www.vasp.at/documentation/) is a package for performing ab initio quantum-mechanical molecular dynamics (MD) using pseudopotentials and a plane wave basis set. The approach implemented in VASP is based on a finite-temperature local-density approximation (with the free energy as variational quantity) and an exact evaluation of the instantaneous electronic ground state at each MD step using efficient matrix diagonalization schemes and an efficient Pulay mixing.

## Accessing VASP in UL HPC clusters

VASP is a proprietary software. If your group has access to VASP, then the UL HPC team can compile the source code and provide your group with a module that is optimally configured for use in our clusters.

All software is installed in the group project directory which is [backed up](/data/backups/#directories-on-the-ulhpc-clusters-infrastructure).
```
${PROJECTHOME}/<project name>/backup/easubuild
```
Add the following to your `bascrc` to access the project modules.
```bash
if command -v module >/dev/null 2>&1 ; then
    module use "${PROJECTHOME}/<project name>/backup/easubuild/${ULHPC_CLUSTER}/2023b/${RESIF_ARCH}/modules/all"
fi
```

After refreshing your environment you can check for the available versions of VASP by typing `module spider vasp`:
```
$ module spider vasp
...
phys/VASP/6.4.3-foss-2023b
...
```

## Working with VASP

VASP support both interactive session with a graphical GUi and batch jobs submitted through a job scheduler.

### Interactive mode

To open VASP in the interactive mode, please follow these steps.

=== "Iris"
    ```bash
    # From your local computer
    $ ssh -X iris-cluster

    # Reserve the node for interactive computation
    $ salloc -p interactive -A <project name> -t 1:00:00 -n 1 -c 14 --x11
    # OR si -A <project name> -t 1:00:00 -n 1 -c 14 --x11 [...]

    # Load the vasp module
    $ module purge
    $ module load phys/VASP/6.4.3-foss-2023b

    $ vasp_[std/gam/ncl]
    ```
=== "Aion"
    ```bash
    # From your local computer
    $ ssh -X iris-cluster

    # Reserve the node for interactive computation
    $ salloc -p interactive -A <project name> -t 1:00:00 -n 1 -c 16 --x11
    # OR si -A <project name> -t 1:00:00 -n 1 -c 16 --x11 [...]

    # Load the vasp module
    $ module purge
    $ module load phys/VASP/6.4.3-foss-2023b

    $ vasp_[std/gam/ncl]
    ```

### Batch mode

VASP jobs can also be executed as batch scripts with the job scheduler. Please execute all large jobs in batch scripts.

When executing very large VASP jobs you should take advantage of OpenMP to reduce the limitations imposed by cache size and memory bandwidth when using multiple MPI processes. According to the VASP documentation, you should

- setup a single process per L3 level cache (`OMP_NUM_THREADS`),
- assign cores to threads so that all threads run on cores that share the same L3 cache (`OMP_PLACES` and `OMP_PROC_BIND`), and
- increase the stack size per OpenMP process to at least `512 Mbytes` to avoid segmentation faults, as VASP is called a significant number of functions per OpenMP process (`OMP_STACKSIZE`).

=== "Aion"
    The [processors of Aion](https://en.wikichip.org/wiki/amd/epyc/7h12) are composed by [Core Complexes (CCX)](https://en.wikichip.org/wiki/amd/microarchitectures/zen_2#Core_Complex), with each CCX having 4 core and an L3 cache where all cores have uniform access. Thus,

    - assign a process per CCX with 4 threads per process by setting the number of `OMP_NUM_THREADS=4`, and
    - bind all threads to the cores where they where assigned with `OMP_PLACES=cores` and `OMP_PROC_BIND=close`.

    ```bash
    #!/usr/bin/bash --login

    #SBATCH --account=<project name>
    #SBATCH --job-name=VASP-casename
    #SBATCH --nodes=2
    #SBATCH --ntasks-per-node=32
    #SBATCH --cpus-per-task=4
    #SBATCH --time=0-08:00:00
    #SBATCH --partition=batch
    #SBATCH --qos=normal

    # Set output and error files
    #SBATCH --error=%x-%j.err
    #SBATCH --output=%x-%j.out

    print_error_and_exit() {
      echo "***ERROR*** $*"
      exit 1
    }

    # Load the vasp module
    module purge || print_error_and_exit "No 'module' command found"
    module load module load phys/VASP/6.4.3-foss-2023b

    export OMP_NUM_THREADS=4

    export OMP_PLACES=cores
    export OMP_PROC_BIND=close

    export OMP_STACKSIZE=512m

    srun vasp_[std/gam/ncl]
    ```

=== "Iris"
    The L3 cache structure of Iris is considerably simpler, with each socket having a [single L3 cache where all cores have uniform access](https://en.wikichip.org/wiki/intel/xeon_e5/e5-2680_v4). Thus,

    - assign a process per socket with 14 threads per process by setting the number of `OMP_NUM_THREADS=14`, and
    - bind all threads to the cores where they where assigned with `OMP_PLACES=cores` and `OMP_PROC_BIND=close`.

    ```bash
    #!/usr/bin/bash --login

    #SBATCH --account=<project name>
    #SBATCH --job-name=VASP-casename
    #SBATCH --nodes=2
    #SBATCH --ntasks-per-node=2
    #SBATCH --cpus-per-task=14
    #SBATCH --time=0-08:00:00
    #SBATCH --partition=batch
    #SBATCH --qos=normal

    # Set output and error files
    #SBATCH --error=%x-%j.err
    #SBATCH --output=%x-%j.out

    print_error_and_exit() {
      echo "***ERROR*** $*"
      exit 1
    }

    # Load the vasp module
    module purge || print_error_and_exit "No 'module' command found"
    module load module load phys/VASP/6.4.3-foss-2023b

    export OMP_NUM_THREADS=14

    export OMP_PLACES=cores
    export OMP_PROC_BIND=close

    export OMP_STACKSIZE=512m

    srun vasp_[std/gam/ncl]
    ```

!!! info "Sources"
    1. [The VASP Manual: Combining MPI and OpenMP](https://www.vasp.at/wiki/index.php/Combining_MPI_and_OpenMP)

## Additional information

To know more information about VASP tutorial and documentation, please refer to [VASP manual](https://www.vasp.at/wiki/index.php/The_VASP_Manual).

!!! tip
    If you find some issues with the instructions above, please report it to us using [support ticket](https://hpc.uni.lu/support).
