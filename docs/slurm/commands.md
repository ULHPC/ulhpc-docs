# Main Slurm Commands

## Submit Jobs

<!--submit-start-->

There are three ways of submitting jobs with slurm, using either [`sbatch`](https://slurm.schedmd.com/sbatch.html), [`srun`](https://slurm.schedmd.com/srun.html) or [`salloc`](https://slurm.schedmd.com/salloc.html):

=== "sbatch (passive job)"
    ```bash
    ### /!\ Adapt <partition>, <qos>, <account> and <command> accordingly
    sbatch -p <partition> [--qos <qos>] [-A <account>] [...] <path/to/launcher.sh>
    ```
=== "srun (interactive job)"
    ```bash
    ### /!\ Adapt <partition>, <qos>, <account> and <command> accordingly
    srun -p <partition> [--qos <qos>] [-A <account>] [...] ---pty bash
    ```
    `srun` is also to be using within your launcher script to initiate a _job step_.

=== "salloc (request allocation/interactive job)"
    ```bash
    # Request interactive jobs/allocations
    ### /!\ Adapt <partition>, <qos>, <account> and <command> accordingly
    salloc -p <partition> [--qos <qos>] [-A <account>] [...] <command>
    ```

### `sbatch`

<!--sbatch-start-->

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
<!--sbatch-end-->

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

### Interactive jobs: `si*`

You should use the helper functions `si`, `si-gpu`, `si-bigmem` to submit an _interactive_ job.

For more details, see [interactive jobs](../jobs/interactive.md).


## Collect Job Information

<!--monitor-job-start-->

| __Command__                   | __Description__                                                              |
|-------------------------------|------------------------------------------------------------------------------|
| `sacct [-X] -j <jobid> [...]` | display accounting information on jobs.                                      |
| `scontrol show [...]`         | view and/or update system, nodes, job, step, partition or reservation status |
| `seff <jobid>`                | get efficiency metrics of past job                                           |
| `smap`                        | graphically show information on jobs, nodes, partitions                      |
| `sprio`                       | show factors that comprise a jobs scheduling priority                        |
| `squeue [-u $(whoami)]`       | display jobs[steps] and their state                                          |
| `sstat`                       | show status of running jobs.                                                 |

<!--monitor-job-end-->

### `squeue`

You can  view information about jobs located in the Slurm scheduling queue (partition/qos), eventually filter on specific job state (_R_:running /_PD_:pending / _F_:failed / _PR_:preempted) with [`squeue`](https://slurm.schedmd.com/squeue.html):

```console
$ squeue [-u <user>] [-p <partition>] [---qos <qos>] [--reservation <name>] [-t R|PD|F|PR]
```

To quickly access **your** jobs, you can simply use `sq`

### Live job statistics

You can use the `scurrent` (for _current_ interactive job) or (more generally) `scontrol show job <jobid>` to collect detailed information for a _running_ job.

??? example "`scontrol show job <jobid>`"
    ```console
    $  scontrol show job 2166371
    JobId=2166371 JobName=bash
       UserId=<login>(<uid>) GroupId=clusterusers(666) MCS_label=N/A
       Priority=12741 Nice=0 Account=ulhpc QOS=debug JobState=RUNNING Reason=None
       [...]
       SubmitTime=2020-12-07T22:08:25 EligibleTime=2020-12-07T22:08:25
       StartTime=2020-12-07T22:08:25 EndTime=2020-12-07T22:38:25
       [...]
       WorkDir=/mnt/irisgpfs/users/<login>
    ```

### Past job statistics: `slist`, `sreport`

Use the `slist` helper for a given job:

```bash
# /!\ ADAPT <jobid> accordingly
$ slist <jobid>
# sacct -j <JOBID> --format User,JobID,Jobname%30,partition,state,time,elapsed,\
#              MaxRss,MaxVMSize,nnodes,ncpus,nodelist,AveCPU,ConsumedEnergyRaw
# seff <jobid>
```

You can also use [`sreport`](https://slurm.schedmd.com/sreport.html) o generate reports of job usage and cluster utilization for Slurm jobs. For instance, to list your usage in CPU-hours since the beginning of the year:

```console
$ sreport -t hours cluster UserUtilizationByAccount Users=$USER  Start=$(date +%Y)-01-01
--------------------------------------------------------------------------------
Cluster/User/Account Utilization 2021-01-01T00:00:00 - 2021-02-13T23:59:59 (3801600 secs)
Usage reported in CPU Hours
----------------------------------------------------------------------------
  Cluster     Login     Proper Name                Account     Used   Energy
--------- --------- --------------- ---------------------- -------- --------
     iris   <login>          <name> <firstname>.<lastname>    [...]
     iris   <login>          <name>      project_<acronym>    [...]
```

### Job efficiency

#### `seff`
<!--seff-start-->

Use `seff` to double check a _past_ job CPU/Memory efficiency. Below examples should be self-speaking:

=== "Good CPU Eff."
    ```console
    $ seff 2171749
    Job ID: 2171749
    Cluster: iris
    User/Group: <login>/clusterusers
    State: COMPLETED (exit code 0)
    Nodes: 1
    Cores per node: 28
    CPU Utilized: 41-01:38:14
    CPU Efficiency: 99.64% of 41-05:09:44 core-walltime
    Job Wall-clock time: 1-11:19:38
    Memory Utilized: 2.73 GB
    Memory Efficiency: 2.43% of 112.00 GB
    ```

=== "Good Memory Eff."
    ```console
    $ seff 2117620
    Job ID: 2117620
    Cluster: iris
    User/Group: <login>/clusterusers
    State: COMPLETED (exit code 0)
    Nodes: 1
    Cores per node: 16
    CPU Utilized: 14:24:49
    CPU Efficiency: 23.72% of 2-12:46:24 core-walltime
    Job Wall-clock time: 03:47:54
    Memory Utilized: 193.04 GB
    Memory Efficiency: 80.43% of 240.00 GB
    ```

=== "Good CPU and Memory Eff."
    ```console
    $ seff 2138087
    Job ID: 2138087
    Cluster: iris
    User/Group: <login>/clusterusers
    State: COMPLETED (exit code 0)
    Nodes: 1
    Cores per node: 64
    CPU Utilized: 87-16:58:22
    CPU Efficiency: 86.58% of 101-07:16:16 core-walltime
    Job Wall-clock time: 1-13:59:19
    Memory Utilized: 1.64 TB
    Memory Efficiency: 99.29% of 1.65 TB
    ```

=== "[Very] Bad efficiency"
    This illustrates a very bad job in terms of CPU/memory efficiency (below 4%), which illustrate a case where basically the user wasted 4 hours of computation while mobilizing a full node and its 28 cores.
    ```console
    $ seff 2199497
    Job ID: 2199497
    Cluster: iris
    User/Group: <login>/clusterusers
    State: COMPLETED (exit code 0)
    Nodes: 1
    Cores per node: 28
    CPU Utilized: 00:08:33
    CPU Efficiency: 3.55% of 04:00:48 core-walltime
    Job Wall-clock time: 00:08:36
    Memory Utilized: 55.84 MB
    Memory Efficiency: 0.05% of 112.00 GB
    ```
     **This is typical of a single-core task** can could be drastically improved via [GNU Parallel](https://ulhpc-tutorials.readthedocs.io/en/latest/sequential/gnu-parallel/).

**Note however that demonstrating a CPU good efficiency with `seff` may not be enough!**
You may still induce an _abnormal_ load on the reserved nodes if you spawn more processes than allowed by the Slurm reservation.
To avoid that, always try to prefix your executions with `srun` within your launchers. See also [Specific Resource Allocations](../slurm/index.md#specific-resource-allocation).

<!--seff-end-->

#### `susage`
<!--susage-start-->

Use `susage` to check your past _jobs walltime accuracy_ (`Timelimit` vs. `Elapsed`)

```console
$ susage -h
Usage: susage [-m] [-Y] [-S YYYY-MM-DD] [-E YYYT-MM-DD]
  For a specific user (if accounting rights granted):    susage [...] -u <user>
  For a specific account (if accounting rights granted): susage [...] -A <account>
Display past job usage summary
```
<!--susage-end-->

#### Official `sacct` command

<!--sacct-start-->


Alternatively, you can use [`sacct`](https://slurm.schedmd.com/sacct.html) (use `sacct --helpformat` to get the list of) for COMPLETED or TIMEOUT jobs (see [Job State Codes](../jobs/reason-codes.md)).

??? example "using `sacct -X -S <start> [...] --format [...],time,elapsed,[...]`"
    ADAPT `-S <start>` and `-E <end>` dates accordingly - Format: `YYYY-MM-DD`.
    _hint_: `$(date +%F)` will return today's date in that format, `$(date +%Y)` return the current year, so the below command will list your completed (or timeout jobs) since the beginning of the month:
    ```console
    $ sacct -X -S $(date +%Y)-01-01 -E $(date +%F) --partition batch,gpu,bigmem --state CD,TO --format User,JobID,partition%12,qos,state,time,elapsed,nnodes,ncpus,allocGRES
         User        JobID    Partition        QOS      State  Timelimit    Elapsed   NNodes      NCPUS    AllocGRES
    --------- ------------ ------------ ---------- ---------- ---------- ---------- -------- ---------- ------------
     <login> 2243517             batch     normal    TIMEOUT 2-00:00:00 2-00:00:05        4        112
     <login> 2243518             batch     normal    TIMEOUT 2-00:00:00 2-00:00:05        4        112
     <login> 2244056               gpu     normal    TIMEOUT 2-00:00:00 2-00:00:12        1         16        gpu:2
     <login> 2246094               gpu       high    TIMEOUT 2-00:00:00 2-00:00:29        1         16        gpu:2
     <login> 2246120               gpu       high  COMPLETED 2-00:00:00 1-02:18:00        1         16        gpu:2
     <login> 2247278            bigmem     normal  COMPLETED 2-00:00:00 1-05:59:21        1         56
     <login> 2250178             batch     normal  COMPLETED 2-00:00:00   10:04:32        1          1
     <login> 2251232               gpu     normal  COMPLETED 1-00:00:00   12:05:46        1          6        gpu:1
    ```

<!--sacct-end-->

## Platform Status

### `sinfo`

[`sinfo`](https://slurm.schedmd.com/sinfo.html) allow to view information about partition status (`-p <partition>`),  problematic nodes (`-R`), reservations (`-T`), eventually in a summarized form (`-s`),

```
sinfo [-p <partition>] {-s | -R | -T |...}
```

We are providing a certain number of [helper functions](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh) based on `sinfo`:

| Command      | Description                                       |
|--------------|---------------------------------------------------|
| `nodelist`   | List available nodes                              |
| `allocnodes` | List currently allocated nodes                    |
| `idlenodes`  | List currently idle nodes                         |
| `deadnodes`  | List dead nodes per partition (hopefully none ;)) |
| `sissues`    | List nodes with issues/problems, with reasons     |
| `sfeatures`  | List available node features                      |

### Cluster, partition and QOS usage stats

We have defined several custom ULHPC Slurm helpers defined in [`/etc/profile.d/slurm.sh`](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh) to facilitate access to account/parition/qos/usage information.
They are listed below.

| __Command__                | __Description__                                                        |
|----------------------------|------------------------------------------------------------------------|
| `acct <name>`              | Get information on user/account holder `<name>` in Slurm accounting DB |
| `irisstat`, `aionstat`     | report cluster status (utilization, partition and QOS live stats)      |
| `listpartitionjobs <part>` | List jobs (and current load) of the slurm partition `<part>`           |
| `pload [-a] i/b/g/m `      | Overview of the Slurm partition load                                   |
| `qload [-a]  <qos>`        | Show current load of the slurm QOS `<qos>`                             |
| `sbill <jobid>`            | Display job charging / billing summary                                 |
| `sjoin [-w <node>]`        | join a running job                                                     |
| `sassoc <name>`            | Show Slurm association information for `<name>` (user or account)      |
| `slist <jobid> [-X]`       | List statistics of a past job                                          |
| `sqos`                     | Show QOS information and limits                                        |
| `susage [-m] [-Y] [...]`   | Display past job usage summary                                         |


## Updating jobs

| __Command__                           | __Description__               |
|---------------------------------------|-------------------------------|
| `scancel <jobid>`                     | cancel a job or set of jobs.  |
| `scontrol update jobid=<jobid> [...]` | update pending job definition |
| `scontrol hold <jobid>`               | Hold job                      |
| `scontrol resume <jobid>`             | Resume held job               |

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
    The new account must be eligible to run the job. See [Account Hierarchy](accounts.md) for more details.

## Hold and Resume jobs

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
