# Job Status and Reason Codes

The `squeue` command details a variety of information on an active
job’s status with state and reason codes. *__Job state
codes__* describe a job’s current state in queue (e.g. pending,
completed). *__Job reason codes__* describe the reason why the job is
in its current state.

The following tables outline a variety of job state and reason codes you
may encounter when using squeue to check on your jobs.

### Job State Codes

| Status        | Code  | Explaination                                                           |
| ------------- | :---: | ---------------------------------------------------------------------- |
| CANCELLED     | `CA`  | The job was explicitly cancelled by the user or system administrator.  |
| COMPLETED     | `CD`  | The job has completed successfully.                                    |
| COMPLETING    | `CG`  | The job is finishing but some processes are still active.              |
| DEADLINE      | `DL`  | The job terminated on deadline                                         |
| FAILED        | `F`   | The job terminated with a non-zero exit code and failed to execute.    |
| NODE_FAIL     | `NF`  | The job terminated due to failure of one or more allocated nodes       |
| OUT_OF_MEMORY | `OOM` | The Job experienced an out of memory error.                            |
| PENDING       | `PD`  | The job is waiting for resource allocation. It will eventually run.    |
| PREEMPTED     | `PR`  | The job was terminated because of preemption by another job.           |
| RUNNING       | `R`   | The job currently is allocated to a node and is running.               |
| SUSPENDED     | `S`   | A running job has been stopped with its cores released to other jobs.  |
| STOPPED       | `ST`  | A running job has been stopped with its cores retained.                |
| TIMEOUT       | `TO`  | Job terminated upon reaching its time limit.                           |
|               |       |                                                                        |

A full list of these Job State codes can be found in [`squeue`
documentation.](https://slurm.schedmd.com/squeue.html#lbAG) or [`sacct` documentation](https://slurm.schedmd.com/sacct.html#lbAG).

### Job Reason Codes

| Reason Code               | Explaination                                                                                |
| ------------------------  | ------------------------------------------------------------------------------------------- |
| `Priority`                | One or more higher priority jobs is in queue for running. Your job will eventually run.     |
| `Dependency`              | This job is waiting for a dependent job to complete and will run afterwards.                |
| `Resources`               | The job is waiting for resources to become available and will eventually run.               |
| `InvalidAccount`          | The job’s account is invalid. Cancel the job and rerun with correct account.                |
| `InvaldQoS`               | The job’s QoS is invalid. Cancel the job and rerun with correct account.                    |
| `QOSGrpCpuLimit`          | All CPUs assigned to your job’s specified QoS are in use; job will run eventually.          |
| `QOSGrpMaxJobsLimit`      | Maximum number of jobs for your job’s QoS have been met; job will run eventually.           |
| `QOSGrpNodeLimit`         | All nodes assigned to your job’s specified QoS are in use; job will run eventually.         |
| `PartitionCpuLimit`       | All CPUs assigned to your job’s specified partition are in use; job will run eventually.    |
| `PartitionMaxJobsLimit`   | Maximum number of jobs for your job’s partition have been met; job will run eventually.     |
| `PartitionNodeLimit`      | All nodes assigned to your job’s specified partition are in use; job will run eventually.   |
| `AssociationCpuLimit`     | All CPUs assigned to your job’s specified association are in use; job will run eventually.  |
| `AssociationMaxJobsLimit` | Maximum number of jobs for your job’s association have been met; job will run eventually.   |
| `AssociationNodeLimit`    | All nodes assigned to your job’s specified association are in use; job will run eventually. |

A full list of these Job Reason Codes can be found [in Slurm’s
documentation.](https://slurm.schedmd.com/squeue.html#lbAF)

### Running Job Statistics Metrics

The [`sstat`](https://slurm.schedmd.com/sstat.html) command allows users to
easily pull up status information about their currently running jobs.
This includes information about *__CPU usage__*,
*__task information__*, *__node information__*, *__resident set size
(RSS)__*, and *__virtual memory (VM)__*. We can invoke the sstat
command as such:

```bash
# /!\ ADAPT <jobid> accordingly
$ sstat --jobs=<jobid>
```

By default, sstat will pull up significantly more information than
what would be needed in the commands default output. To remedy this,
we can use the `--format` flag to choose what we want in our
output. A chart of some these variables are listed in the table below:

| __Variable__ | __Description__                                          |
| ------------ | -------------------------------------------------------- |
| `avecpu`     | Average CPU time of all tasks in job.                    |
| `averss`     | Average resident set size of all tasks.                  |
| `avevmsize`  | Average virtual memory of all tasks in a job.            |
| `jobid`      | The id of the Job.                                       |
| `maxrss`     | Maximum number of bytes read by all tasks in the job.    |
| `maxvsize`   | Maximum number of bytes written by all tasks in the job. |
| `ntasks`     | Number of tasks in a job.                                |

For an example, let's print out a job's average job id, cpu time, max
rss, and number of tasks. We can do this by typing out the command:

```bash
# /!\ ADAPT <jobid> accordingly
sstat --jobs=<jobid> --format=jobid,cputime,maxrss,ntasks
```

A full list of variables that specify data handled by sstat can be
found with the `--helpformat` flag or by [visiting the slurm page on
`sstat`](https://slurm.schedmd.com/sstat.html).


### Past Job Statistics Metrics

You can use the custom `susage` function in [`/etc/profile.d/slurm.sh`](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh) to collect statistics information.

```console
$ susage -h
Usage: susage [-m] [-Y] [-S YYYY-MM-DD] [-E YYYT-MM-DD]
  For a specific user (if accounting rights granted):    susage [...] -u <user>
  For a specific account (if accounting rights granted): susage [...] -A <account>
Display past job usage summary
```

But by default, you should use the
[`sacct`](https://slurm.schedmd.com/sacct.html) command allows users to pull up
status information about past jobs.
This command is very similar to `sstat`, but is used on jobs
that have been previously run on the system instead of currently
running jobs.

```bash
# /!\ ADAPT <jobid> accordingly
$ sacct [-X] --jobs=<jobid> [--format=metric1,...]
# OR, for a user, eventually between a Start and End date
$ sacct [-X] -u $USER  [-S YYYY-MM-DD] [-E YYYY-MM-DD] [--format=metric1,...]
# OR, for an account - ADAPT <account> accordingly
$ sacct [-X] -A <account> [--format=metric1,...]
```

Use `-X` to _aggregate_ the statistics relevant to the job allocation itself, not
taking job steps into consideration.


The main metrics code you may be interested to review are listed below.

| Variable       | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `account`      | Account the job ran under.                                                  |
| `avecpu`       | Average CPU time of all tasks in job.                                       |
| `averss`       | Average resident set size of all tasks in the job.                          |
| `cputime`      | Formatted (Elapsed time * CPU) count used by a job or step.                 |
| `elapsed`      | Jobs elapsed time formated as DD-HH:MM:SS.                                  |
| `exitcode`     | The exit code returned by the job script or salloc.                         |
| `jobid`        | The id of the Job.                                                          |
| `jobname`      | The name of the Job.                                                        |
| `maxdiskread`  | Maximum number of bytes read by all tasks in the job.                       |
| `maxdiskwrite` | Maximum number of bytes written by all tasks in the job.                    |
| `maxrss`       | Maximum resident set size of all tasks in the job.                          |
| `ncpus`        | Amount of allocated CPUs.                                                   |
| `nnodes`       | The number of nodes used in a job.                                          |
| `ntasks`       | Number of tasks in a job.                                                   |
| `priority`     | Slurm priority.                                                             |
| `qos`          | Quality of service.                                                         |
| `reqcpu`       | Required number of CPUs                                                     |
| `reqmem`       | Required amount of memory for a job.                                        |
| `reqtres`      | Required [Trackable RESources (TRES)](https://slurm.schedmd.com/tres.html) |
| `user`         | Userna                                                                      |

A full list of variables that specify data handled by sacct can be
found with the `--helpformat` flag or by [visiting the slurm page on
`sacct`](https://slurm.schedmd.com/sacct.html).
