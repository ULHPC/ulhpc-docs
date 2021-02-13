#  Regular Jobs

| __Node Type__ | __Slurm command__                                                                      |
|---------------|----------------------------------------------------------------------------------------|
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

## Joining/monitoring running jobs

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
    (node)$> htop # view of all processes
    #               F5: tree view
    #               u <name>: filter by process of <name>
    #               q: quit
    ```

### Monitoring Job CPU/Memory Usage with `pestat`

We have deployed the (excellent) Slurm tool [`pestat`](https://github.com/OleHolmNielsen/Slurm_tools/tree/master/pestat) (Processor Element status) of Ole Holm Nielsen that you can use to quickly check the CPU/Memory usage of your jobs.
Information deserving investigation (too low/high CPU or Memory usage compared to allocation) will be flagged in Red or Magenta

```
pestat [-p <partition>] [-G] [-f]
```

??? example "`pestat` output (official sample output)"
    ![](https://github.com/OleHolmNielsen/Slurm_tools/raw/master/pestat/pestat-example.png)

!!! tips "Always check your node activity (multi-core - single node job)"
    **If you asked for more than a core in your job** (> 1 tasks, `-c <threads>` where `<threads>` > 1), there are 3 typical situations you **MUST** analysed (and `pestat` or `htop` are of great help for that):

    1. You cannot see the expected activity (only 1 core seems to be active at 100%), then you should review your workflow as you are _under_-exploiting (and thus probably **waste**) the allocated resources.
    2. you have the expected activity on the requested cores (Ex: the 28 cores were requested, and `htop` reports a significant usage of all cores) **BUT** the [CPU load of the system]() **exceed the core capacity of the computing node**. That means you are forking too many processes and **overloading/harming** the systems.
        - For instance on regular `iris` (resp. `aion`) node, a CPU load _above_ 28 (resp. 128) is suspect.
            * Note that we use [LBNL Node Health Check (NHC)](https://github.com/mej/nhc) to automatically [drain](https://slurm.schedmd.com/sinfo.html#lbAG) nodes for which the load exceed twice the core capacity
        - An analogy for a _single_ core load with the amont of cars possible in a single-lane brige or tunnel is illustrated below ([<tiny>source</tiny>](https://scoutapm.com/blog/understanding-load-averages)). Like the bridge/tunnel operator, you'd like your cars/processes to never be waiting, otherwise you are harming the system. Imagine this analogy for the amount of cores available on a computing node to better reporesent the situtation on a single core.

        ![](images/understanding-cpu-load-1-core.png)

    3. you have the expected activity on the requested cores and the load match your allocation without harming the system: you're good to go!


!!! warning "On the [impossibility] to monitor passive GPU jobs over `sjoin`"
    If you use `sjoin` to join a GPU job, you **WON'T** be able to see the allocated GPU activity with `nvidia-smi` and all the monitoring tools provided by NVidia.


## Careful Monitoring of your Jobs Efficiency

!!! bug
    **DON'T LEAVE your jobs running WITHOUT monitoring them** and ensure they are not abusing of the computational resources allocated for you!!!

[:fontawesome-solid-sign-in-alt: ULHPC Tutorial / Getting Started](https://ulhpc-tutorials.readthedocs.io/en/latest/beginners/)

!!! important "Walltime estimation and Job efficiency"
    By default, none of the regular jobs you submit can exceed a walltime of 2 days (`2-00:00:00`).
    You have a _strong_ interest to estimate accurately the walltime of your jobs.
    While it is not always possible, or quite hard to guess at the beginning of a given job campaign where you'll probably ask for the maximum walltime possible, you should look back as your historical usage for the past efficiency and elapsed time of your previously completed jobs using [`seff` or `susage` utilities](../slurm/commands.md#job-efficiency-seff-susage).
    Update the time constraint `[#SBATCH] -t [...]` of your jobs accordingly.
    There are two immediate benefits for you:

    1. Short jobs are scheduled faster, and may even be elligible for [backfilling](priority.md#backfill-scheduling)
    2. You will be more likely elligible for a raw share upgrade of your user account -- see [Fairsharing](../slurm/fairsharing.md#q-my-user-fairshare-is-low-what-can-i-do)

In all cases, if you are confident that your jobs will last more than 2 days **while efficiently using the allocated resources**, you can use [`--qos long`](long.md) QOS. Be aware that special restrictions applies for this kind of jobs.

!!! danger "Don't spread across multiple nodes until you validated the single node efficiency!"
    Check with `htop` for instance on [interactive tests](interactive.md) that you are really using the cores you asked for

    Too often, we see job flooding the scheduler which have obviously not been checked for efficiency


## Long jobs


The [`long`](#long-qos) QOS can be used if you are confident this is not sufficient, however be aware that in most of the cases, the 2 days limits is compliant with most workflows.
