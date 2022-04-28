# ULHPC Job Prioritization Factors

The ULHPC Slurm configuration rely on the [Multifactor Priority Plugin](https://slurm.schedmd.com/priority_multifactor.html) and the **[Fair tree](https://slurm.schedmd.com/fair_tree.html)** algorithm to preform [Fairsharing](../slurm/fairsharing.md) among the users[^1]

[^1]: All users from a higher priority account receive a higher fair share factor than all users from a lower priority account

## Priority Factors

There are several factors enabled on ULHPC supercomputers  that influence job priority:

* _Age_: length of time a job has been waiting (PD state) in the queue
* _Fairshare_: difference between the portion of the computing resource
that has been promised and the amount of resources that has been
consumed - see [Fairsharing](../slurm/fairsharing.md).
* _Partition_: factor associated with each node [partition](../slurm/partitions.md), for instance to privilege `interactive` over `batch` partitions
* _QOS_ A factor associated with each [Quality Of Service](../slurm/qos.md) (`low` $\longrightarrow$ `urgent`)

The job's priority at any given time will be a weighted sum of all the factors that have been enabled.
Job priority can be expressed as:

```bash
Job_priority =
    PriorityWeightAge       * age_factor +
    PriorityWeightFairshare * fair-share_factor+
    PriorityWeightPartition * partition_factor +
    PriorityWeightQOS       * QOS_factor +
    - nice_factor
```

All of the factors in this formula are floating point numbers that range from 0.0 to 1.0.
The weights are unsigned, 32 bit integers, you can get with:
  ```console
  $ sprio -w
  # OR, from slurm.conf
  $ scontrol show config | grep -i PriorityWeight
  ```
You can use the [`sprio`](https://slurm.schedmd.com/sprio.html) to view the factors that comprise a job's scheduling priority and were your (pending) jobs stands in the priority queue.

!!! example "sprio Utility usage"
    Show current weights
    ```
    sprio -w
    ```
    List pending jobs, sorted by jobid
    ```bash
    sprio [-n]     # OR: sp
    ```
    List pending jobs, sorted by priority
    ```
    sprio [-n] -S+Y
    sprio [-n] | sort -k 3 -n
    sprio [-n] -l | sort -k 4 -n
    ```

Getting the priority given to a job can be done either with [`squeue`](https://slurm.schedmd.com/squeue.html):

```bash
# /!\ ADAPT <jobid> accordingly
squeue -o %Q -j <jobid>
```

## Backfill Scheduling

Backfill is a mechanism by which lower priority jobs can start earlier to fill
the idle slots provided they are finished before the next high priority jobs is
expected to start based on resource availability.

!!! important ""
    If your job is sufficiently small, it can be backfilled and scheduled in the shadow of a larger, higher-priority job

For more details, see [official Slurm documentation](https://slurm.schedmd.com/sched_config.html)
