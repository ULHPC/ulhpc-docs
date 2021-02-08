# Main Slurm Commands

## Submit Jobs

<!--submit-start-->


There are three ways of submitting jobs with slurm, using either [`sbatch`](https://slurm.schedmd.com/sbatch.html), [`srun`](https://slurm.schedmd.com/srun.html) or [`salloc`](https://slurm.schedmd.com/salloc.html):

```bash
### /!\ Adapt <partition>, <qos>, <account> and <command> accordingly
# Passive job
sbatch -p <partition> [--qos <qos>] [-A <account>] [...] <path/to/launcher.sh>
# Interactive job -
srun -p <partition> [--qos <qos>] [-A <account>] [...] ---pty bash
# Request interactive jobs/allocations
salloc -p <partition> [--qos <qos>] [-A <account>] [...] <command>
```

### `sbatch`

[`sbatch`](https://slurm.schedmd.com/sbatch.html) is used to submit a batch _launcher script_ for later execution, corresponding to _batch/passive submission mode_.
The script will typically contain one or more `srun` commands to launch parallel tasks.
Upon submission with `sbatch`, Slurm will:

* allocate resources (nodes, tasks, partition, constraints, etc.)
* runs a single **copy** of the batch script on the _first_ allocated node
    - in particular, if you depend on other scripts, ensure you have refer to them with the _complete_ path toward them.

When you submit the job, Slurm responds with the job's ID, which will be used to identify this job in reports from Slurm.

```bash
# /!\ ADAPT path to launcher accordingly
$ sbatch <path/to/launcher>.sh
Submitted batch job 864933
```

### `srun`

[`srun`](https://slurm.schedmd.com/srun.html) is used to initiate parallel _job steps within a job_ **OR** to _start an interactive job_
Upon submission with `srun`, Slurm will:

* (_eventually_) allocate resources (nodes, tasks, partition, constraints, etc.) when run for _interactive_ submission
* launch a job step that will execute on the allocated resources.

A job can contain multiple job steps executing sequentially
or in parallel on independent or shared resources within the job's
node allocation.

### salloc

[`salloc`](https://slurm.schedmd.com/salloc.html) is used to _allocate_ resources for a job
in real time. Typically this is used to allocate resources  (nodes, tasks, partition, etc.) and spawn a
shell. The shell is then used to execute srun commands to launch
parallel tasks.

<!--submit-end-->

## Collect Job Information

<!--monitor-start-->

| __Command__                   | __Description__                                                              |
|-------------------------------|------------------------------------------------------------------------------|
| `sinfo`                       | Report system status (nodes, partitions etc.)                                |
| `squeue [-u $(whoami)]`       | display jobs[steps] and their state                                          |
| `seff <jobid>`                | get efficiency metrics of past job                                           |
| `scancel <jobid>`             | cancel a job or set of jobs.                                                 |
| `scontrol show [...]`         | view and/or update system, nodes, job, step, partition or reservation status |
| `sstat`                       | show status of running jobs.                                                 |
| `sacct [-X] -j <jobid> [...]` | display accounting information on jobs.                                      |
| `sprio`                       | show factors that comprise a jobs scheduling priority                        |
| `smap`                        | graphically show information on jobs, nodes, partitions                      |

<!--monitor-end-->

### `squeue`

You can  view information about jobs located in the Slurm scheduling queue (partition/qos), eventually filter on specific job state (_R_:running /_PD_:pending / _F_:failed / _PR_:preempted) with [`squeue`](https://slurm.schedmd.com/squeue.html):

```console
$ squeue [-u <user>] [-p <partition>] [---qos <qos>] [-t R|PD|F|PR]
```

To quickly access **your** jobs, you can simply use `sq`
