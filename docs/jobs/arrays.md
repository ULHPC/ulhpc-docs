# Job arrays in HPC systems

[Job arrays](https://slurm.schedmd.com/job_array.html) is a mechanism for submitting and managing collections of similar jobs. All jobs in an array have the same options in terms of scheduler resources, as they are submitted with the same `sbatch` options and directives.

!!! info "When to use job arrays"
    A naive way to submit multiple jobs is to programmatically submit the jobs with a custom script. This however can quickly hit the [maximum job limit](/slurm/qos/#available-qoss) (`MaxJobPU`), which is `100` jobs per user in the `normal` QoS. If your jobs share the same options, then consider using job arrays. Job arrays create job records for task progressively, so they will help you keep within `MaxJobPU` while reducing the load for the scheduler.

!!! warning "When _not_ to use job arrays"
    Every job in a job array requires an allocation from the scheduler, which is an expensive operation. If you plan to submit many small jobs in an array that require the allocation of [more than _10 jobs per minute_](#launch-rate-calculations), please use [GNU parallel](/jobs/gnu-parallel/) to batch multiple tasks in a single job allocation.

## Using job arrays

The job array feature of Slurm groups similar jobs and provides functionality for managing the group of jobs. A fundamental concept for managing and organizing the is the task index value (task ID). Every task in the job array is a Slurm job and is assigned a task ID which is used to refer to the Slurm job in the context of the job array. The following environment variables are set in job array tasks on top of the usual `SLURM_JOB_ID` that is available on all jobs.

- `SLURM_ARRAY_JOB_ID` is the Slurm job ID of the whole job array.
- `SLURM_ARRAY_TASK_ID` is the task ID of the current Slurm job.
- `SLURM_ARRAY_TASK_COUNT` is the total number of tasks in the job array.
- `SLURM_ARRAY_TASK_MAX` is the largest task ID in the job array
- `SLURM_ARRAY_TASK_MIN` is the smallest task ID in the job array.

??? info "Inner workings of jobs arrays and the job ID of the whole array"
    When a job array is submitted to Slurm, [only one job record is created](https://slurm.schedmd.com/job_array.html#squeue). The `SLURM_JOB_ID` of this initial job will then be the `SLURM_ARRAY_JOB_ID` of the whole array. Additional jobs records are then created by the initial job. The [`squeue`](#viewing-array-job-status) command shows that additional jobs appear in the queue as their records are created by the initial job, and the initial [job ID string changes](#managing-tasks-and-arrays) to reflect the progress of the job array execution. This gradual submission of jobs ensures that the user remains within the limits specified by the Slurm configuration. For instance in a job array with `400` jobs, up to 100 jobs will be launched in parallel in the [`normal` QoS](/slurm/qos/#available-qoss) that has a limit (`MaxJobPU`) of 100 jobs.

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

where the `--array` is used to control how many Slurm jobs are created. Inside the `job_array_script.sh` the `SLURM_ARRAY_TASK_ID` can be used to control to differentiate the operation of the script. The number of jobs that runs in parallel is controlled using the suffix
```
sbatch --array=<task list>%<number of parallel jobs> job_script.sh
```
where `<number of parallel jobs>` is the maximum number of jobs that will run in parallel.

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

    A task list is _valid_ if all task IDs in the list are in the range `0-(MaxArraySize-1)`.

If you job specification has a syntax error or lists tasks with ID outside the range `0-(MaxArraySize-1)`, then the array job submission fails immediately with an error message.

!!! warning "Job execution order"
    The task ID simply provides a way to differentiate the job array tasks and their behavior, there is no guaranty in which order tasks will run. If you need your job array tasks to run in a particular order consider using job dependencies.

### Managing tasks and arrays

A combination of the `${SLURM_ARRAY_TASK_ID}` and `${SLURM_ARRAY_JOB_ID}` can replace the `${SLURM_JOB_ID}` of job array tasks in Slurm commands such as `scontrol` and `squeue`.

- Use the `${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}` to refer to a task of the job array.
- Use the `${SLURM_ARRAY_JOB_ID}` to refer to all the tasks of the job array collectively.

Each array job, is associated with a job ID string that contains information about the status of the array. The job ID string is formatted using the [_task list_](#submitting-a-job-array) as follows.
```
<${SLURM_ARRAY_JOB_ID}>_[<task list>]
```

As the execution of the job array with job `${SLURM_ARRAY_JOB_ID}` progresses, the job ID string is updated to reflect the progress.

!!! example "The job array ID string"
    Assume that a job
    ```console
    sbatch --array=0-399%4 job_script.sh
    ```
    is submitted and gets assigned `SLURM_ARRAY_JOB_ID=625449`.

    - The initial job ID string is: `9625449_[0-399%4]`
    - After tasks `0-23` are executed, the new ID string is: `9625449_[24-399%4]`

A few example with the most representative use for job ID strings cases follow.

#### Canceling job arrays and job array tasks

With `scancel` some of the array tasks or all the array can be cancelled. Assume that array with `SLURM_ARRAY_JOB_ID=9624577` is running.

- To cancel the whole job array use:
  ```console
  scancel 9624577
  ```
- To cancel the job array task with `SLURM_ARRAY_TASK_ID=197` in particular use:
  ```console
  scancel 9624577_197
  ```

!!! info "Syntax shortcuts for job ID strings"
    When addressing a single task ID, the square brackets in the job ID string can be dropped. For instance,
    ```
    9624577_[197]
    ```
    is equivalent to
    ```
    9624577_197
    ```
    in all cases where job ID strings appear.

#### Viewing array job status

The `squeue` can access the job ID string for the whole array and task ID strings of individual tasks. Assume that array with `SLURM_ARRAY_JOB_ID=9624577` is running.

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

## Job array scripts

Consider a job array script designed to stress test a set of network file systems mounted on `${FILE_SYSTEM_PATH_PREFIX}_0` to `${FILE_SYSTEM_PATH_PREFIX}_255`. The job array launch script is the following.

!!! example "io_test.sh"
    ```
    #!/bin/bash --login
    #SBATCH --job-name=array_script
    #SBATCH --array=0-255%16
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=16
    #SBATCH --time=00:30:00
    #SBATCH --output=%x-%A_%a.out
    #SBATCH --error=%x-%A_%a.err

    declare test_duration=20m

    srun \
      stress-ng \
        --timeout "${test_duration}" \
        --iomix "${SLURM_CPUS_PER_TASK}" \
        --temp-path "${FILE_SYSTEM_PATH_PREFIX}_${SLURM_ARRAY_TASK_ID}" \
        --verify \
        --metrics
    ```

This job script a job array with `256` tasks, where up to `16` tasks will run in parallel. Job arrays provide two extra [filename patterns](https://slurm.schedmd.com/sbatch.html#SECTION_FILENAME-PATTERN) that can be used to name output files (defined with the `--output` and `--error` options). This patterns are,

- `%A` that contains the master job allocation number `SLURM_ARRAY_JOB_ID`, and
- `%a` that contains the task index number `SLURM_ARRAY_TASK_ID`.

### Launch rate calculations

The `io_test.sh` script launches $16$ jobs in parallel, and each job has a duration of $20$ minutes. This results in a job launch rate of

$$
  \frac{16 ~ \text{jobs}}{20 ~ \text{min}} = 0.8 ~ \text{jobs per minute}
$$

that is lower than the rule of thumb limit of $10$ jobs per minute. Imagine for instance that we do not limit the maximum number of tasks that can run in parallel by overriding the `--array` option.
```console
sbatch --array=0-255 io_test.sh
```
Then, up to all $256$ can run in parallel and each job has a duration of $20$ minutes, which would result in a peak allocation rate of

$$
  \frac{256}{20} = 12.8 ~ \text{jobs per minute}
$$

a lunch rate that is momentarily above the rule of rule of thumbs limit of $10$ jobs per minute. Therefore, a limit in the maximum number of parallel running jobs should be considered.

!!! warning "Limiting the job launch rate"
    The [`MaxArraySize`](#using-job-arrays) limit in UL HPC systems makes it difficult to exceed the suggested limit of job launches per minute. However, in case you need to launch more that 1000 jobs or you expect a job launch rate that is more that 10 jobs per minute, please consider using [GNU parallel](/jobs/gnu-parallel/).

### Writing launch scripts

Array indices can be used to differentiate the input of a task. In the following example, a script creates programmatically a job array to run a parametric investigation on a 2-dimensional input, and then launches the job array.

!!! example "`launch_parammetric_analysis.sh`"
    ```bash
    #!/usr/bin/bash --login

    declare max_parallel_tasks=16
    declare speed_step=0.01

    generate_commands() {
      local filename="${1}"

      echo -n > ${filename}
      declare nx ny vx vy
      for nx in $(seq 1 10); do
        for ny in $(seq 1 10); do
          vx="$(echo "${nx}"*"${speed_step}" | bc --mathlib)"
          vy="$(echo "${ny}"*"${speed_step}" | bc --mathlib)"
          echo "simulate_with_drift.py '${vx}' '${vy}' --output-file='speed_idx_${nx}_${ny}.dat'" >> ${filename}
        done
      done
    }

    generate_submission_script() {
      local submission_script="${1}"
      local command_script="${2}"

      local n_commands="$(cat ${command_script} | wc --lines)"
      local max_task_id="$((${n_commands} - 1))"

      cat > job_array_script.sh <<EOF
    #!/bin/bash --login
    #SBATCH --job-name=parametric_analysis
    #SBATCH --array=0-${max_task_id}%${max_parallel_tasks}
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=16
    #SBATCH --time=0-10:00:00
    #SBATCH --output=%x-%A_%a.out
    #SBATCH --error=%x-%A_%a.err

    module load lang/Python

    declade command="\$(sed "\${SLURM_ARRAY_TASK_ID}"'!d' ${command_script})"

    echo "Running commnand: \${command}"
    eval "srun python \${command}"
    EOF
    }

    generate_commands 'commands.sh'
    generate_submission_script 'job_array_script.sh' 'commands.sh'

    sbatch job_array_script.sh
    ```

Run the `launch_parammetric_analysis.sh` script with the bash command.

```console
bash launch_parammetric_analysis.sh
```

??? info "Avoiding script generation"
    Script generation is a complex and error prone command. In this example script generation is unavoidable, as the whole parametric analysis cannot run in a single job of the [`normal` QoS](/slurm/qos/#available-qoss) which has the default maximum wall time (`MaxWall`) of 2 days. The expected runtime on each simulation would be about $0.25$ to $0.5$ of the maximum wall time (`--time`) which is set at 10 hours.

    If all the parametric analysis can run within the 2 day limit, then consider running the analysis in a single allocation using [GNU parallel](/jobs/gnu-parallel/). You can then generate the command file and lauch the simulation all from a single script in a single job allocation.
