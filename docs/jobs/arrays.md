# Job arrays in HPC systems

[Job arrays](https://slurm.schedmd.com/job_array.html) is a mechanism for submitting and managing collections of similar jobs. All jobs in an array have the same options in terms of scheduler resources, as they are submitted with the same `sbatch` options and directives.

!!! info "When to use job arrays"
    A naive way to submit multiple jobs is to programmatically submit the jobs with a custom script. This however can quickly hit the [maximum job limit](/slurm/qos/#available-qoss) (`MaxJobPU`), which is `100` jobs per user in the `normal` QoS. If your jobs share the same options, then consider using job arrays. Job arrays create job records for task progressively, so they will help you keep within `MaxJobPU` while reducing the load for the scheduler.

!!! warning "When _not_ to use job arrays"
    Every job in a job array requires an allocation from the scheduler, which is an expensive operation. If you plan to submit many small jobs in an array that require the allocation of more than _10 jobs per minute_, please use [GNU parallel](/jobs/gnu-parallel/) to batch multiple tasks in a single job allocation.

<!--
quickly and easily; job arrays with millions of tasks can be submitted in milliseconds (subject to configured size limits). All jobs must have the same initial options (e.g. size, time limit, etc.), however it is possible to change some of these options after the job has begun execution using the scontrol command specifying the JobID of the array or individual ArrayJobID.

In HPC systems, cluster policy may enforce job submission limits in order to protect the scheduler from overload.

When you want to submit multiple jobs that share the same initial options (e.g. qos, time limit etc.) but with different input parameters the naive way is to manually or programatically generate and submit multiple scripts with different parameters each with its own sbatch job allocation. But doing this may quickly hit the cluster limits and risks having your job submission rejected. 

Job arrays provides you with a mechanism for submitting and managing collections of similar jobs quickly and easily, while still giving you fine control over the maximum simultaneously running tasks from the Job array.
-->

## Using job arrays

The job array feature of Slurm groups similar jobs and provides functionality for managing the group of jobs. A fundamental concept for managing and organizing the is the task index value (task ID). Every task in the job array is a Slurm job and is assigned a task ID which is used to refer to the Slurm job in the context of the job array. The following environment variables are set in job array tasks on top of the usual `SLURM_JOB_ID` that is available on all jobs.

- `SLURM_ARRAY_JOB_ID` is the Slurm job ID of the whole job array.
- `SLURM_ARRAY_TASK_ID` is the task ID of the current Slurm job.
- `SLURM_ARRAY_TASK_COUNT` is the total number of tasks in the job array.
- `SLURM_ARRAY_TASK_MAX` is the largest task ID in the job array
- `SLURM_ARRAY_TASK_MIN` is the smallest task ID in the job array.

??? info "Inner workings of jobs arrays and the job ID of the whole array"
    When a job array is submitted to Slurm, [only one job record is created](https://slurm.schedmd.com/job_array.html#squeue). The `SLURM_JOB_ID` of this initial job will then be the `SLURM_ARRAY_JOB_ID` of the whole array. Additional jobs records are then created by the initial job. Using the `squeue` someone can see additional jobs appear in the as their records are created by the initial job, and you will also see the initial job name change to reflect the progress of the job array execution.

    Typically the Slurm job with `SLURM_ARRAY_JOB_ID` will also execute the last task in the array before terminating, but this is implementation dependent and not part of the job array interface.

The task ID takes values from `0` up to some maximum value determined by the `MaxArraySize` variable in the Slurm configuration. The maximum available task ID is `(MaxArraySize - 1)`, and limits the maximum possible size of a job array.

!!! info "Maximum size of job arrays in UL HPC systems"
    The `MaxArraySize` in our site is set to the [default value](https://slurm.schedmd.com/job_array.html#administration) from Slurm at `1001`. Job arrays allow the submission of many jobs very quickly, and purely configured scripts can easily overload the scheduler.

    If you are affected by the `MaxArraySize` limit, please consider using [GNU parallel](/jobs/gnu-parallel/).

### Submitting a job array

A job array is submitted with the `--array` (`-a` short form) option of `sbatch`. The option is available both in the command line and as script `#SBATCH` directive, as usual. The `--array` option takes as argument a list of tasks that will be run. The simples for of list is a simple range,

```console
sbatch --array=0-31 job_array_script.sh
```

where the `--array` is used to control how many Slurm jobs are created. Inside the `job_array_script.sh` the `SLURM_ARRAY_TASK_ID` can be used to control to differentiate the operation of the script.

??? info "Advances _task list_ specifications"
    During debugging or testing it's often convenient to specify a subrange of tasks to execute. The _task list_ supports a rich syntax. The types of _entries_ in the task list are

    - single task task IDs: `<task ID>`,
    - ranges of task IDs: `<task ID:begin>-<task ID:end>` where `<task ID:begin> <= <task ID:end>`, and
    - stepped ranges of task IDs: `<task ID:begin>-<task ID:end>:<step>` where `<task ID:begin> <= <task ID:end>` and `<step> > 0`.

    Any comma separated list of _entries_ is a task list and repeated entries are ignored.

    For instance,

    - `--array=1-4` is equivalent to `--array=1,2,3,4`,
    - `--array=1-7:2` is equivalent to `--array=1,3,5,7`,
    - `--array=1-7:2,0-6:2` is equivalent to `--array=1,3,5,7,0,2,4,6`, and
    - `--array=1-4,1-7:2` is equivalent to `--array=1,2,3,4,5,7`.

    A task list is _valid_ if all task IDs in the list are the range `0-MaxArraySize`.

If you job specification has a syntax error or lists tasks with ID outside the range `0-MaxArraySize`, then the array job submission fails immediately with an error message 

!!! warning "Job execution order"
    The task ID simply provides a way to differentiate the job array tasks and their behavior, there is no guaranty in which order tasks will run. If you need your job array tasks to run in a particular order consider using job dependencies.

### Managing tasks and arrays

A combination of the `${SLURM_ARRAY_TASK_ID}` and `${SLURM_ARRAY_JOB_ID}` can replace the `${SLURM_JOB_ID}` of job array tasks in Slurm commands such as `scontrol` and `squeue`.

- Use the `${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}` to refer to a task of the job array.
- Use the `${SLURM_ARRAY_JOB_ID}` to refer to all the tasks of the job array collectively.

#### Viewing array job status

Assume that array with `SLURM_ARRAY_JOB_ID=9624577` is running.

- To view the status of the whole job array use:
  ```console
  squeue --job=9624577
  ```
- To view the status of a job array task with `SLURM_ARRAY_TASK_ID=197` in particular use:
  ```console
  squeue --job=9624577_197
  ```

!!! info "Viewing the status of all steps of a submitted array"
    When submitting a job array job records for the tasks of the array are created progressively. If you would like to view all submitted tasks, provide the `--array` (`-r` short format) option to `squeue`.

??? info "Formatting the output of `squeue` to extract array status information"
    The job ID string printed by `squeue` contains information about the status of the array job, but the ID string may be printed with insufficient number of digit to extract any useful information. Use the `--format` or `--Format` options of `squeue` to control how information is printed. The `--format` option supports greater flexibility in formatting whereas `--Format` supports access to all fields; the 2 interfaces cannot be used in parallel.

    The following option values print the ID string with sufficiently many digits:

    === "`--format` style"
        ```console
        squeue --format='%.25i %.9P %.9q %.15j %.15u %.2t %.6D %.10M %.10L %12Q %R'
        ```
    === "`--Format` style"
        ```console
        squeue --Format='JobID:10,ArrayTaskID:20,Partition:10,QOS:10,Name:30,UserName:20,NumNodes:6,State:15,TimeUsed:6,TimeLeft:10,PriorityLong:10,ReasonList:30'
        ```

    The format commands are compatible with the `sq` wrapper script for `squeue` that is available in UL HPC systems.

    You can also set environment variables to avoid having to specify the format string every time.

    - Set `SQUEUE_FORMAT` for old interface `--format` type scripts.
    - Set `SQUEUE_FORMAT2` for new interface `--Format` type scripts.

    This variables can be set in the `${HOME}/.bashrc` script to be loaded automatically in your environment.

    === "`--format` style"
        ```bash
        export SQUEUE_FORMAT='%.25i %.9P %.9q %.15j %.15u %.2t %.6D %.10M %.10L %12Q %R'
        ```
    === "`--Format` style"
        ```bash
        export SQUEUE_FORMAT2='JobID:10,ArrayTaskID:20,Partition:10,QOS:10,Name:30,UserName:20,NumNodes:6,State:15,TimeUsed:6,TimeLeft:10,PriorityLong:10,ReasonList:30'`
        ```

#### Canceling job arrays and job array tasks

Assume that array with `SLURM_ARRAY_JOB_ID=9624577` is running.

- To cancel the whole job array use:
  ```console
  scancel 9624577
  ```
- To cancel the job array task with `SLURM_ARRAY_TASK_ID=197` in particular use:
  ```console
  scancel 9624577_197
  ```
#### Modifying job array tasks

Even though job array tasks are submitted with the exact same scheduler options, individual jobs can be modified at any point before completion with the `scotrol` command. For instance, you can increase the runtime of the task of a job array that has already been submitted.

Consider submitting the following job.

!!! example "`stress_test.sh`"
    ```bash
    #!/bin/bash --login
    #SBATCH --job-name=array_script
    #SBATCH --array=0-400%4
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=16
    #SBATCH --time=00:10:00

    declare test_duration=720 # 12min

    srun \
      --nodes=1 \
      --ntasks=1 \
      stress-ng \
        --cpu ${SLURM_CPUS_PER_TASK} \
        --timeout "${test_duration}" 
    ```

The tasks in `stress_test.sh` do not have sufficient time to finish. After submission the `TimeLimit` can be raised to 15min to allow tasks sufficient time to finish. Assume that `SLURM_ARRAY_JOB_ID=9625003`.

- Update all tasks with:
  ```console
  scontrol update jobid=9625003 TimeLimit=00:15:00
  ```
  For complete tasks you may get a warning, like:
  ```
  9625003_6-11: Job has already finished
  ```
- Update individual tasks:
  ```
  scontrol update jobid=9625003_4 TimeLimit=00:15:00
  ```  



??? info "Examples using `${SLURM_ARRAY_JOB_ID}` and `${SLURM_ARRAY_TASK_ID}`"



With `the `squeue` command y 
- `squeue --job=312_2` will print information about task with `SLURM_ARRAY_TASK_ID=2` of job array with `SLURM_ARRAY_JOB_ID=312`, and
- `squeue --job=312` will print informatino about all jobs of job array with `SLURM_ARRAY_JOB_ID=312`.

Use 9624577_197

- `scancel 312_2` will cancel task with `SLURM_ARRAY_TASK_ID=2` of job array with `SLURM_ARRAY_JOB_ID=312`, and
- `scancel 312` will cancel all tasks of job array with `SLURM_ARRAY_JOB_ID=312`.



## Scheduling of job arrays 

The jobs of an array are submitted in batches, according to the state of the Slurm job manager and 


Job arrays will not create job records immediately for all the tasks in the array. Only jobs for which records are created will count towards the maximum job limit of the user and will be considered for resource scheduling. Thus more jobs can be submitted without encumbering the scheduler.




The option has the form

```
--array=<min ID>-<max ID>:<increment>
```
where

sed "${SLURM_ARRAY_TASK_ID}"'!d' input_file.csv


[Job Arrays](https://slurm.schedmd.com/job_array.html) are supported for `batch` jobs by specifying array index values using `--array` or `-a`option either as a comment inside the SLURM script `#SBATCH --array=<start_index>-<end_index>:<increment>` or by specifying the array range directly when you run the `sbatch` command `sbatch --array=1-100 array_script.sh` 


The option arguments can be either 

- specific array index values `--array=0-31`
- a range of index values `--array=1,3,5,7`
- optional step sizes `--array=1-7:2` (step size 2)
- `<start_index>` an Integer > 0 that defines the Task ID for the first job in the array
- `<end_index>` an Integer > `<start_index>` that defines the Task ID of the last job in the array 
- `<increment>` an Integer > 0 that specifies the increment or step size between the Task IDs it is default to '1' if not specified


```
#!/bin/bash --login
#SBATCH --job-name=array_script
#SBATCH --array=10-30:10
#SBATCH --partition=batch
#SBATCH --qos=normal
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=16
#SBATCH --time=02:00:00
#SBATCH --output=%A_%a.out
#SBATCH --error=%A_%a.err

declare test_duration=${SLURM_ARRAY_TASK_ID}

  srun \
    --nodes=1 \
    --ntasks=1 \
    stress-ng \
      --cpu ${SLURM_CPUS_PER_TASK} \
      --timeout "${test_duration}" 

```

Additionally you can specify the maximum number of concurrent running tasks from the job array by ising  a `%` separator for example `--array=0-31%4` will limit the number of simultaneously running tasks from this job array to 4. Note that the minimum index value is zero and the maximum value is a Slurm configuration parameter (MaxArraySize minus one). 



??? info "Additional enviroment variables for Job Arrays"
    Job arrays will have additional environment variables set





