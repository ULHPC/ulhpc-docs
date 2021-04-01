#  Regular Jobs

| __Node Type__ | __Slurm command__                                                                      |
|:-------------:|----------------------------------------------------------------------------------------|
| regular       | `sbatch [-A <project>] -p batch  [--qos {high,urgent}] [-C {broadwell,skylake}] [...]` |
| gpu           | `sbatch [-A <project>] -p gpu    [--qos {high,urgent}] [-C volta[32]] -G 1 [...]`      |
| bigmem        | `sbatch [-A <project>] -p bigmem [--qos {high,urgent}] [...]`                          |

[:fontawesome-solid-sign-in-alt: Main Slurm commands](../slurm/commands.md){: .md-button .md-button--link }
[:fontawesome-solid-sign-in-alt: Resource Allocation guide](../slurm/index.md#specific-resource-allocation){: .md-button .md-button--link }

## `sbatch [...] /path/to/launcher`

{%
   include-markdown "../slurm/commands.md"
   start="<!--sbatch-start-->"
   end="<!--sbatch-end-->"
%}

### Job Submission Option

{%
   include-markdown "../slurm/index.md"
   start="<!--job-submit-options-start-->"
   end="<!--job-submit-options-end-->"
%}

{%
   include-markdown "../slurm/index.md"
   start="<!--resource-allocation-start-->"
   end="<!--resource-allocation-end-->"
%}

### Careful Monitoring of your Jobs

!!! bug
    **DON'T LEAVE your jobs running WITHOUT monitoring them** and ensure they are not abusing of the computational resources allocated for you!!!

[:fontawesome-solid-sign-in-alt: ULHPC Tutorial / Getting Started](https://ulhpc-tutorials.readthedocs.io/en/latest/beginners/){: .md-button .md-button--link }

You will find below several ways to monitor the effective usage of the resources allocated (for running jobs) as well as the general efficiency (Average Walltime Accuracy, CPU/Memory efficiency etc.) for past jobs.

## Joining/monitoring running jobs

### `sjoin`

At any moment of time, you can _join_ a running job using the
[custom helper functions](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh)
`sjoin` **in another terminal** (or another screen/tmux tab/window). The format is as follows:

```bash
sjoin <jobid> [-w <node>]    # Use <tab> to automatically complete <jobid> among your jobs
```

!!! example "Using `sjoin` to `htop` your processes"
    ```bash
    # check your running job
    (access)$> sq
    # squeue -u $(whoami)
       JOBID PARTIT       QOS                 NAME       USER NODE  CPUS ST         TIME    TIME_LEFT PRIORITY NODELIST(REASON)
     2171206  [...]
    # Connect to your running job, identified by its Job ID
    (access)$> sjoin 2171206     # /!\ ADAPT <jobid> accordingly, use <TAB> to have it autocatically completed
    # Equivalent of: srun --jobid 2171206 --gres=gpu:0 --pty bash -i
    (node)$> htop # view of all processes
    #               F5: tree view
    #               u <name>: filter by process of <name>
    #               q: quit
    ```

!!! warning "On the [impossibility] to monitor _passive_ GPU jobs over `sjoin`"
    If you use `sjoin` to join a GPU job, you **WON'T** be able to see the allocated GPU activity with `nvidia-smi` and all the monitoring tools provided by NVidia.
    The reason is that currently, there is no way to perform an over-allocation of a Slurm [Generic Resource](https://slurm.schedmd.com/gres.html) (GRES) as our GPU cards, that means you can't create (_e.g._ with `sjoin` or `srun --jobid [...]`) job steps with access to GPUs which are bound to another step.
    **To keep `sjoin` working with gres job, you MUST add "`--gres=none`"**

    You can use a direct connection with `ssh <node>` or `clush -w @job:<jobid>` for that (see below) but be aware that confined context is **NOT** maintained that way and that you will see the GPU processes on _all_ 4 GPU cards.


### ClusterShell

!!! danger
    **Only for VERY Advanced users!!!**.
    You should know what you are doing when using [ClusterShell](https://clustershell.readthedocs.io/en/latest/intro.html) as you can mistakenly generate a huge amount of remote commands across the cluster which, while they will likely fail, still induce an unexpected load that may disturb the system.

[ClusterShell](https://clustershell.readthedocs.io/en/latest/intro.html) is a useful Python package for executing arbitrary commands across multiple hosts.
On the ULHPC clusters, it provides a relatively simple way for you to run commands on nodes your jobs are running on, and collect the results.

!!! info
    You can only `ssh` to, and therefore run `clush` on, nodes where you have **active/running** jobs.


#### `nodeset`

The [`nodeset`](https://clustershell.readthedocs.io/en/latest/tools/nodeset.html) command enables the easy manipulation of node sets, as well as node groups, at the command line level.
It uses `sinfo`  underneath but has slightly different syntax. You can use it to ask about node states and nodes your job is running on.

The nice difference is you can ask for **folded** (e.g. `iris-[075,078,091-092]`) or **expanded** (e.g. `iris-075 iris-078 iris-091 iris-092`) forms of the node lists.

| __Command__        | __description__                                      |
|--------------------|------------------------------------------------------|
| `nodeset -L[LL]`   | List all groups  available                           |
| `nodeset -c [...]` | show number of nodes in nodeset(s)                   |
| `nodeset -e [...]` | expand nodeset(s) to separate nodes                  |
| `nodeset -f [...]` | fold nodeset(s) (or separate nodes) into one nodeset |


??? example "Nodeset expansion and folding"
    === "nodeset -e (expand)"
        ```bash
        # Get list of nodes with issues
        $ sinfo -R --noheader -o "%N"
        iris-[005-008,017,161-162]
        # ... and expand that list
        $ sinfo -R --noheader -o "%N" | nodeset -e
        iris-005 iris-006 iris-007 iris-008 iris-017 iris-161 iris-162

        # Actually equivalent of (see below)
        $ nodeset -e @state:drained
        ```

    === "nodeset -f (fold)"
        ```bash
        # List nodes in IDLE state
        $> sinfo -t IDLE --noheader
        interactive    up    4:00:00      4   idle iris-[003-005,007]
        long           up 30-00:00:0      2   idle iris-[015-016]
        batch*         up 5-00:00:00      1   idle iris-134
        gpu            up 5-00:00:00      9   idle iris-[170,173,175-178,181]
        bigmem         up 5-00:00:00      0    n/a

        # make out a synthetic list
        $> sinfo -t IDLE --noheader | awk '{ print $6 }' | nodeset -f
        iris-[003-005,007,015-016,134,170,173,175-178,181]

        # ... actually done when restricting the column to nodelist only
        $> sinfo -t IDLE --noheader -o "%N"
        iris-[003-005,007,015-016,134,170,173,175-178,181]

        # Actually equivalent of (see below)
        $ nodeset -f @state:idle
        ```

??? example "Exclusion / intersection  of nodeset"
    | __Option__               | __Description__                                                         |
    |--------------------------|-------------------------------------------------------------------------|
    | `-x <nodeset>`           | __exclude__ from working set `<nodeset>`                                |
    | `-i <nodeset>`           | __intersection__ from working set with `<nodeset>`                      |
    | `-X <nodeset>` (`--xor`) | elements that are in __exactly one__ of the working set and `<nodeset>` |

    ```bash
    # Exclusion
    $> nodeset -f iris-[001-010] -x iris-[003-005,007,015-016]
    iris-[001-002,006,008-010]
    # Intersection
    $> nodeset -f iris-[001-010] -i iris-[003-005,007,015-016]
    iris-[003-005,007]
    # "XOR" (one occurrence only)
    $> nodeset -f iris-[001-010] -x iris-006 -X iris-[005-007]
    iris-[001-004,006,008-010]
    ```

The groups useful to you that we have configured are `@user`, `@job` and `@state`.

=== "List available groups"
    ```bash
    $ nodeset -LLL
    # convenient partition groups
    @batch  iris-[001-168] 168
    @bigmem iris-[187-190] 4
    @gpu    iris-[169-186,191-196] 24
    @interactive iris-[001-196] 196
    # conveniente state groups
    @state:allocated [...]
    @state:idle      [...]
    @state:mixed     [...]
    @state:reserved  [...]
    # your individual jobs
    @job:2252046 iris-076 1
    @job:2252050 iris-[191-196] 6
    # all the jobs under your username
    @user:svarrette iris-[076,191-196] 7
    ```

=== "User group"
    List expanded node names where you have jobs running
    ```bash
    # Similar to: squeue -h -u $USER -o "%N"|nodeset -e
    $ nodeset -e @user:$USER
    ```

=== "Job group"
    List folded nodes where your job 1234567 is running (use `sq` to quickly list your jobs):
    ```bash
    $ similar to squeue -h -j 1234567 -o "%N"
    nodeset -f @job:1234567
    ```

=== "State group"
    List expanded node names that are idle according to slurm
    ```bash
    # Similar to: sinfo -t IDLE -o "%N"
    nodeset -e @state:idle
    ```

#### `clush`

[`clush`](https://clustershell.readthedocs.io/en/latest/tools/clush.html) can run commands on multiple nodes at once for instance to monitor you jobs. It uses the node grouping syntax from [`nodeset`]((https://clustershell.readthedocs.io/en/latest/tools/nodeset.html) to allow you to run commands on those nodes.

[`clush`](https://clustershell.readthedocs.io/en/latest/tools/clush.html) uses `ssh` to connect to each of these nodes.
You can use the `-b` option to gather output from nodes with same output into the same lines. Leaving this out will report on each node separately.

| __Option__      | __Description__                                                          |
|-----------------|--------------------------------------------------------------------------|
| `-b`            | gathering output (as when piping to `dshbak -c`)                         |
| `-w <nodelist>` | specify remote hosts, incl. node groups with `@group` special syntax     |
| `-g <group>`    | similar to `-w @<group>`, restrict commands to the hosts group `<group>` |
| `--diff`        | show differences between common outputs                                  |

=== "Monitor CPU usage"
    Show %cpu, memory usage, and command for all nodes running any of your jobs.
    ``` bash
    clush -bw @user:$USER ps -u$USER -o%cpu,rss,cmd
    ```
    As above, but only for the nodes reserved with your job `<jobid>`
    ``` bash
    clush -bw @job:<jobid> ps -u$USER -o%cpu,rss,cmd
    ```



=== "Monitor GPU usage"
    Show what's running on _all_ the GPUs on the nodes associated with your job `654321`.
    ``` bash
    clush -bw @job:654321 bash -l -c 'nvidia-smi --format=csv --query-compute-apps=process_name,used_gpu_memory'
    ```
    As above but for all your jobs (assuming you have only GPU nodes with _all_ GPUs)
    ```bash
    clush -bw @user:$USER bash -l -c 'nvidia-smi --format=csv --query-compute-apps=process_name,used_gpu_memory'
    ```

    This may be convenient for passive jobs since the `sjoin` utility does **NOT** permit to run `nvidia-smi` (see [explaination](#sjoin)).
    **However** that way you will see unfortunately _ALL_ processes running on the 4 GPU cards -- including from other users sharing your nodes. It's a known bug, not a feature.


### `pestat`: CPU/Mem usage report


We have deployed the (excellent) Slurm tool [`pestat`](https://github.com/OleHolmNielsen/Slurm_tools/tree/master/pestat) (Processor Element status) of Ole Holm Nielsen that you can use to quickly check the CPU/Memory usage of your jobs.
Information deserving investigation (too low/high CPU or Memory usage compared to allocation) will be flagged in Red or Magenta

```
pestat [-p <partition>] [-G] [-f]
```

??? example "`pestat` output (official sample output)"
    ![](https://github.com/OleHolmNielsen/Slurm_tools/raw/master/pestat/pestat-example.png)

### General Guidelines

As mentionned before, always check your node activity with _at least_ `htop` on the **all** allocated nodes to ensure you use them as expected. Several cases might apply to your job workflow:

=== "Single Node, single core"
    You are dealing with an [embarrasingly parallel job campaign](https://ulhpc-tutorials.readthedocs.io/en/latest/sequential/basics/#embarrassingly-gnu-parallel-tasks-across-multiples-nodes) and this approach is **bad** and overload the scheduler unnecessarily.
    You will also quickly cross the limits set in terms of maximum number of jobs.
    **You must aggregate multiples tasks within a single job** to exploit fully a complete node.
    In particular, you **MUST** consider using [GNU Parallel](https://ulhpc-tutorials.readthedocs.io/en/latest/sequential/gnu-parallel/) and our [generic GNU launcher `launcher.parallel.sh`](https://github.com/ULHPC/tutorials/blob/devel/sequential/basics/scripts/launcher.parallel.sh).

    [:fontawesome-solid-sign-in-alt: ULHPC Tutorial / HPC Management of Embarrassingly Parallel Jobs](https://ulhpc-tutorials.readthedocs.io/en/latest/beginners/){: .md-button .md-button--link }


=== "Single Node, multi-core"
    **If you asked for more than a core in your job** (> 1 tasks, `-c <threads>` where `<threads>` > 1), there are 3 typical situations you **MUST** analysed (and `pestat` or `htop` are of great help for that):

    1. You cannot see the expected activity (only 1 core seems to be active at 100%), then you should review your workflow as you are _under_-exploiting (and thus probably **waste**) the allocated resources.
    2. you have the expected activity on the requested cores (Ex: the 28 cores were requested, and `htop` reports a significant usage of all cores) **BUT** the [CPU load of the system]() **exceed the core capacity of the computing node**. That means you are forking too many processes and **overloading/harming** the systems.
        - For instance on regular `iris` (resp. `aion`) node, a CPU load _above_ 28 (resp. 128) is suspect.
            * Note that we use [LBNL Node Health Check (NHC)](https://github.com/mej/nhc) to automatically [drain](https://slurm.schedmd.com/sinfo.html#lbAG) nodes for which the load exceed twice the core capacity
        - An analogy for a _single_ core load with the amont of cars possible in a single-lane brige or tunnel is illustrated below ([<tiny>source</tiny>](https://scoutapm.com/blog/understanding-load-averages)). Like the bridge/tunnel operator, you'd like your cars/processes to never be waiting, otherwise you are harming the system. Imagine this analogy for the amount of cores available on a computing node to better reporesent the situtation on a single core.

        ![](images/understanding-cpu-load-1-core.png)

    3. you have the expected activity on the requested cores and the load match your allocation without harming the system: you're good to go!

=== "Multi-node"
    **If you asked for more than ONE node**, ensure that you have consider the following questions.

    1. You are running an **MPI job**: you generally know what you're doing, **YET** ensure your followed the single node monitoring checks (`htop` etc. yet across all nodes) to review your core activity on **ALL** nodes (see 3. below) .
    Consider also parallel profilers like [Arm Forge](../development/performance-debugging-tools/arm-forge.md)
    2. You are running an [embarrasingly parallel job campaign](https://ulhpc-tutorials.readthedocs.io/en/latest/sequential/basics/#embarrassingly-gnu-parallel-tasks-across-multiples-nodes). You should first ensure you correctly exploit a **single node** using [GNU Parallel](https://ulhpc-tutorials.readthedocs.io/en/latest/sequential/gnu-parallel/) before attempting to cross multiple nodes
    3. You run a distributed framework able to exploit multiple nodes (typically with a master/slave model as for [Spark cluster](https://ulhpc-tutorials.readthedocs.io/en/latest/bigdata/#running-spark-in-standalone-cluster)). You **MUST** assert that your [slave] processes are _really_ run on the over nodes using

    ```bash
    # check you running job
    $ sq
    # Join **another** node than the first one listed
    $ sjoin <jobid> -w <node>
    $ htop  # view of all processes
    #               F5: tree view
    #               u <name>: filter by process of <name>
    #               q: quit
    ```

## Monitoring past jobs efficiency

!!! important "Walltime estimation and Job efficiency"
    By default, none of the regular jobs you submit can exceed a walltime of 2 days (`2-00:00:00`).
    You have a _strong_ interest to estimate accurately the walltime of your jobs.
    While it is not always possible, or quite hard to guess at the beginning of a given job campaign where you'll probably ask for the maximum walltime possible, you should look back as your historical usage for the past efficiency and elapsed time of your previously completed jobs using [`seff` or `susage` utilities](../slurm/commands.md#job-efficiency-seff-susage).
    Update the time constraint `[#SBATCH] -t [...]` of your jobs accordingly.
    There are two immediate benefits for you:

    1. Short jobs are scheduled faster, and may even be elligible for [backfilling](priority.md#backfill-scheduling)
    2. You will be more likely elligible for a raw share upgrade of your user account -- see [Fairsharing](../slurm/fairsharing.md#q-my-user-fairshare-is-low-what-can-i-do)

The below utilities will help you track the CPU/Memory efficiency (`seff`) or the Average Walltime Accuracy (`susage`, `sacct`) of your past jobs

### `seff`

{%
   include-markdown "../slurm/commands.md"
   start="<!--seff-start-->"
   end="<!--seff-end-->"
%}

### `susage`

{%
   include-markdown "../slurm/commands.md"
   start="<!--susage-start-->"
   end="<!--susage-end-->"
%}

In all cases, if you are confident that your jobs will last more than 2 days **while efficiently using the allocated resources**, you can use [`--qos long`](long.md) QOS. Be aware that special restrictions applies for this kind of jobs.
