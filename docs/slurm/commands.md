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
| `sinfo`                       | report system status (nodes, partitions etc.)                                |
| `squeue [-u $(whoami)]`       | display jobs[steps] and their state                                          |
| `seff <jobid>`                | get efficiency metrics of past job                                           |
| `scancel <jobid>`             | cancel a job or set of jobs.                                                 |
| `scontrol show [...]`         | view and/or update system, nodes, job, step, partition or reservation status |
| `sstat`                       | show status of running jobs.                                                 |
| `sacct [-X] -j <jobid> [...]` | display accounting information on jobs.                                      |
| `sprio`                       | show factors that comprise a jobs scheduling priority                        |
| `smap`                        | graphically show information on jobs, nodes, partitions                      |

<!--monitor-end-->

### Live Job Statistics { .t }



~~~bash
$> scontrol show job 2166371
JobId=2166371 JobName=bash
   UserId=<login>(<uid>) GroupId=clusterusers(666) MCS_label=N/A
   Priority=12741 Nice=0 Account=ulhpc QOS=debug JobState=RUNNING Reason=None
   [...]
   SubmitTime=2020-12-07T22:08:25 EligibleTime=2020-12-07T22:08:25
   StartTime=2020-12-07T22:08:25 EndTime=2020-12-07T22:38:25
   [...]
   WorkDir=/mnt/irisgpfs/users/<login>
~~~

### Node/Job Statistics { .t }

~~~bash
$> sinfo
PARTITION   AVAIL  TIMELIMIT  NODES  STATE NODELIST
interactive    up    4:00:00    196   idle iris-[001-196]
batch*         up 2-00:00:00      5    mix [...]
batch*         up 2-00:00:00    127  alloc [...]
batch*         up 2-00:00:00     36   idle [...]
gpu            up 2-00:00:00      4   resv iris-[186,191-193]
gpu            up 2-00:00:00     19  alloc [...]
gpu            up 2-00:00:00      1   idle iris-185
bigmem         up 2-00:00:00      4    mix iris-[187-190]
~~~

. . .

~~~bash
$> slist <JOBID>
# sacct -j <JOBID> --format User,JobID,Jobname%30,partition,state,time,elapsed,\
#              MaxRss,MaxVMSize,nnodes,ncpus,nodelist,AveCPU,ConsumedEnergyRaw
# seff <JOBID>
~~~



### `sinfo`

[`sinfo`](https://slurm.schedmd.com/sinfo.html) allow to view information about Slurm nodes and partitions.


### `squeue`

You can  view information about jobs located in the Slurm scheduling queue (partition/qos), eventually filter on specific job state (_R_:running /_PD_:pending / _F_:failed / _PR_:preempted) with [`squeue`](https://slurm.schedmd.com/squeue.html):

```console
$ squeue [-u <user>] [-p <partition>] [---qos <qos>] [-t R|PD|F|PR]
```

To quickly access **your** jobs, you can simply use `sq`


## Updating jobs

The [`scontrol`](https://slurm.schedmd.com/scontrol.html) command allows certain charactistics of a job to be
updated while it is still **queued** (_i.e._ not running ), with the syntax `scontrol update jobid=<jobid> [...]`

!!! important
    Once the job is running, most changes requested with `scontrol update jobid=[...]` will **NOT** be applied.

### Change timelimit

```bash
# /!\ ADAPT <jobid> and new time limit accordingly
scontrol update jobid=<jobid> timelimit=<[DD-]HH:MM::SS>
```

### Change QOS or Reservation

```bash
# /!\ ADAPT <jobid>, <qos>, <resname> accordingly
scontrol update jobid=<jobid> qos=<qos>
scontrol update jobid=<jobid> reservationname=<resname>
```

### Change account

If you forgot to specify the expected project account:

```bash
# /!\ ADAPT <jobid>, <account> accordingly
scontrol update jobid=<jobid> account=<account>
```
!!! note ""
    The new account must be eligible to run the job.

### Hold and Resume jobs

Prevent a pending job from being started:

```bash
# /!\ ADAPT <jobid>  accordingly
scontrol hold <jobid>
```

Allow a held job to accrue priority and run:

```bash
# /!\ ADAPT <jobid>  accordingly
scontrol release <jobid>
```

## Cancel jobs

Cancel a specific job:

```bash
# /!\ ADAPT <jobid> accordingly
scancel <jobid>
```

??? info "Cancel all jobs owned by a user (you)"
    ```
    scancel -u $USER
    ```
    This only applies to jobs which are associated with your
    accounts.
