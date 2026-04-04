# Slurm Launcher Examples

[:fontawesome-solid-right-to-bracket:  ULHPC Tutorial / Getting Started](https://ulhpc-tutorials.readthedocs.io/en/latest/beginners/){: .md-button .md-button--link }
[:fontawesome-solid-right-to-bracket:  ULHPC Tutorial / OpenMP/MPI ](https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/basics/){: .md-button .md-button--link }


When setting your default `#SBATCH` directive, always keep in mind your expected _default_ resource allocation that would permit to submit your launchers

1. without options `sbatch <launcher>` (you will be glad in a couple of month not to have to remember the options you need to pass) and
1. try to stick to a single node (to avoid to accidentally induce a huge submission).

## Resource allocation Guidelines

!!! important "General guidelines"
    Always try to align [resource specifications](index.md#specific-resource-allocation) for your jobs with physical characteristics. Always prefer the use of `--ntasks-per-{node,socket}` over `-n` when defining your tasks allocation request to automatically scale appropriately upon multi-nodes submission with for instance `sbatch --nodes=2 <launcher>`. Launcher template:
    ```bash
    #!/bin/bash --login # <--- DO NOT FORGET '--login/-l' to facilitate further access to ULHPC modules
    #SBATCH --partition=<partition>            #SBATCH --partition=<partition>
    #SBATCH --nodes=1                          #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=<n>              #SBATCH --ntasks-per-node=<#sockets * s>
    #SBATCH --cpus-per-task=<thread>           #SBATCH --ntasks-per-socket=<s>
                                               #SBATCH --cpus-per-task=<thread>
    ```
    This would define by default a **total** of `<n>` (left) or $\#sockets \times$`<s>` (right) **tasks per node**, each on `<thread>` **threads**. You **MUST** ensure that either:

    - `<n>`$\times$`<thread>` matches the number of cores avaiable on the target computing node (left), or
    - `<n>`=$\#sockets \times$`<s>`, and `<s>`$\times$`<thread>` matches the number of cores _per socket_ available on the target computing node (right).

    See [Specific Resource Allocation](index.md#specific-resource-allocation)


{%
   include-markdown "../slurm/index.md"
   start="<!--table-feature-start-->"
   end="<!--table-feature-end-->"
%}

=== "Aion (default Dual-CPU)"
    16 cores per socket and 8 (virtual) sockets (CPUs) per `aion` node. Examples:
    ```bash
    #SBATCH --partition=batch        #SBATCH --partition=batch       #SBATCH --partition=batch
    #SBATCH --nodes=1                #SBATCH --nodes=1               #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=128    #SBATCH --ntasks-per-node=16    #SBATCH --ntasks-per-node=8
    #SBATCH --ntasks-per-socket=16   #SBATCH --ntasks-per-socket=2   #SBATCH --ntasks-per-socket=1
    #SBATCH --cpus-per-task=1        #SBATCH --cpus-per-task=8       SBATCH --cpus-per-task=16
    ```

=== "Iris (default Dual-CPU)"
    14 cores per socket and 2 sockets (physical CPUs) per _regular_ `iris`. Examples:
    ```bash
    #SBATCH --partition=batch       #SBATCH --partition=batch        #SBATCH --partition=batch
    #SBATCH --nodes=1               #SBATCH --nodes=1                #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=28    #SBATCH --ntasks-per-node=14     #SBATCH --ntasks-per-node=4
    #SBATCH --ntasks-per-socket=14  #SBATCH --ntasks-per-socket=7    #SBATCH --ntasks-per-socket=2
    #SBATCH --cpus-per-task=1       #SBATCH --cpus-per-task=2        #SBATCH --cpus-per-task=7
    ```

=== "Iris (GPU)"
    14 cores per socket and 2 sockets (physical CPUs) per _gpu_ `iris`, 4 GPU accelerator cards per node. You probably want to dedicate 1 task and $\frac{1}{4}$ of the available cores to the management of each GPU accelerator. Examples:
    ```bash
    #SBATCH --partition=gpu         #SBATCH --partition=gpu          #SBATCH --partition=gpu
    #SBATCH --nodes=1               #SBATCH --nodes=1                #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1     #SBATCH --ntasks-per-node=2      #SBATCH --ntasks-per-node=4
    #SBATCH --cpus-per-task=7       #SBATCH --ntasks-per-socket=1    #SBATCH --ntasks-per-socket=2
    #SBATCH --gpus-per-task=1       #SBATCH --cpus-per-task=7        #SBATCH --cpus-per-task=7
                                    #SBATCH --gpus-per-task=2        #SBATCH --gpus-per-task=4
    ```

=== "Iris (Large-Memory)"
    28 cores per socket and 4 sockets (physical CPUs) per _bigmem_ `iris` node. Examples:
    ```bash
    #SBATCH --partition=bigmem     #SBATCH --partition=bigmem        #SBATCH --partition=bigmem
    #SBATCH --nodes=1              #SBATCH --nodes=1                 #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=4    #SBATCH --ntasks-per-node=8       #SBATCH --ntasks-per-node=16
    #SBATCH --ntasks-per-socket=1  #SBATCH --ntasks-per-socket=2     #SBATCH --ntasks-per-socket=4
    #SBATCH --cpus-per-task=28     #SBATCH --cpus-per-task=14        #SBATCH --cpus-per-task=7
    ```
    You probably want to play with a _single_ task but define the expected memory allocation with `--mem=<size[units]>` (Default units are megabytes - Different units can be specified using the suffix `[K|M|G|T]`)

## Basic Slurm Launcher Examples

=== "Single core task"
    !!! example "1 task per job (Note: prefer GNU Parallel in that case - see below)"
        ```bash
        #!/bin/bash --login                # <--- DO NOT FORGET '-l'
        ### Request a single task using one core on one node for 5 minutes in the batch queue
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=1
        #SBATCH --cpus-per-task=1
        #SBATCH --time=0-00:05:00
        #SBATCH --partition=batch

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
        #!/bin/bash --login
        ### Request as many tasks as cores available on a single node for 3 hours
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=28  # On iris; for aion, use --ntasks-per-node=128
        #SBATCH --cpus-per-task=1
        #SBATCH --time=0-03:00:00
        #SBATCH --partition=batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load <...>
        # [...]
        ```

=== "Multithreaded parallel tasks"
    !!! example "7 multithreaded tasks per job (4 threads each)"
        ```bash
        #!/bin/bash --login
        ### Request as many tasks as cores available on a single node for 3 hours
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=7  # On iris; for aion, use --ntasks-per-node=32
        #SBATCH --cpus-per-task=4
        #SBATCH --time=0-03:00:00
        #SBATCH --partition=batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load <...>
        # [...]
        ```

## Embarrassingly Parallel Tasks

![](https://www.gnu.org/software/parallel/logo-gray+black300.png){: style="width:150px; float: right;"}

For many users, the reason to consider (or being encouraged) to offload their computing executions on a (remote) HPC or Cloud facility is tied to the limits reached by their computing devices (laptop or workstation). It is generally motivated by time constraints

> "My computations take several hours/days to complete. On an HPC, it will last a few minutes, no?"

or search-space explorations:

> "I need to check my application against a huge number of input pieces (files) - it worked on a few of them locally but takes ages for a single check. How to proceed on HPC?"

In most of the cases, your favorite Java application or R/python (custom) development scripts, iterated again over multiple input conditions, are **inherently SERIAL**: they are able to use only one core when executed. You thus deal with what is often call a _Bag of (independent) tasks_, also referred to as **embarrassingly parallel tasks**.

In this case, you **MUST NOT** overload the job scheduler with a large number of small (single-core) jobs. Instead, you should use [GNU Parallel](http://www.gnu.org/software/parallel/) which permits the effective management of such tasks in a way that optimize both the resource allocation and the completion time.

More specifically, [GNU Parallel](http://www.gnu.org/software/parallel/) is a tool for executing tasks in parallel, typically on a single machine. When coupled with the Slurm command srun, `parallel` becomes a powerful way of distributing a set of tasks amongst a number of workers. This is particularly useful when the number of tasks is significantly larger than the number of available workers (i.e. `$SLURM_NTASKS`), and each tasks is independent of the others.

[:fontawesome-solid-right-to-bracket: ULHPC Tutorial: GNU Parallel launcher for Embarrassingly Parallel Jobs](https://ulhpc-tutorials.readthedocs.io/en/latest/sequential/basics/#best-launcher-based-on-gnu-parallel-1-job-1-node-n-tasks){: .md-button .md-button--link }

Luckily, we have prepared a [generic GNU Parallel launcher](https://github.com/ULHPC/tutorials/blob/devel/sequential/basics/scripts/launcher.parallel.sh) that should be straight forward to adapt to your own workflow following [our tutorial](https://ulhpc-tutorials.readthedocs.io/en/latest/sequential/basics/#best-launcher-based-on-gnu-parallel-1-job-1-node-n-tasks):

1. Create a dedicated script `run_<task>` responsible to run your java/R/Python tasks while taking as argument the parameter of each run. You can inspire from [`run_stressme`](https://github.com/ULHPC/tutorials/blob/devel/sequential/basics/scripts/run_stressme) for instance.
  - test it in interactive
2. rename the generic launcher [`launcher.parallel.sh`](https://github.com/ULHPC/tutorials/blob/devel/sequential/basics/scripts/launcher.parallel.sh) to `launcher_<task>.sh`,
  - enable `#SBATCH --dependency=singleton`
  - set the jobname
  - change TASK to point to the **absolute** path to `run_<task>` script
  - set TASKLISTFILE to point to a files with the parameters to pass to your script for each task
  - adapt eventually the `#SBATCH --ntasks-per-node=[...]` and `#SBATCH --cpus-per-task=[...]` to match your needs AND the hardware configs of a single node (28 cores on iris, 128 cores on Aion) -- see [guidelines](#resource-allocation-guidelines)
3. test a batch run -- **stick to a single node** to take the best out of one full node.

## Serial Task script Launcher

=== "Serial Killer (Generic template)"
    !!! example ""
        ```bash
        #!/bin/bash --login     # <--- DO NOT FORGET '--login/-l'
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=1
        #SBATCH --cpus-per-task=1
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        # C/C++: module load toolchain/intel # OR: module load toolchain/foss
        # Java:  module load lang/Java/1.8
        # Ruby/Perl/Rust...:  module load lang/{Ruby,Perl,Rust...}
        # /!\ ADAPT TASK variable accordingly - absolute path to the (serial) task to be executed
        TASK=${TASK:=${HOME}/bin/app.exe}
        OPTS=$*

        srun ${TASK} ${OPTS}
        ```

=== "Serial Python"
    !!! example ""
        ```bash
        #!/bin/bash --login
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=1
        #SBATCH --cpus-per-task=1
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        # Python 3.X by default (also on system)
        module load lang/Python
        # module load lang/SciPy-bundle
        # and/or: activate the virtualenv <name> you previously generated with
        #     python -m venv <name>
        source ./<name>/bin/activate
        OPTS=$*

        srun python [...] ${OPTS}
        ```

=== "R"
    !!! example ""
        ```bash
        #!/bin/bash --login
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=1
        #SBATCH --cpus-per-task=28
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load lang/R
        export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
        OPTS=$*

        srun Rscript <script>.R ${OPTS}  |& tee job_${SLURM_JOB_NAME}.out
        ```

=== "Matlab"
    ... but why? just use Python or R.

    !!! example ""
        ```bash
        #!/bin/bash --login
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=1
        #SBATCH --cpus-per-task=28
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load math/MATLAB

        matlab -nodisplay -nosplash < INPUTFILE.m > OUTPUTFILE.out
        ```

## Specialized BigData/GPU launchers

!!! example "BigData/[Large-]memory single-core tasks"
    ```bash
	#!/bin/bash --login
	### Request one sequential task requiring half the memory of a regular iris node for 1 day
	#SBATCH --job-name=MyLargeMemorySequentialJob # Job name
	#SBATCH --mail-user=Your.Email@Address.lu     # mail me ...
	#SBATCH --mail-type=end,fail                  # ... upon end or failure
	#SBATCH --nodes=1
	#SBATCH --ntasks-per-node=1
	#SBATCH --cpus-per-task=1
	#SBATCH --mem=64GB                            # if above 112GB: consider bigmem partition (USE WITH CAUTION)
	#SBATCH --time=1-00:00:00
	#SBATCH --partition=batch                     # if above 112GB: consider bigmem partition (USE WITH CAUTION)

	print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
	module purge || print_error_and_exit "No 'module' command"
	module load <...>
	# [...]
	```

!!! example "AI/DL task  tasks"
    ```bash
	#!/bin/bash --login
	### Request one GPU tasks for 4 hours - dedicate 1/4 of available cores for its management
	#SBATCH --nodes=1
	#SBATCH --ntasks-per-node=1
	#SBATCH --cpus-per-task=7
	#SBATCH --gpus-per-task=1
	#SBATCH --time=04:00:00
	#SBATCH --partition=gpu

	print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
	module purge || print_error_and_exit "No 'module' command"
	module load <...>    # USE apps compiled against the {foss,intel}cuda toolchain !
    # Ex: 
    # module load numlib/cuDNN

	# This should report a single GPU (over 4 available per gpu node)
	nvidia-smi
	# [...]
    srun [...]
	```

## pthreads/OpenMP Launcher

!!! warning "Always set `OMP_NUM_THREADS` to match `${SLURM_CPUS_PER_TASK:-1}`"
    You **MUST** enforce the use of `--cpus-per-task=<threads>` in your launcher to ensure the variable `$SLURM_CPUS_PER_TASK` exists within your launcher scripts. This is the appropriate value to set for [`OMP_NUM_THREAD`](https://www.openmp.org/spec-html/5.0/openmpse50.html), with default to 1 as extra safely which can be obtained with the following affectation:

    ```bash
    export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
    ```

=== "Aion (default Dual-CPU)"
    !!! example "Single node, threaded (pthreads/OpenMP) application launcher"
        ```bash
        #!/bin/bash --login
        # Single node, threaded (pthreads/OpenMP) application launcher, using all 128 cores of an aion cluster node
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=1
        #SBATCH --cpus-per-task=128
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

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
        #!/bin/bash --login
        # Single node, threaded (pthreads/OpenMP) application launcher, using all 28 cores of an iris cluster node:
        #SBATCH --nodes=1
        #SBATCH --ntasks-per-node=1
        #SBATCH --cpus-per-task=28
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

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
        #!/bin/bash --login
        # Multi-node parallel application IntelMPI launcher, using 256 MPI processes

        #SBATCH --nodes=2
        #SBATCH --ntasks-per-node=128    # MPI processes per node
        #SBATCH --cpus-per-task=1
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/intel
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/intel-toolchain-compiled-application ${OPTS}
        ```
        Recall to use [`si-bigmem`](../jobs/interactive.md) to request an [interactive](../jobs/interactive.md) job when testing your script. 

=== "Iris (default Dual-CPU)"
    !!! example "Multi-node parallel application IntelMPI launcher"
        ```bash
        #!/bin/bash --login
        # Multi-node parallel application IntelMPI launcher, using 56 MPI processes

        #SBATCH --nodes=2
        #SBATCH --ntasks-per-node=28    # MPI processes per node
        #SBATCH --cpus-per-task=1
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/intel
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/intel-toolchain-compiled-application ${OPTS}
        ```
        Recall to use [`si-gpu`](../jobs/interactive.md) to request an [interactive](../jobs/interactive.md) job when testing your script on a GPU node. 

You may want to use [PMIx](https://pmix.github.io/standard) as MPI initiator -- use `srun --mpi=list` to list the available implementations (default: pmi2), and `srun --mpi=pmix[_v3] [...]` to use PMIx.

### OpenMPI Slurm Launchers { .t }

!!! tips ""
    Official Slurm [guide for Open MPI](https://slurm.schedmd.com/mpi_guide.html#open_mpi)

=== "Aion (default Dual-CPU)"
    !!! example "Multi-node parallel application OpenMPI launcher"
        ```bash
        #!/bin/bash --login
        # Multi-node parallel application OpenMPI launcher, using 256 MPI processes

        #SBATCH --nodes=2
        #SBATCH --ntasks-per-node=128    # MPI processes per node
        #SBATCH --cpus-per-task=1
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

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
        #!/bin/bash --login
        # Multi-node parallel application OpenMPI launcher, using 56 MPI processes

        #SBATCH --nodes=2
        #SBATCH --ntasks-per-node=28    # MPI processes per node
        #SBATCH --cpus-per-task=1
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

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
        #!/bin/bash --login
        # Multi-node hybrid application IntelMPI+OpenMP launcher, using 16 threads per socket(CPU) on 2 nodes (256 cores):

        #SBATCH --nodes=2
        #SBATCH --ntasks-per-node=8   # MPI processes per node
        #SBATCH --ntasks-per-socket=1 # MPI processes per (virtual) processor
        #SBATCH --cpus-per-task=16
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

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
        #!/bin/bash --login
        # Multi-node hybrid application IntelMPI+OpenMP launcher, using 14 threads per socket(CPU) on 2 nodes (56 cores):

        #SBATCH --nodes=2
        #SBATCH --ntasks-per-node=2   # MPI processes per node
        #SBATCH --ntasks-per-socket=1 # MPI processes per processor
        #SBATCH --cpus-per-task=14
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

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
        #!/bin/bash --login
        # Multi-node hybrid application OpenMPI+OpenMP launcher, using 16 threads per socket(CPU) on 2 nodes (256 cores):

        #SBATCH --nodes=2
        #SBATCH --ntasks-per-node=8   # MPI processes per node
        #SBATCH --ntasks-per-socket=1 # MPI processes per processor
        #SBATCH --cpus-per-task=16
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

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
        #!/bin/bash --login
        # Multi-node hybrid application OpenMPI+OpenMP launcher, using 14 threads per socket(CPU) on 2 nodes (56 cores):

        #SBATCH --nodes=2
        #SBATCH --ntasks-per-node=2   # MPI processes per node
        #SBATCH --ntasks-per-socket=1 # MPI processes per processor
        #SBATCH --cpus-per-task=14
        #SBATCH --time=0-01:00:00
        #SBATCH --partition=batch

        print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
        module purge || print_error_and_exit "No 'module' command"
        module load toolchain/foss
        module load mpi/OpenMPI
        export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1}
        OPTS=$*

        srun -n $SLURM_NTASKS /path/to/your/parallel-hybrid-app ${OPTS}
        ```
