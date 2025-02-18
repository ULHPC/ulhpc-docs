# Slurm Resource and Job Management System

ULHPC uses [Slurm](https://slurm.schedmd.com/) (_Simple Linux Utility for Resource Management_) for cluster/resource management and job scheduling.
This middleware is responsible for allocating resources to users, providing a framework for starting, executing and monitoring work on allocated resources and scheduling work for future execution.

[:fontawesome-solid-sign-in-alt: Official docs](https://slurm.schedmd.com/documentation.html){: .md-button .md-button--link }
[:fontawesome-solid-sign-in-alt: Official FAQ](https://slurm.schedmd.com/faq.html){: .md-button .md-button--link }
[:fontawesome-solid-sign-in-alt: ULHPC Tutorial/Getting Started](https://ulhpc-tutorials.readthedocs.io/en/latest/beginners/){: .md-button .md-button--link }

[![](https://hpc-docs.uni.lu/slurm/images/2022-ULHPC-user-guide.png)](https://hpc-docs.uni.lu/slurm/2022-ULHPC-user-guide.pdf)

!!! important "IEEE ISPDC22: ULHPC Slurm 2.0"
    If you want more details on the RJMS optimizations performed upon Aion acquisition, check out our [IEEE ISPDC22](https://orbilu.uni.lu/handle/10993/51494) conference paper (21<sup>st</sup> IEEE Int. Symp. on Parallel and Distributed Computing) presented in Basel (Switzerland) on July 13, 2022.
    > __IEEE Reference Format__ | [ORBilu entry](https://orbilu.uni.lu/handle/10993/51494) | [slides](https://hpc-docs.uni.lu/slurm/2022-07-13-IEEE-ISPDC22.pdf) <br/>
    > Sebastien Varrette, Emmanuel Kieffer, and Frederic Pinel, "Optimizing the Resource and Job Management System of an Academic HPC and Research Computing Facility". _In 21st IEEE Intl. Symp. on Parallel and Distributed Computing (ISPDC’22)_, Basel, Switzerland, 2022.


## TL;DR Slurm on ULHPC clusters

<!--tldr-start-->

In its concise form, the Slurm configuration in place on [ULHPC
supercomputers](../systems/index.md) features the following attributes you
should be aware of when interacting with it:

* Predefined [_Queues/Partitions_](../slurm/partitions.md) depending on node type
    - `batch`  (Default Dual-CPU nodes) _Max_: 64 nodes, 2 days walltime
    - `gpu`    (GPU nodes nodes)        _Max_: 4 nodes, 2 days walltime
    - `bigmem` (Large-Memory nodes)     _Max_: 1 node, 2 days walltime
    - In addition: `interactive` (for quicks tests)  _Max_: 2 nodes, 2h walltime
        * for code development, testing, and debugging
* Queue Policy: _[cross-partition QOS](../slurm/qos.md)_, mainly tied to _priority level_ (`low` $\rightarrow$ `urgent`)
    - `long` QOS with extended Max walltime (`MaxWall`) set to **14 days**
    -  special _preemptible QOS_ for [best-effort](../jobs/best-effort.md') jobs: `besteffort`.
* [Accounts hierarchy](../slurm/accounts.md) associated to supervisors (multiple
  associations possible), projects or trainings
    - you **MUST** use the proper account as a [detailed usage
      tracking](../policies/usage-charging.md) is performed and reported.
* [Slurm Federation configuration](https://slurm.schedmd.com/federation.html) between `iris` and `aion`
    - ensures global policy (coherent job ID, global scheduling, etc.) within ULHPC systems
    - easily submit jobs from one cluster to another using `-M, --cluster aion|iris`

<!--tldr-end-->

For more details, see the appropriate pages in the left menu.

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

<!--resource-allocation-start-->

Within a job, you aim at running a certain number of **tasks**, and Slurm allow for a fine-grain control of the resource allocation that must be satisfied for _each_ task.

!!! danger "Beware of Slurm terminology in [Multicore Architecture](https://slurm.schedmd.com/mc_support.html)!"
    ![](../slurm/images/slurm_mc_support.png){: style="width:350px; float: right;"}

    * __Slurm Node = Physical node__, specified with `-N <#nodes>`
        - _Advice_: always explicit number of expected number of tasks _per node_ using `--ntasks-per-node <n>`. This way you control the node footprint of your job.
    * __Slurm Socket = Physical Socket/CPU/Processor__
        - _Advice_: if possible, explicit also the number of expected number of tasks _per socket_ (processor) using `--ntasks-per-socket <s>`.
            * relations between `<s>` and `<n>` must be aligned with the physical NUMA characteristics of the node.
            * For instance on aion nodes, `<n> = 8*<s>`
            * For instance on iris regular nodes, `<n>=2*<s>` when on iris bigmem nodes, `<n>=4*<s>`.
    * (_the most confusing_): __Slurm CPU = Physical CORE__
        - use `-c <#threads>` to specify the number of cores reserved per task.
        - Hyper-Threading (HT) Technology is _disabled_ on all ULHPC compute nodes. In particular:
            *  assume **\#cores = \#threads**, thus when using `-c <threads>`, you can safely set
            ```bash
            OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK:-1} # Default to 1 if SLURM_CPUS_PER_TASK not set
            ```
            to automatically abstract from the job context
            * you have interest to match the physical NUMA characteristics of the compute node you're running at (Ex: target 16 threads per socket on Aion nodes (as there are 8 virtual sockets per nodes, 14 threads per socket on Iris regular nodes).

The total number of tasks defined in a given job is stored in the `$SLURM_NTASKS` environment variable.

!!! note "The --cpus-per-task option of srun in Slurm 23.11 and later"
    In the latest versions of Slurm `srun` inherits the `--cpus-per-task` value requested by `salloc` or `sbatch` by reading the value of `SLURM_CPUS_PER_TASK`, as for any other option. _This behavior may differ from some older versions where special handling was required to propagate the `--cpus-per-task` option to `srun`._

In case you would like to launch multiple programs in a single allocation/batch script, divide the resources accordingly by requesting resources with `srun` when launching the process, for instance:
```bash
srun --cpus-per-task <some of the SLURM_CPUS_PER_TASK> --ntasks <some of the SLURM_NTASKS> [...] <program>
```

We encourage you to **always** explicitly specify upon resource allocation the number of tasks you want _per_ node/socket (`--ntasks-per-node <n> --ntasks-per-socket <s>`), to easily scale on multiple nodes with `-N <N>`. Adapt the number of threads and the settings to match the physical NUMA characteristics of the nodes

=== "Aion"
    16 cores per socket and 8 (virtual) sockets (CPUs) per `aion` node.

    * `{sbatch|srun|salloc|si} [-N <N>] --ntasks-per-node <8n> --ntasks-per-socket <n> -c <thread>`
        - _Total_: `<N>`$\times 8\times$`<n>` tasks, each on `<thread>` threads
        - **Ensure** `<n>`$\times$`<thread>`= 16
        - Ex: `-N 2 --ntasks-per-node 32 --ntasks-per-socket 4 -c 4` (_Total_: 64 tasks)

=== "Iris (default Dual-CPU)"
    14 cores per socket and 2 sockets (physical CPUs) per _regular_ `iris`.

    * `{sbatch|srun|salloc|si} [-N <N>] --ntasks-per-node <2n> --ntasks-per-socket <n> -c <thread>`
        - _Total_: `<N>`$\times 2\times$`<n>` tasks, each on `<thread>` threads
        - **Ensure** `<n>`$\times$`<thread>`= 14
        - Ex: `-N 2 --ntasks-per-node 4 --ntasks-per-socket 2  -c 7` (_Total_: 8 tasks)

=== "Iris (Bigmem)"
    28 cores per socket and 4 sockets (physical CPUs) per _bigmem_ `iris`

    * `{sbatch|srun|salloc|si} [-N <N>] --ntasks-per-node <4n> --ntasks-per-socket <n> -c <thread>`
        - _Total_: `<N>`$\times 4\times$`<n>` tasks, each on `<thread>` threads
        - **Ensure** `<n>`$\times$`<thread>`= 28
        - Ex: `-N 2 --ntasks-per-node 8 --ntasks-per-socket 2  -c 14` (_Total_: 16 tasks)

<!--resource-allocation-end-->

## Job submission options

<!--job-submit-options-start-->

There are several useful [environment variables](https://slurm.schedmd.com/sbatch.html#lbAK) set be Slurm _within_ an allocated job.
The most important ones are detailed in the below table which summarizes the main job submission options offered with `{sbatch | srun | salloc} [...]`:

| __Command-line option__   | __Description__                                      | __Example__              |
|---------------------------|------------------------------------------------------|--------------------------|
| `-N <N>`                  | **`<N>` Nodes** request                              | `-N 2`                   |
| `--ntasks-per-node=<n>`   | `<n>` Tasks-per-node request                         | `--ntasks-per-node=28`   |
| `--ntasks-per-socket=<s>` | `<s>` Tasks-per-socket request                       | `--ntasks-per-socket=14` |
| `-c <c>`                  | `<c>` Cores-per-task request (multithreading)        | `-c 1`                   |
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

At a minimum a job submission script must include number of nodes, time, type of partition and nodes (resource allocation constraint and features), and quality of service (QOS).
If a script does not specify any of these options then a default may be applied.
The full list of directives is documented in the man pages for the [`sbatch`](https://slurm.schedmd.com/sbatch.html) command (see. `man sbatch`).

<!--job-submit-options-end-->

### `#SBATCH` directives vs. CLI options

Each option can be specified either as an `#SBATCH [...]` directive in the job submission script:

```slurm
#!/bin/bash -l                # <--- DO NOT FORGET '-l'
### Request a single task using one core on one node for 5 minutes in the batch queue
#SBATCH -N 2
#SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --time=0-00:05:00
#SBATCH -p batch
# [...]
```

Or as a command line option when submitting the script:

```bash
$ sbatch -p batch -N 2 --ntasks-per-node=1 -c 1 --time=0-00:05:00 ./first-job.sh
```

!!! tips ""
    The command line and directive versions of an option are
    **equivalent and interchangeable**:
    if the same option is present both on the command line and as a directive,
    the command line will be honored.
    If the same option or directive is specified twice, the last value supplied
    will be used.
    Also, many options have both a long form, eg `--nodes=2` and a short form, eg `-N 2`. These are equivalent and interchangable.

??? info "Common options to `sbatch` and `srun`"
    Many options are common to both `sbatch` and `srun`, for example
    `sbatch -N 4 ./first-job.sh` allocates 4 nodes to `first-job.sh`, and
    `srun -N 4 uname -n` inside the job runs a copy of `uname -n` on each of 4 nodes.

    If you don't specify an option in the `srun` command line, `srun` will
    inherit the value of that option from  `sbatch`.
    In these cases the default behavior of `srun` is to assume the same
    options as were passed to `sbatch`. This is achieved via environment
    variables: `sbatch` sets a number of environment variables with names
    like `SLURM_NNODES` and srun checks the values of those
    variables. This has two important consequences:

    1. Your job script can see the settings it was submitted with by
       checking these environment variables
    2. You should **NOT** override these environment variables. Also be aware
       that if your job script tries to do certain tricky things, such as using
       `ssh` to launch a command on another node, the environment might not
       be propagated and your job may not behave correctly


### HW characteristics and Slurm features of ULHPC nodes

When selecting specific resources allocations, it is crucial to match the
hardware characteristics of the computing nodes.
Details are provided below:

<!--table-feature-start-->

| Node (type)                          | #Nodes | #Socket / #Cores | RAM [GB] | Features              |
|--------------------------------------|--------|------------------|----------|-----------------------|
| `aion-[0001-0354]`                   | 354    | 8 / 128          | 256      | `batch,epyc`          |
| `iris-[001-108]`                     | 108    | 2 / 28           | 128      | `batch,broadwell`     |
| `iris-[109-168]`                     | 60     | 2 / 28           | 128      | `batch,skylake`       |
| `iris-[169-186]`   (GPU)             | 18     | 2 / 28           | 768      | `gpu,skylake,volta`   |
| `iris-[191-196]`   (GPU)             | 6      | 2 / 28           | 768      | `gpu,skylake,volta32` |
| `iris-[187-190]` <br/>(Large-Memory) | 4      | 4 / 112          | 3072     | `bigmem,skylake`      |

<!--table-feature-end-->

As can be seen, Slurm [features] are associated to ULHPC compute nodes and permits to easily filter with the `-C <feature>` option the list of nodes.

To list available features, use [`sfeatures`](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh#L173):

```bash
sfeatures
# sinfo  -o '%20N %.6D %.6c %15F %12P %f'
# NODELIST              NODES   CPUS NODES(A/I/O/T)  PARTITION    AVAIL_FEATURES
# [...]
```
<!--resource-allocation-match-hw-start-->

!!! important "Always try to align resource specifications for your jobs with physical characteristics"
    The typical format of your Slurm submission should thus probably be:
    ```
    sbatch|srun|... [-N <N>] --ntasks-per-node <n> -c <thread> [...]
    sbatch|srun|... [-N <N>] --ntasks-per-node <#sockets * s> --ntasks-per-socket <s> -c <thread> [...]
    ```
    This would define a **total of `<N>`$\times$`<n>` TASKS** (first form) or
    **`<N>`$\times \#sockets \times$`<s>` TASKS** (second form), **each on
    `<thread>` threads**.
    :octicons-alert: You **MUST** ensure that either:

    * `<n>`$\times$`<thread>` matches the number of cores avaiable on the target
    computing node (first form), or
    * `<n>`=$\#sockets \times$`<s>`, and `<s>`$\times$`<thread>` matches the
    number of cores _per socket_ available on the target computing node (second form).

    === "Aion (default Dual-CPU)"
        16 cores per socket and 8 virtual sockets (CPUs) per `aion` node.
        Depending on the selected form, you **MUST** ensure that either
        `<n>`$\times$`<thread>`=128, or that `<n>`=8`<s>` and `<s>`$\times$`<thread>`=16.
        ```bash
        ### Example 1 - use all cores available
        {sbatch|srun|salloc} -N 2 --ntasks-per-node 32 --ntasks-per-socket 4 -c 4 [...]
        # Total: 64 tasks (spread across 2 nodes), each on 4 cores/threads

        ### Example 2 - use all cores available
        {sbatch|srun|salloc} --ntasks-per-node 128 -c 1  [...]
        # Total; 128 (single-core) tasks

        ### Example 3 - use all cores available
        {sbatch|srun|salloc} -N 1 --ntasks-per-node 8 --ntasks-per-socket 1 -c 16 [...]
        # Total: 8 tasks, each on 16 cores/threads

        ### Example 4 - use all cores available
        {sbatch|srun|salloc} -N 1 --ntasks-per-node 2 -c 64 [...]
        # Total: 2 tasks, each on 64 cores/threads
        ```

    === "Iris (default Dual-CPU)"
        14 cores per socket and 2 sockets (physical CPUs) per _regular_ `iris`
        node. Depending on the selected form, you **MUST** ensure that either
        `<n>`$\times$`<thread>`=28, or that `<n>`=2`<s>` and `<s>`$\times$`<thread>`=14.
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
        28 cores per socket and 4 sockets (physical CPUs) per _bigmem_ `iris`
        node.
        Depending on the selected form, you **MUST** ensure that either
        `<n>`$\times$`<thread>`=112, or that `<n>`=4`<s>` and `<s>`$\times$`<thread>`=28.
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

<!--resource-allocation-match-hw-end-->

## Using Slurm Environment variables



Recall that the Slurm controller will set several `SLURM_*` variables in the environment of
the batch script.
The most important are listed in the table below - use them wisely to make your
launcher script as flexible as possible to abstract and adapt from the
allocation context, "_independently_" of the way the job script has been
submitted.

| Submission option         | Environment variable                      | Typical usage                            |
|---------------------------|-------------------------------------------|------------------------------------------|
| `-N <N>`                  | `SLURM_JOB_NUM_NODES` or<br/> `SLURM_NNODES`   |                                          |
| `--ntasks-per-node=<n>`   | `SLURM_NTASKS_PER_NODE`                   |                                          |
| `--ntasks-per-socket=<s>` | `SLURM_NTASKS_PER_SOCKET`                 |                                          |
| `-c <c>`                  | `SLURM_CPUS_PER_TASK`                     | `OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}` |
|                           | `SLURM_NTASKS`<br/> Total number of tasks | `srun -n $SLURM_NTASKS [...]`            |
