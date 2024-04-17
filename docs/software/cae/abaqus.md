[![](https://images.g2crowd.com/uploads/product/image/large_detail/large_detail_d05e3566f966e83e3ef9753e3aed4086/abaqus.png){: style="width:300px;float: right;" }](https://www.3ds.com/products-services/simulia/products/abaqus/abaquscae/)

The [Abaqus Unified FEA](https://www.3ds.com/products-services/simulia/products/abaqus/abaquscae/)
product suite offers powerful and complete solutions
for both routine and sophisticated engineering problems covering a vast
spectrum of industrial applications. In the automotive industry engineering
work groups are able to consider full vehicle loads, dynamic vibration,
multibody systems, impact/crash, nonlinear static, thermal coupling, and
acoustic-structural coupling using a common model data structure and integrated
solver technology. Best-in-class companies are taking advantage of
Abaqus Unified FEA to consolidate their processes and tools,
reduce costs and inefficiencies, and gain a competitive advantage

## Available versions of Abaqus in ULHPC

To check available versions of Abaqus at ULHPC, type `module spider abaqus`.
It will list the available versions with the following format:
```bash
cae/ABAQUS/<version>[-hotfix-<hotfix>]
```

!!! important "Don't forget to unset `SLURM_GTIDS`"
    You **MUST** unset the SLURM environment variable `SLURM_GTIDS` **for both interactive/GUI and batch jobs**
    ```
    unset SLURM_GTIDS
    ```
    Failure to do so will cause Abaqus to get stuck due to the MPI that Abaqus ships witch is not supporting the SLURM scheduler.

When using a general compute node for Abaqus 2021, please run:

* `abaqus cae -mesa` to launch the GUI without support for hardware-accelerated graphics rendering.
    - the option `-mesa` disables hardware-accelerated graphics rendering within Abaqus’s GUI.
* For a Non-Graphical execution, use
  ```
  abaqus job=<my_job_name> input=<filename>.inp mp_mode=<mode> cpus=<cores> [gpus=<gpus>] scratch=$SCRATCH memory="<mem>gb"
  ```


## Supported parallel mode

Abaqus has two parallelization options which are mutually exclusive:

* __MPI__ (`mp_mode=mpi`), which is generally preferred since this allows for scaling the job to multiple compute nodes. As for MPI jobs, use `-N <nodes> --ntasks-per-node <cores> -c1` upon submission to use:

         abaqus mp_mode=mpi cpu=$SLURM_NTASKS [...]

* __Shared memory / Threads__ (`mp_mode=threads`) for single node / multi-threaded executions. Typically use `-N1 --ntasks-per-node 1 -c <threads>` upon submission to use:

        abaqus mp_mode=threads cpus=${SLURM_CPUS_PER_TASK} [...]

*  __Shared memory for single node with GPU(s)__ / multi-threaded executions (`mp_mode=threads`).  Typically use `-N1 -G 1 --ntasks-per-node 1 -c <threads>` upon submission **on a GPU node** to use:

        abaqus mp_mode=threads cpus=${SLURM_CPUS_PER_TASK} gpus=${SLURM_GPUS} [...]


## Abaqus example problems

Abaqus contains a large number of example problems which can be used to become familiar with Abaqus on the system. These example problems are described in the [Abaqus documentation](https://abaqus-docs.mit.edu/2017/English/SIMACAEEXCRefMap/simaexc-c-fetchproc.htm) and can be obtained using the `abaqus fetch jobs=<name>` command.

!!! example ""
    For example, after loading the Abaqus module `cae/ABAQUS`, enter the following at the command line to extract the input file for test problem s4d:
    ```
    abaqus fetch job=s4d
    ```
    This will extract the input file `s4d.inp`
    See also [Abaqus performance data](https://www.3ds.com/support/hardware-and-software/simulia-system-information/abaqus-69/performance-data/).


## Interactive mode
To open an Abaqus in the interactive mode, please follow the following steps:

(_eventually_) [connect](../../connect/access.md) to the ULHPC login node with the `-X` (or `-Y`) option:

=== "Iris"
    ```bash
    ssh -X iris-cluster   # OR on Mac OS: ssh -Y iris-cluster
    ```
=== "Aion"
    ```bash
    ssh -X aion-cluster   # OR on Mac OS: ssh -Y aion-cluster
    ```

Then you can reserve an [interactive job](../../jobs/interactive.md), for instance with 8 MPI processes. **Don't forget to use the `--x11` option if you intend to use the GUI**.

```bash
$ si --x11 -c 8               # Abaqus mp_mode=threads test
# OR
$ si --x11 --ntask-per-node 8 # abaqus mp_mode=mpi test

# Load the module ABAQUS and needed environment
(node)$ module purge
(node)$ module load cae/ABAQUS
(node)$ unset SLURM_GTIDS   # MANDATORY

# /!\ IMPORTANT: You MUST ADAPT the LM_LICENSE_FILE variable to point to YOUR licence server!!!
(node)$ export LM_LICENSE_FILE=xyz

# Check License server token available
(node)$ abaqus licensing lmstat -a
abaqus licensing lmstat -a
lmutil - Copyright (c) 1989-2019 Flexera. All Rights Reserved.
Flexible License Manager status on Wed 4/13/2022 22:39
[...]
```

### Non-graphical Abaqus

Then the general format to run your Non-Graphical multithreaded interactive execution:

=== "Shared Memory (`-c <threads>`)"
    Assuming a job submitted with `{sbatch|srun|si...} -N1 -c <threads>`:
    ```bash
    # /!\ ADAPT $INPUTFILE accordingly
    abaqus job="${SLURM_JOB_NAME}" verbose=2 interactive \
        input=${INPUTFILE} \
        cpus=${SLURM_CPUS_PER_TASK} mp_mode=threads
    ```

=== "Distributed Memory (MPI)"
    Assuming a job submitted with `{sbatch|srun|si...} -N <N> --ntasks-per-node <npn> -c 1`:
    ```bash
    # /!\ ADAPT $INPUTFILE accordingly
    abaqus job="${SLURM_JOB_NAME}" verbose=2 interactive \
        input=${INPUTFILE} \
        cpus=${SLURM_NTASKS} mp_mode=mpi
    ```

### GUI

If you want to run the GUI, use: `abaqus cae -mesa`

??? info "License information"
    Assuming you have set the variable `LM_LICENSE_FILE` to point to **YOUR** licence server, you can
    check the available license and group you belongs to with:
    ```
    abaqus licensing lmstat -a
    ```
    **If**  your server is hosted outside the ULHPC network, you will have to contact the HPC team to adapt the network firewalls to allow the connection towards your license server.

Use the following options for simulation to stop and resume it:
```bash
# /!\ ADAPT <jobname> accordingly:
abaqus job=<jobname> suspend
abaqus job=<jobname> resume
```

## Batch mode

=== "Shared memory (mp_mode=threads)"
    ```bash
    #!/bin/bash -l                # <--- DO NOT FORGET '-l'
    #SBATCH -J <jobname>
    #SBATCH -N 1
    #SBATCH --ntasks-per-node=1
    #SBATCH -c 4                  # /!\ ADAPT accordingly
    #SBATCH --time=0-03:00:00
    #SBATCH -p batch

    print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
    module purge || print_error_and_exit "No 'module' command"
    module load cae/ABAQUS
    # export LM_LICENSE_FILE=[...]
    unset SLURM_GTIDS

    INPUTFILE=s4d.inp
    [ ! -f "${INPUTFILE}" ] && print_error_and_exit "Unable to find input file ${INPUTFILE}"

    abaqus job="${SLURM_JOB_NAME}" verbose=2 interactive \
        input=${INPUTFILE} cpus=${SLURM_CPUS_PER_TASK} mp_mode=threads
    ```

=== "Distributed memory (mp_mode=mpi)"
    ```bash
    #!/bin/bash -l                # <--- DO NOT FORGET '-l'
    #SBATCH -J <jobname>
    #SBATCH -N 2
    #SBATCH --ntasks-per-node=8  # /!\ ADAPT accordingly
    #SBATCH -c 1
    #SBATCH --time=0-03:00:00
    #SBATCH -p batch

    print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
    module purge || print_error_and_exit "No 'module' command"
    module load cae/ABAQUS
    # export LM_LICENSE_FILE=[...]
    unset SLURM_GTIDS

    INPUTFILE=s4d.inp
    [ ! -f "${INPUTFILE}" ] && print_error_and_exit "Unable to find input file ${INPUTFILE}"

    abaqus job="${SLURM_JOB_NAME}" verbose=2 interactive \
        input=${INPUTFILE} cpus=${SLURM_NTASKS} mp_mode=mpi
    ```

=== "Shared memory with GPU"
    **May not be supported depending on the software set**
    ```bash
    #!/bin/bash -l                # <--- DO NOT FORGET '-l'
    #SBATCH -J <jobname>
    #SBATCH -N 1
    #SBATCH --ntasks-per-node=1
    #SBATCH -c 7
    #SBATCH -G 1
    #SBATCH --time=0-03:00:00
    #SBATCH -p gpu

    print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
    module purge || print_error_and_exit "No 'module' command"
    module load cae/ABAQUS
    # export LM_LICENSE_FILE=[...]
    unset SLURM_GTIDS

    INPUTFILE=s4d.inp
    [ ! -f "${INPUTFILE}" ] && print_error_and_exit "Unable to find input file ${INPUTFILE}"

    abaqus job="${SLURM_JOB_NAME}" verbose=2 interactive \
        input=${INPUTFILE} cpus=${SLURM_CPUS_PER_TASK} gpus=${SLURM_GPUS} mp_mode=threads
    ```



## Additional information
To know more about Abaqus documentation and tutorial,
please refer [Abaqus CAE](http://130.149.89.49:2080/v6.11/pdf_books/CAE.pdf)

??? Tutorial
     * http://www.franc3d.com/wp-content/uploads/2012/05/FRANC3D_V7_ABAQUS_Tutorial.pdf
     * https://sig.ias.edu/files/Abaqus%20tutorial.pdf
     * https://sites.engineering.ucsb.edu/~tshugar/GET_STARTED.pdf?fbclid=IwAR2MQTzCTISqdPuM4D3PiDwXk9oVTBqZWXJUvMccVPYsd1kKPwPOZcnq078


!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
