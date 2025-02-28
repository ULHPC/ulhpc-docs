# ULHPC Slurm Partitions

In Slurm multiple nodes can be grouped into _partitions_ which are sets of nodes aggregated by shared characteristics or objectives, with associated limits for wall-clock time, job size, etc. These limits are hard limits for the jobs and can not be overruled.

To select a given partition with a [Slurm command](commands.md), use the `-p <partition>` option:

```
srun|sbatch|salloc|sinfo|squeue... -p <partition> [...]
```

You will find on ULHPC resources the following partitions (mostly matching the 3 types of computing resources)

* `batch` is intended for running parallel scientific applications as _passive_ jobs on "__regular__" nodes (Dual CPU, no accelerators, 128 to 256 GB of RAM)
* `gpu` is intended for running GPU-accelerated scientific applications  as _passive_ jobs on "__gpu__" nodes (Dual CPU, 4 Nvidia accelerators, 768 GB RAM)
* `bigmem` is dedicated for memory intensive data processing jobs on "__bigmem__" nodes (Quad-CPU, no accelerators, 3072 GB RAM)
* `interactive`: a _floating_ partition intended for quick [interactive jobs](../jobs/interactive.md), allowing for quick tests and compilation/preparation work.
    - this is the only partition crossing all type of nodes (thus _floating_).
    - use `si`, `si-gpu` or `si-bigmem` to submit an interactive job on either a regular, gpu or bigmem node

## Aion

| __AION__      (type)     | #Nodes (cores/node) | Default/MaxTime | MaxNodes | PriorityTier |
|--------------------------|---------------------|-----------------|----------|--------------|
| `interactive` (floating) | 354                 | 30min - 2h      | 2        | 100          |
| `batch` (default)        | 354    (128c)       | 2h    - 48h     | 64       | 1            |

## Iris

| __IRIS__       (type)    | #Nodes (cores/n) | Default/MaxTime | MaxNodes | PriorityTier |
|--------------------------|------------------|-----------------|----------|--------------|
| `interactive` (floating) | 196              | 30min - 2h      | 2        | 100          |
| `batch` (default)        | 168     (28c)    | 2h    - 48h     | 64       | 1            |
| `gpu`                    | 24      (28c)    | 2h    - 48h     | 4        | 1            |
| `bigmem`                 | 4       (112c)   | 2h    - 48h     | 1        | 1            |


## Queues/Partitions State Information

For detailed information about all available partitions and their definition/limits:
```
scontrol show partitions [name]
```

## Partition load status

You can of course use [`squeue -p <partition>`](https://slurm.schedmd.com/squeue.html) to list the jobs currently scheduled on a given, partition `<partition>`.

As part of the custom ULHPC Slurm helpers defined in [`/etc/profile.d/slurm.sh`](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh), the following commands have been made to facilitate the review of the current load usage of the partitions.

| __Command__                | __Description__                                                        |
|----------------------------|------------------------------------------------------------------------|
| `irisstat`, `aionstat`     | report cluster status (utilization, partition and QOS live stats)      |
| `pload [-a] i/b/g/m `      | Overview of the Slurm partition load                                   |
| `listpartitionjobs <part>` | List jobs (and current load) of the slurm partition `<part>`           |

!!! example "Partition load with `pload`"
    ```console
    $ pload -h
    Usage: pload [-a] [--no-header] <partition>
     => Show current load of the slurm partition <partition>, eventually without header
        <partition> shortcuts: i=interactive b=batch g=gpu m=bigmem
     Options:
       -a: show all partition
    $ pload -a
      Partition  CPU Max  CPU Used  CPU Free     Usage[%]
          batch     4704      4223       481       89.8%
            gpu      672       412       260       61.3% GPU: 61/96 (63.5%)
         bigmem      448       431        17       96.2%
    ```

## Partition Limits

At partition level, only the following limits can be enforced:

* `DefaultTime`:       Default time limit
* `MaxNodes`:          Maximum number of nodes per job
* `MinNodes`:          Minimum number of nodes per job
* `MaxCPUsPerNode`:    Maximum number of CPUs job can be allocated on any node
* `MaxMemPerCPU/Node`: Maximum memory job can be allocated on any CPU or node
* `MaxTime`:           Maximum length of time user's job can run
