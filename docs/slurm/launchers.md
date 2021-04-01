# Slurm Launcher Examples

[:fontawesome-solid-sign-in-alt:  ULHPC Tutorial / Getting Started](https://ulhpc-tutorials.readthedocs.io/en/latest/beginners/){: .md-button .md-button--link }
[:fontawesome-solid-sign-in-alt:  ULHPC Tutorial / OpenMP/MPI ](https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/basics/){: .md-button .md-button--link }


When setting your default `#SBATCH` directive, always keep in mind your expected _default_ resource allocation that would permit to submit your launchers

1. without options `sbatch <launcher>` (you will be glad in a couple of month not to have to remember the options you need to pass) and
2. try to stick to a single node (to avoid to accidentally induce a huge submission).

## Resource allocation Guidelines

!!! important "General guidelines"
    Always try to align resource specifications for your jobs with physical characteristics.
    Always prefer the use of `--ntasks-per-{node,socket}` over `-n` when defining your tasks allocation request to automatically scale appropriately upon multi-nodes submission with for instance `sbatch -N 2 <launcher>`. Launcher template:
    ```bash
    #!/bin/bash -l # <--- DO NOT FORGET '-l' to facilitate further access to ULHPC modules
    #SBATCH -p <partition>                     #SBATCH -p <partition>
    #SBATCH -N 1                               #SBATCH -N 1
    #SBATCH --ntasks-per-node=<n>              #SBATCH --ntasks-per-node <#sockets * s>
    #SBATCH -c <thread>                        #SBATCH --ntasks-per-socket <s>
                                               #SBATCH -c <thread>
    ```
    This would define by default a **total** of `<n>` (left) or $\#sockets \times$`<s>` (right) **tasks per node**, each on `<thread>` **threads**.
    You **MUST** ensure that either:

    * `<n>`$\times$`<thread>` matches the number of cores avaiable on the target
    computing node (left), or
    * `<n>`=$\#sockets \times$`<s>`, and `<s>`$\times$`<thread>` matches the
    number of cores _per socket_ available on the target computing node (right).

    See [Specific Resource Allocation](index.md#specific-resource-allocation)


{%
   include-markdown "../slurm/index.md"
   start="<!--table-feature-start-->"
   end="<!--table-feature-end-->"
%}

=== "Aion (default Dual-CPU)"
    64 cores per socket and 2 sockets (physical CPUs) per `aion` node. Examples:
    ```bash
    #SBATCH -p batch                 #SBATCH -p batch                #SBATCH -p batch
    #SBATCH -N 1                     #SBATCH -N 1                    #SBATCH -N 1
    #SBATCH --ntasks-per-node=128    #SBATCH --ntasks-per-node 16    #SBATCH --ntasks-per-node 4
    #SBATCH --ntasks-per-socket 64   #SBATCH --ntasks-per-socket 8   #SBATCH --ntasks-per-socket 2
    #SBATCH -c 1                     #SBATCH -c 8                    #SBATCH -c 32
    ```

=== "Iris (default Dual-CPU)"
    14 cores per socket and 2 sockets (physical CPUs) per _regular_ `iris`. Examples:
    ```bash
    #SBATCH -p batch                #SBATCH -p batch                 #SBATCH -p batch
    #SBATCH -N 1                    #SBATCH -N 1                     #SBATCH -N 1
    #SBATCH --ntasks-per-node=28    #SBATCH --ntasks-per-node 14     #SBATCH --ntasks-per-node 4
    #SBATCH --ntasks-per-socket=14  #SBATCH --ntasks-per-socket 7    #SBATCH --ntasks-per-socket 2
    #SBATCH -c 1                    #SBATCH -c 2                     #SBATCH -c 7
    ```

=== "Iris (GPU)"
    14 cores per socket and 2 sockets (physical CPUs) per _gpu_ `iris`, 4 GPU accelerator cards per node.
    You probably want to dedicate 1 task and $\frac{1}{4}$ of the available cores to the management of each GPU accelerator. Examples:
    ```bash
    #SBATCH -p gpu                  #SBATCH -p gpu                   #SBATCH -p gpu
    #SBATCH -N 1                    #SBATCH -N 1                     #SBATCH -N 1
    #SBATCH --ntasks-per-node=1     #SBATCH --ntasks-per-node 2      #SBATCH --ntasks-per-node 4
    #SBATCH -c 7                    #SBATCH --ntasks-per-socket 1    #SBATCH --ntasks-per-socket 2
    #SBATCH -G 1                    #SBATCH -c 7                     #SBATCH -c 7
                                    #SBATCH -G 2                     #SBATCH -G 4
    ```

=== "Iris (Large-Memory)"
    28 cores per socket and 4 sockets (physical CPUs) per _bigmem_ `iris`
    node. Examples:
    ```bash
    #SBATCH -p bigmem              #SBATCH -p bigmem                 #SBATCH -p bigmem
    #SBATCH -N 1                   #SBATCH -N 1                      #SBATCH -N 1
    #SBATCH --ntasks-per-node=4    #SBATCH --ntasks-per-node 8       #SBATCH --ntasks-per-node 16
    #SBATCH --ntasks-per-socket=1  #SBATCH --ntasks-per-socket 2     #SBATCH --ntasks-per-socket 4
    #SBATCH -c 28                  #SBATCH -c 14                     #SBATCH -c 7
    ```
    You probably want to play with a _single_ task but define the expected memory allocation with `--mem=<size[units]>` (Default units are megabytes - Different units can be specified using the suffix `[K|M|G|T]`)



## Basic Slurm Launcher Examples

=== "Single core task"
    !!! example "1 task per job (Note: prefer GNU Parallel in that case)"
        ```bash
        #!/bin/bash -l                # <--- DO NOT FORGET '-l'
        ### Request a single task using one core on one node for 5 minutes in the batch queue
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=1
        #SBATCH -c 1
        #SBATCH --time=0-00:05:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        # Safeguard for NOT running this launcher on access/login nodes
        module purge || print_error_and_exit "No 'module' command"
        # List modules required for execution of the task
        module load <...>
        # [...]
        ```

=== "Multiple Single core tasks"
    !!! example "28 single-core tasks per job"
        ```bash
        #!/bin/bash -l
        ### Request as many tasks as cores available on a single node for 3 hours
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=28  # On iris; for aion, use --ntasks-per-node=128
        #SBATCH -c 1
        #SBATCH --time=0-03:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load <...>
        # [...]
        ```

=== "Multithreaded parallel tasks"
    !!! example "7 multithreaded tasks per job (4 threads each)"
        ```bash
        #!/bin/bash -l
        ### Request as many tasks as cores available on a single node for 3 hours
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=7  # On iris; for aion, use --ntasks-per-node=32
        #SBATCH -c 4
        #SBATCH --time=0-03:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load <...>
        # [...]
        ```

### Specialized BigData/GPU launchers

=== "BigData/[Large-]memory single-core tasks"
    !!! example "1 large-memory single-core task per job"
        ```bash
        #!/bin/bash -l
        ### Request one sequential task requiring half the memory of a regular iris node for 1 day
        #SBATCH -J MyLargeMemorySequentialJob       # Job name
        #SBATCH --mail-user=Your.Email@Address.lu   # mail me ...
        #SBATCH --mail-type=end,fail                # ... upon end or failure
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=1
        #SBATCH -c 1
        #SBATCH --mem=64GB         # if above 112GB: consider bigmem partition (USE WITH CAUTION)
        #SBATCH --time=1-00:00:00
        #SBATCH -p batch           # if above 112GB: consider bigmem partition (USE WITH CAUTION)

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load <...>
        # [...]
        ```

=== "AI/DL task  tasks"
    !!! example "1 ML/DL GPU task"
        ```bash
        #!/bin/bash -l
        ### Request one GPU tasks for 4 hours - dedicate 1/4 of available cores for its management
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=1
        #SBATCH -c 7
        #SBATCH -G 1
        #SBATCH --time=00:04:00
        #SBATCH -p gpu

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        # You probably want to use more recent gpu/CUDA-optimized software builds
        module use /opt/apps/resif/iris/2019b/gpu/modules
        module load <...>

        # This should report a single GPU (over 4 available per gpu node)
        nvidia-smi
        # [...]
        ```

## Serial Task script Launcher

=== "Serial Killer (Generic template)"
    !!! example ""
        ```bash
        #!/bin/bash -l     # <--- DO NOT FORGET '-l'
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=1
        #SBATCH -c 1
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        # C/C++: module load toolchain/intel # OR: module load toolchain/foss
        # Java:  module load lang/Java/1.8
        # Ruby/Perl/Rust...:  module load lang/{Ruby,Perl,Rust...}
        # /!\ ADAPT TASK variable accordingly - absolute path to the (serial) task to be executed
        TASK=${TASK:=${HOME}/bin/app.exe}
        OPTS=$*

        ${TASK} ${OPTS}
        ```

=== "Serial Python"
    !!! example ""
        ```bash
        #!/bin/bash -l
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=1
        #SBATCH -c 1
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        # Python 3.X by default (also on system)
        module load lang/Python
        # module load lang/SciPy-bundle
        # and/or: activate the virtualenv <name> you previously generated with
        #     python -m venv <name>
        source ./<name>/bin/activate
        OPTS=$*

        python [...] ${OPTS}
        ```

=== "R"
    !!! example ""
        ```bash
        #!/bin/bash -l
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=1
        #SBATCH -c 28
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load lang/R
        export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
        OPTS=$*

        Rscript <script>.R ${OPTS}  |& tee job_${SLURM_JOB_NAME}.out
        ```

=== "Matlab"
    ... but why? just use Python or R.

    !!! example ""
        ```bash
        #!/bin/bash -l
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=1
        #SBATCH -c 28
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load math/MATLAB

        matlab -nodisplay -nosplash < INPUTFILE.m > OUTPUTFILE.out
        ```

## pthreads/OpenMP Launcher

=== "Aion (default Dual-CPU)"
    !!! example "Single node, threaded (pthreads/OpenMP) application launcher"
        ```bash
        #!/bin/bash -l
        # Single node, threaded (pthreads/OpenMP) application launcher, using all 128 cores of an aion cluster node
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=1
        #SBATCH -c 128
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/foss

        export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
        OPTS=$*

        srun /path/to/your/threaded.app ${OPTS}
        ```

=== "Iris (default Dual-CPU)"
    !!! example "Single node, threaded (pthreads/OpenMP) application launcher"
        ```bash
        #!/bin/bash -l
        # Single node, threaded (pthreads/OpenMP) application launcher, using all 28 cores of an iris cluster node:
        #SBATCH -N 1
        #SBATCH --ntasks-per-node=1
        #SBATCH -c 28
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/foss

        export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
        OPTS=$*

        srun /path/to/your/threaded.app ${OPTS}
        ```

## MPI

### Intel MPI Launchers

!!! tips ""
    Official Slurm [guide for Intel MPI](https://slurm.schedmd.com/mpi_guide.html#intel_mpi)

=== "Aion (default Dual-CPU)"
    !!! example "Multi-node parallel application IntelMPI launcher"
        ```bash
        #!/bin/bash -l
        # Multi-node parallel application IntelMPI launcher, using 256 MPI processes

        #SBATCH -N 2
        #SBATCH --ntasks-per-node 128    # MPI processes per node
        #SBATCH -c 1
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/intel
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/intel-toolchain-compiled-application ${OPTS}
        ```

=== "Iris (default Dual-CPU)"
    !!! example "Multi-node parallel application IntelMPI launcher"
        ```bash
        #!/bin/bash -l
        # Multi-node parallel application IntelMPI launcher, using 56 MPI processes

        #SBATCH -N 2
        #SBATCH --ntasks-per-node 28    # MPI processes per node
        #SBATCH -c 1
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/intel
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/intel-toolchain-compiled-application ${OPTS}
        ```


### OpenMPI Slurm Launchers { .t }

!!! tips ""
    Official Slurm [guide for Open MPI](https://slurm.schedmd.com/mpi_guide.html#open_mpi)

=== "Aion (default Dual-CPU)"
    !!! example "Multi-node parallel application OpenMPI launcher"
        ```bash
        #!/bin/bash -l
        # Multi-node parallel application OpenMPI launcher, using 256 MPI processes

        #SBATCH -N 2
        #SBATCH --ntasks-per-node 128    # MPI processes per node
        #SBATCH -c 1
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/foss
        module load mpi/OpenMPI
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/foss-toolchain-openMPIcompiled-application ${OPTS}
        ```

=== "Iris (default Dual-CPU)"
    !!! example "Multi-node parallel application OpenMPI launcher"
        ```bash
        #!/bin/bash -l
        # Multi-node parallel application OpenMPI launcher, using 56 MPI processes

        #SBATCH -N 2
        #SBATCH --ntasks-per-node 28    # MPI processes per node
        #SBATCH -c 1
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/foss
        module load mpi/OpenMPI
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/foss-toolchain-openMPIcompiled-application ${OPTS}
        ```

## Hybrid Intel MPI+OpenMP Launcher

=== "Aion (default Dual-CPU)"
    !!! example "Multi-node hybrid parallel application IntelMPI/OpenMP launcher"
        ```bash
        #!/bin/bash -l
        # Multi-node hybrid application IntelMPI+OpenMP launcher, using 64 threads per socket(CPU) on 2 nodes (256 cores):

        #SBATCH -N 2
        #SBATCH --ntasks-per-node   2    # MPI processes per node
        #SBATCH --ntasks-per-socket 1    # MPI processes per processor
        #SBATCH -c 64
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/intel
        export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/parallel-hybrid-app ${OPTS}
        ```

=== "Iris (default Dual-CPU)"
    !!! example "Multi-node hybrid parallel application IntelMPI/OpenMP launcher"
        ```bash
        #!/bin/bash -l
        # Multi-node hybrid application IntelMPI+OpenMP launcher, using 14 threads per socket(CPU) on 2 nodes (56 cores):

        #SBATCH -N 2
        #SBATCH --ntasks-per-node   2    # MPI processes per node
        #SBATCH --ntasks-per-socket 1    # MPI processes per processor
        #SBATCH -c 14
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/intel
        export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/parallel-hybrid-app ${OPTS}
        ```

## Hybrid OpenMPI+OpenMP Launcher

=== "Aion (default Dual-CPU)"
    !!! example "Multi-node hybrid parallel application OpenMPI/OpenMP launcher"
        ```bash
        #!/bin/bash -l
        # Multi-node hybrid application OpenMPI+OpenMP launcher, using 64 threads per socket(CPU) on 2 nodes (256 cores):

        #SBATCH -N 2
        #SBATCH --ntasks-per-node   2    # MPI processes per node
        #SBATCH --ntasks-per-socket 1    # MPI processes per processor
        #SBATCH -c 64
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/foss
        module load mpi/OpenMPI
        export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/parallel-hybrid-app ${OPTS}
        ```

=== "Iris (default Dual-CPU)"
    !!! example "Multi-node hybrid parallel application OpenMPI/OpenMP launcher"
        ```bash
        #!/bin/bash -l
        # Multi-node hybrid application OpenMPI+OpenMP launcher, using 14 threads per socket(CPU) on 2 nodes (56 cores):

        #SBATCH -N 2
        #SBATCH --ntasks-per-node   2    # MPI processes per node
        #SBATCH --ntasks-per-socket 1    # MPI processes per processor
        #SBATCH -c 14
        #SBATCH --time=0-01:00:00
        #SBATCH -p batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/foss
        module load mpi/OpenMPI
        export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/parallel-hybrid-app ${OPTS}
        ```
