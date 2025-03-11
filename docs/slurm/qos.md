# ULHPC Slurm QoS

[Quality of Service](https://slurm.schedmd.com/qos.html) or QoS is used to constrain or modify the characteristics that a job can have. This could come in the form of specifying a QoS to request for a longer run time or a high priority queue for a given job.

To select a given QoS with a [Slurm command](commands.md), use the `--qos=<QoS>` option (available onlt in long form):

```
srun|sbatch|salloc|sinfo|squeue... [--partition=<partition>] --qos=<QoS> [...]
```

!!! important ""
    The _default_ QoS of your jobs depends on your account and affiliation. Normally, the `--qos=<QoS>` directive does not need to be set for most jobs

We favor in general _cross-partition QoS_, mainly tied to _priority level_ (`low` $\rightarrow$ `urgent`). A special _preemptible QoS_ exists for [best-effort jobs](../jobs/best-effort.md) and is named `besteffort`.

## Available QoS's

<!--qos-start-->

| QoS          (partition)       | Prio | GrpTRES | MaxTresPJ | MaxJobPU | MaxWall     |
|--------------------------------|------|---------|-----------|----------|-------------|
| `besteffort`  (\*)             | 1    |         |           | 300      | 50-00:00:00 |
| `low`         (\*)             | 10   |         |           | 4        |             |
| `normal`      (\*)             | 100  |         |           | 50       |             |
| `long`        (\*)             | 100  | node=24 | node=2    | 4        | 14-00:00:00 |
| `debug`       (`interactive`)  | 150  | node=50 |           | 10       |             |
| `high`        (\*)             | 200  |         |           | 50       |             |
| `urgent`      (\*)             | 1000 |         |           | 100      |             |
| `wide`        (\*)             | 100  |         | node=160  | 10       | 0-02:00:00  |

<!--qos-end-->

## List QoS Limits

<!--limits-start-->

Use the `sqos` utility function to list the existing QOS limits.

!!! example "List current ULHPC QOS limits with `sqos`"
    ```console
    $ sqos
    # sacctmgr show qos  format="name%20,preempt,priority,GrpTRES,MaxTresPerJob,MaxJobsPerUser,MaxWall,flags"
                    Name    Preempt   Priority       GrpTRES       MaxTRES MaxJobsPU     MaxWall                Flags
    -------------------- ---------- ---------- ------------- ------------- --------- ----------- --------------------
                  normal besteffort        100                                   100                      DenyOnLimit
              besteffort                     1                                   300 50-00:00:00            NoReserve
                     low besteffort         10                                     4                      DenyOnLimit
                    high besteffort        200                                    50                      DenyOnLimit
                  urgent besteffort       1000                                   100                      DenyOnLimit
                   debug besteffort        150       node=50                      10                      DenyOnLimit
                    long besteffort        100       node=24        node=2         4 14-00:00:00 DenyOnLimit,Partiti+
                   admin besteffort       1000                                                            DenyOnLimit
                    wide besteffort        100                    node=160        10    02:00:00          DenyOnLimit
    ```

<!--limits-end-->

!!! question "What are the possible limits set on ULHPC QoS?"
    At the QoS level, the following elements are composed to define the [resource limits](https://slurm.schedmd.com/resource_limits.html) for our QoS:

    - Limits on Trackable RESources [TRES](https://slurm.schedmd.com/tres.html) - a resource (nodes, cpus, gpus, etc.) tracked for usage or used to enforce limits against, in particular:
        - `GrpTRES`: The total count of TRES able to be used at any given time from all jobs running from the QoS; if this limit is reached new jobs will be queued but only allowed to run after resources have been relinquished from this group.
        - `MaxTresPerJob`: the maximum size in TRES any given job can have from the QoS.
    - `MaxJobsPerUser`: The maximum number of jobs a user can have running at a given time.
    - `MaxWall[DurationPerJob]`: The maximum wall clock time any individual job can run for in the given QoS.

As explained in the [Limits](../jobs/limits.md) section, there are basically three layers of Slurm limits, from least to most priority:

0. None
0. [Partitions](partitions.md)
0. Account associations: Root/Cluster -> Account (ascending the hierarchy) -> User
0. Job/Partition [QoS](#)
