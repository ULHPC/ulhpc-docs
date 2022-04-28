# ULHPC Slurm QOS 2.0


[Quality of Service](https://slurm.schedmd.com/qos.html) or QOS is used to
constrain or modify the characteristics that a job can have.
This could come in the form of specifying a QoS to request for a longer run time
or a high priority queue for a given job.

To select a given QOS with a [Slurm command](commands.md), use the `--qos <qos>` option:

```
srun|sbatch|salloc|sinfo|squeue... [-p <partition>] --qos <qos> [...]
```

!!! important ""
    The _default_ QoS of your jobs depends on your account and affiliation.
    Normally, the `--qos <qos>` directive does not need to be set for most jobs

We favor in general _cross-partition QOS_, mainly tied to _priority level_
(`low` $\rightarrow$ `urgent`).
A special _preemptible QOS_ exists for [best-effort
jobs](../jobs/best-effort.md) and is named `besteffort`.


## Available QOS

<!--qos-start-->

| QOS          (partition)      | Prio | GrpTRES | MaxTresPJ | MaxJobPU | MaxWall     |
|-------------------------------|------|---------|-----------|----------|-------------|
| `besteffort`  (*)             | 1    |         |           | 50       |             |
| `low`         (*)             | 10   |         |           | 2        |             |
| `normal`      (*)             | 100  |         |           | 50       |             |
| `long`        (*)             | 100  | node=6  | node=2    | 4        | 14-00:00:00 |
| `debug`       (`interactive`) | 150  | node=8  |           | 10       |             |
| `high`        (*)             | 200  |         |           | 50       |             |
| `urgent`      (*)             | 1000 |         |           | 100      |             |

<!--qos-end-->

## List QOS Limits

<!--limits-start-->

Use the `sqos` utility function to list the existing QOS limits.

!!! example "List current ULHPC QOS limits with `sqos`"
    ```console
    $ sqos
    \# sacctmgr show qos  format="name%20,preempt,priority,GrpTRES,MaxTresPerJob,MaxJobsPerUser,MaxWall,flags"
                    Name    Preempt   Priority       GrpTRES       MaxTRES MaxJobsPU     MaxWall                Flags
    -------------------- ---------- ---------- ------------- ------------- --------- ----------- --------------------
                  normal besteffort        100                                    50                      DenyOnLimit
              besteffort                     1                                   100                        NoReserve
                     low besteffort         10                                     2                      DenyOnLimit
                    high besteffort        200                                    50                      DenyOnLimit
                  urgent besteffort       1000                                   100                      DenyOnLimit
                   debug besteffort        150        node=8                      10                      DenyOnLimit
                    long besteffort        100        node=6        node=2         4 14-00:00:00 DenyOnLimit,Partiti+
    ```

<!--limits-end-->

!!! question "What are the possible limits set on ULHPC QOS?"
    At the QOS level, the following elements are composed to define the [resource limits](https://slurm.schedmd.com/resource_limits.html) for our QOS:

    * Limits on Trackable RESources ([TRES](https://slurm.schedmd.com/tres.html) - a resource (cpu,node,etc.) tracked for usage or used to enforce limits against), in particular:
        - `GrpTRES`: The total count of TRES able to be used at any given time from jobs running from the QOS.
            * If this limit is reached new jobs will be queued but only allowed to run after resources have been relinquished from this group.
        - `MaxTresPerJob`: the maximum size in TRES (cpu,nodes,...) any given job can have from the QOS
    * `MaxJobsPerUser`: The maximum number of jobs a user can have running at a given time
    * `MaxWall[DurationPerJob]`= The maximum wall clock time any individual job can run for in the given QOS.

As explained in the [Limits](../jobs/limits.md) section, there are basically three layers of Slurm limits, from least to most priority:

0. None
1. [partitions](partitions.md)
2. account associations: Root/Cluster -> Account (ascending the hierarchy) -> User
3. Job/Partition [QOS](#)
