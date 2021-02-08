# Slurm Resource and Job Management System

ULHPC uses [Slurm](https://slurm.schedmd.com/) (_Simple Linux Utility for Resource Management_) for cluster/resource management and job scheduling.
This middleware is responsible for allocating resources to users, providing a framework for starting, executing and monitoring work on allocated resources and scheduling work for future execution.

[:fontawesome-solid-sign-in-alt: Official docs](https://slurm.schedmd.com/documentation.html){: .md-button .md-button--link }
[:fontawesome-solid-sign-in-alt: Official FAQ](https://slurm.schedmd.com/faq.html){: .md-button .md-button--link }
[:fontawesome-solid-sign-in-alt: ULHPC Tutorial/Getting Started](https://ulhpc-tutorials.readthedocs.io/en/latest/beginners/){: .md-button .md-button--link }

[![](https://hpc.uni.lu/download/slides/2020-ULHPC-user-guide.png)](https://hpc.uni.lu/download/slides/2020-ULHPC-user-guide.pdf)


## Jobs

A **job** is an allocation of resources such as compute nodes assigned to a user for an certain amount of time.
Jobs can be _interactive_ or _passive_ (e.g., a batch script) scheduled for later execution.

!!! question "What characterize a job?"
    A user _jobs_ have the following key characteristics:

    *  set of requested resources:
         - number of computing resources: **nodes** (including all their CPUs and cores) or **CPUs** (including all their cores) or **cores**
         - amount of **memory**: either per node or per CPU
         -  **(wall)time** needed for the users tasks to complete their work
    * a requested node **partition** (job queue)
    * a requested **quality of service** (QoS) level which grants users specific accesses
    * a requested **account** for accounting purposes

Once a job is assigned a set of nodes, the user is able to initiate parallel work in the form of _job steps_ (sets of tasks) in any configuration within the allocation.

When you login to a ULHPC system you land on a [access/login node](../connect/access.md). Login nodes are only for editing and preparing jobs: They are not meant for actually running jobs.
From the login node you can interact with Slurm to **submit** job scripts or start interactive jobs, which will be further run on the compute nodes.

## Submit Jobs

{%
   include-markdown "commands.md"
   start="<!--submit-start-->"
   end="<!--submit-end-->"
%}

## Specific Resource Allocation

Within a job, you aim at running a certain number of **tasks**, and Slurm allow for a fine-grain control of the resource allocation that must be satisfied for _each_ task.

!!! danger "Beware of Slurm terminology in [Multicore Architecture](https://slurm.schedmd.com/mc_support.html)!"
    ![](images/slurm_mc_support.png){: style="width:350px; float: right;"}

    * __Slurm Node = Physical node__, specified with `-N <#nodes>`
        - _Advice_: always explicit number of expected number of tasks _per node_ using `--ntasks-per-node <n>`. This way you control the node footprint of your job.
    * __Slurm Socket = Physical Socket/CPU/Processor__
        - _Advice_: if possible, explicit also the number of expected number of tasks _per socket_ (processor) using `--ntasks-per-socket <n>`
    * (_the most confusing_): __Slurm CPU = Physical CORE__
        - use `-c <#threads>` to specify the number of cores reserved per task.
        - Hyper-Threading (HT) Technology is _disabled_ on all ULHPC compute nodes. In particular:
            *  assume **\#cores = \#threads**, thus when using `-c <N>`, you can safely set
            ```bash
            OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1} # Default to 1 if SLURM_CPUS_PER_TASK not set
            ```
            to automatically abstract from the job context

The total number of tasks defined in a given job is stored in the `$SLURM_NTASKS` environment variable.
This is very convenient to abstract from the job context to run MPI tasks/processes in parallel using for instance:
```bash
srun -n ${SLURM_NTASKS} [...]
```

### Job submission options

There are several useful [environment variables](https://slurm.schedmd.com/sbatch.html#lbAK) set be Slurm _within_ an allocated job.
The most important ones are detailed in the below table which summarizes the main job submission options offered with `{sbatch | srun | salloc} [...]`:

| __Command-line option__   | __Description__                                      | __Example__              |
|---------------------------|------------------------------------------------------|--------------------------|
| `-N <N>`                  | **`<N>` Nodes** request                              | `-N 2`                   |
| `--ntasks-per-node=<n>`   | `<n>` Tasks-per-node request                         | `--ntasks-per-node=28`   |
| `--ntasks-per-socket=<n>` | `<n>` Tasks-per-socket request                       | `--ntasks-per-socket=14` |
| `-c=<c>`                  | `<c>` Cores-per-task request (multithreading)        | `-c 1`                   |
| `--mem=<m>GB`             | **`<m>`GB memory per node** request                  | `--mem 0`                |
| `-t [DD-]HH[:MM:SS]>`     | **Walltime** request                                 | `-t 4:00:00`             |
| `-G <gpu>`                | `<gpu>` GPU(s) request                               | `-G 4`                   |
| `-C <feature>`            | Feature request (`broadwell,skylake...`)             | `-C skylake`             |
| `-p <partition>`          | Specify job partition/queue                          |                          |
| `--qos <qos>`             | Specify job qos                                      |                          |
| `-A <account>`            | Specify account                                      |                          |
| `-J <name>`               | Job name                                             | `-J MyApp`               |
| `-d <specification>`      | Job dependency                                       | `-d singleton`           |
| `--mail-user=<email>`     | Specify email address                                |                          |
| `--mail-type=<type>`      | Notify user by email when certain event types occur. | `--mail-type=END,FAIL`   |


### Hardware Characteristics and Slurm features of ULHPC nodes

When selecting specific resources allocations, it is crucial to match the hardware characteristics of the computing nodes.
Details are provided below:

| Node (type)                          | #Nodes | #Socket / #Cores | RAM [GB] | Features              |
|--------------------------------------|--------|-----------------|----------|-----------------------|
| `aion-[0001-0318]`                   | 318    | 2 / 128    | 256      | `batch,epyc`          |
| `iris-[001-108]`                     | 108    | 2 / 28     | 128      | `batch,broadwell`     |
| `iris-[109-168]`                     | 60     | 2 / 28     | 128      | `batch,skylake`       |
| `iris-[169-186]`   (GPU)             | 18     | 2 / 28     | 768      | `gpu,skylake,volta`   |
| `iris-[191-196]`   (GPU)             | 6      | 2 / 28     | 768      | `gpu,skylake,volta32` |
| `iris-[187-190]` <br/>(Large-Memory) | 4      | 4 / 112    | 3072     | `bigmem,skylake`      |

As can be seen, Slurm [features] are associated to ULHPC compute nodes and permits to easily filter with the `-C <feature>` option the list of nodes.

To list available features, use [`sfeatures`](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh#L173):

```bash
sfeatures
# sinfo  -o '%20N %.6D %.6c %15F %12P %f'
# NODELIST              NODES   CPUS NODES(A/I/O/T)  PARTITION    AVAIL_FEATURES
# [...]
```

!!! important "Always try to align resource specifications for your jobs with physical characteristics"
    The typical format of your Slurm submission should thus probably be:
    ```
    sbatch|srun|... [-N <N>] --ntasks-per-node <#sockets * n> --ntasks-per-socket <n> -c <thread> [...]
    ```
    This would define a **total of `<N>`$\times \#sockets \times$`<n>` TASKS, each on `<thread>` threads**.
    :octicons-alert: You **MUST** ensure that `<n>`$\times$`<thread>` matches the number of cores _per socket_ available on the target computing nodes.

    === "Iris (default Dual-CPU)"
        14 cores per socket and 2 sockets (physical CPUs) per _regular_ `iris` node: you **MUST** ensure `<n>`$\times$`<thread>`=14.
        ```bash
        ### Example 1 - use all cores available
        {sbatch|srun|salloc} -N 3 --ntasks-per-node 14 --ntasks-per-socket 7 -c 2 [...]
        # Total: 42 tasks (spread across 3 nodes), each on 2 cores/threads

        ### Example 2 - use all cores available
        {sbatch|srun|salloc} -N 2 --ntasks-per-node 28 -c 1  [...]
        # Total; 56 (single-core) tasks

        ### Example 3 - use all cores available
        {sbatch|srun|salloc} -N 2 --ntasks-per-node 2 --ntasks-per-socket 1 -c 14 [...]
        # Total: 4 tasks (spread across 2 nodes), each on 14 cores/threads
        ```

    === "Iris (Large-Memory)"
        28 cores per socket and 4 sockets (physical CPUs) per _bigmem_ `iris` node: you **MUST** ensure `<n>`$\times$`<thread>`=28.
        ```bash
        ### Example 1 - use all cores available
        {sbatch|srun|salloc} -N 1 --ntasks-per-node 56 --ntasks-per-socket 14 -c 2 [...]
        # Total: 56 tasks on a single bigmem node, each on 2 cores/threads

        ### Example 2 - use all cores available
        {sbatch|srun|salloc} --ntasks-per-node 112 -c 1  [...]
        # Total; 112 (single-core) tasks

        ### Example 3 - use all cores available
        {sbatch|srun|salloc} -N 1 --ntasks-per-node 4 --ntasks-per-socket 1 -c 28 [...]
        # Total: 4 tasks, each on 28 cores/threads
        ```

    === "Aion (default Dual-CPU)"
        64 cores per socket and 2 sockets (physical CPUs) per `aion` node: you **MUST** ensure `<n>`$\times$`<thread>`=64.
        ```bash
        ### Example 1 - use all cores available
        {sbatch|srun|salloc} -N 2 --ntasks-per-node 32 --ntasks-per-socket 16 -c 4 [...]
        # Total: 64 tasks (spread across 2 nodes), each on 2 cores/threads

        ### Example 2 - use all cores available
        {sbatch|srun|salloc} --ntasks-per-node 128 -c 1  [...]
        # Total; 128 (single-core) tasks

        ### Example 3 - use all cores available
        {sbatch|srun|salloc} -N 1 --ntasks-per-node 2 --ntasks-per-socket 1 -c 64 [...]
        # Total: 2 tasks, each on 64 cores/threads
        ```





This would allow you to abstract and adapt from the allocation context with the following variables

| Option                    | Environment variable                          | Example                       |
|---------------------------|-----------------------------------------------|-------------------------------|
| `-N <N>`                  |                                               |                               |
| `--ntasks-per-node=<n>`   | `<n>` Tasks-per-node request                  | `--ntasks-per-node=28`        |
| `--ntasks-per-socket=<n>` | `<n>` Tasks-per-socket request                | `--ntasks-per-socket=14`      |
| `-c=<c>`                  | `<c>` Cores-per-task request (multithreading) | `-c 1`                        |
|                           | `SLURM_NTASKS`: total number of tasks         | `srun -n $SLURM_NTASKS [...]` |

_Note_ that you can easily set default values for these variables with `#SBATCH [...]` comments.
