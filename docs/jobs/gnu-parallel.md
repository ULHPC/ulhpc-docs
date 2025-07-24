[GNU Parallel](https://www.gnu.org/software/parallel/) is a tool for executing tasks in parallel, typically on a single machine. When coupled with the Slurm command `srun`, `parallel` becomes a powerful way of distributing a set of tasks amongst a number of workers. This is particularly useful when the number of tasks is significantly larger than the number of available workers (i.e. `$SLURM_NTASKS`), and each tasks is independent of the others.

??? info "Example usage"

    ```bash
    $ parallel -j 5 'srun --exclusive -N1 -n1 echo Task {} on $(hostname)' ::: {1..5}
    Task 1 on access1.aion-cluster.uni.lux
    Task 4 on access1.aion-cluster.uni.lux
    Task 5 on access1.aion-cluster.uni.lux
    Task 3 on access1.aion-cluster.uni.lux
    Task 2 on access1.aion-cluster.uni.lux
    ```
    The default argument separator `:::` separate your command from your inputs. Inputs can either be a list separated by spaces, or a range using brace expansions. Place `{}` replacement string where you want your inputs to go inside your command.

## Running jobs with GNU parallel

The Slurm scheduler performs 2 jobs,

- allocates resources for a job (allocation),
- launches the job steps.

The job steps are the actual processes launched within a job which consume the job resources. Resources can be entities like nodes, CPU cores, GPUs, and memory allocated for the job. The job steps can execute in serial or parallel given that enough resources are available.

The Slurm scheduler is designed to allocate resources in an allocation loop that runs periodically, usually every 30-180sec depending on the Slurm configuration. The resource allocation loop is quite time consuming as the scheduler is configured to perform operations such as back-filling. If a lot of small jobs are in the queue, they tend to trigger expensive operations such as back-filling, and can delay the scheduling loop past its usual period. The end result is a scheduler with sluggish response.

To avoid multiple small jobs, we can schedule multiple jobs in a single allocation.

```bash
#!/bin/bash --login
#SBATCH --job-name=single_process
#SBATCH --partition=batch
#SBATCH --qos=normal
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=16
#SBATCH --time=02:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --exclusive
#SBATCH --mem=0

declare stress_test_duration=160

parallel --max-procs "${SLURM_NTASKS}" --max-args 0 srun --nodes=1 --ntasks=1 stress --cpu 16 --timeout "${stress_test_duration}" ::: {0..255}
```

The scheduler is much more efficient in lunching job steps within a job, as the resources have been allocated and there is no need to interact with the resource allocation loop. Job steps are lunched in blocking calls within a job whenever a `srun` command is executes in the job.

However, even there are limit even in the number of job steps per job, as the scheduler needs to keep some information for each job step and multiple small jobs steps encumber the scheduler database. To reduce the number of job steps, we can group smaller jobs into groups of jobs lanced with parallel within a job step.

There are 2 options when lunching multiple scripts in a single step, we can launch them in an external script or within functions. When using an external script, call the external script from your main script

```bash
#!/bin/bash --login
#SBATCH --job-name=multi_process
#SBATCH --partition=batch
#SBATCH --qos=normal
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=16
#SBATCH --time=02:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --exclusive
#SBATCH --mem=0

declare stress_test_duration=5
declare operations_per_step=256

parallel --max-procs "${SLURM_NTASKS}" --max-args 0 srun --nodes=1 --ntasks=1 run_job_step "${operations_per_step}" "${stress_test_duration}" ::: {0..255}
```

and ensure that the external script is accessible, for instance placed in the same directory:

```bash
#!/bin/bash --login
# Contents of `run_job_step`

declare total_operations="${1}"
declare test_duration="${2}"
declare final_operation=$((${total_operations}-1))

parallel --max-procs 4 --max-args 0 stress --cpu 4 --timeout "${test_duration}" ::: $(seq 0 "${final_operation}")
```

When running the job in a function, make sure that the function is exported to the environment of `srun`:

```bash
#!/bin/bash --login
#SBATCH --job-name=function_multi_process
#SBATCH --partition=batch
#SBATCH --qos=normal
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=16
#SBATCH --time=02:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err
#SBATCH --exclusive
#SBATCH --mem=0

declare stress_test_duration=5
declare operations_per_step=256

run_step() {
  local total_operations="${1}"
  local test_duration="${2}"
  local final_operation=$((${total_operations}-1))

  parallel --max-procs 4 --max-args 0 stress --cpu 4 --timeout "${test_duration}" ::: $(seq 0 "${final_operation}")
}

export -f run_step

parallel --max-procs "${SLURM_NTASKS}" --max-args 0 srun --nodes=1 --ntasks=1 bash -c "\"run_step ${operations_per_step} ${stress_test_duration}\"" ::: {0..255}
```

!!! tip "Notice how `srun` works"
    
    For `parallel` jobs `srun` command plays an important role of starting the parallel program and setting up the environment. Each srun invocation becomes a separate SLURM job step within your overall allocation meaning it will start as many instances of the program as requested with the `--ntasks` option on the CPUs that were allocated for the job. 



To run jobs successfully, the resources you request from Slurm (#SBATCH directives) must match what your commands (parallel, srun, and your program) actually use. See [Resource Allocation Guidelines](https://hpc-docs.uni.lu/slurm/launchers/#resource-allocation-guidelines) 


## Launch concurrent Programs in One Allocation

Often, real workflows need to run different commands or executables within one job. GNU parallel can take a command list from a file and execute each line. For example, create `cmdlist.txt` (tab-separated, or use multiple spaces) listing programs and their arguments for each task:

```txt
python3	data_processing.py	sample1.dat	sample1.proc
python3	model_training.py	sample1.csv	sample1.model
```

*(Use tabs or multiple spaces between columns)*

Each line defines a program and its arguments. We can then write a Slurm batch script to execute each line in parallel:

```bash
#!/bin/bash --login
#SBATCH --job-name=conc_programs
#SBATCH --partition=batch
#SBATCH --qos=normal
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=16
#SBATCH --time=02:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

parallel --colsep '\t' --jobs "$SLURM_NTASKS" --results parallel_logs/ srun -N1 -n1 {1} {2} :::: cmdlist.txt
```

- `{1}` is the program; `{2..}` expands to the remaining columns (its arguments).
- `--colsep ' +'` treats runs of spaces or tabs as column separators.

if you want to pass each line as a full command use:
```bash
parallel --jobs "$SLURM_NTASKS" --results parallel_logs/ srun -N1 -n1 {} ::: cmdlist.txt
```
- `{}` is replaced by the entire line (the full command and its arguments).


## Collect Logs and Monitor Progress

```bash
parallel --joblog run.log --results results/{#}/ --bar --eta srun ... ::: ${TASKS}
```

- `run.log` — records start/finish time, runtime duration, exit status.
- `results/{#}` — create a separate directory per task; stdout/stderr captured automatically.
- `--bar` — live progress bar
- `--eta` — estimated completion time



To check the actual state of your job and all it's steps you can use `sacct` command.  

```
sacct -j $SLURM_JOBID --format=JobID,JobName,State,ExitCode,Elapsed
$ sacct -j 8717582 --format=JobID,JobName,State,ExitCode,Elapsed
JobID           JobName      State ExitCode    Elapsed 
------------ ---------- ---------- -------- ---------- 
8717582      single_pr+    RUNNING      0:0   00:00:52 
8717582.bat+      batch    RUNNING      0:0   00:00:52 
8717582.ext+     extern    RUNNING      0:0   00:00:52 
8717582.0        stress    RUNNING      0:0   00:00:51 
8717582.1        stress    RUNNING      0:0   00:00:51 
8717582.2        stress    RUNNING      0:0   00:00:51 
8717582.3        stress    RUNNING      0:0   00:00:51 
8717582.4        stress    RUNNING      0:0   00:00:51 
8717582.5        stress    RUNNING      0:0   00:00:51 
8717582.6        stress    RUNNING      0:0   00:00:51 
8717582.7        stress    RUNNING      0:0   00:00:51 
8717582.8        stress    RUNNING      0:0   00:00:51 
8717582.9        stress    RUNNING      0:0   00:00:51 
8717582.10       stress    RUNNING      0:0   00:00:51
[...] 
```

## Error Handling and Automatic Retries

Enable bounded retries for flaky tasks:

```bash
# /!\ ADAPT <n> to set the number of automatic retries
parallel --retries <n> --halt now,fail=1 srun ... ::: ${TASKS}
```

- `--retries 3` — retries each task up to 3 times if it fails.
- `--halt now,fail=1` — If any task fails after all retries, GNU Parallel will immediately stop all running and pending tasks, aborting the whole job allocation.

For _checkpointable_ binaries, you can resume failed tasks using the joblog:

```bash
parallel --joblog run.log --resume-failed ...
```
`--resume-failed` — Only reruns the tasks that failed (according to the log file).

## When to Use GNU parallel

Use GNU parallel when:

- You have many short or heterogeneous tasks (different commands or arguments per task).

- You want to minimize scheduler overhead by running many tasks within a single job allocation.

- You need to quickly retry or resume failed tasks using GNU Parallel’s joblog.

- You want interactive or rapid prototyping without waiting for the scheduler.

- You want to efficiently utilize allocated resources by launching multiple commands concurrently.

When not to use GNU parallel:

- When you need each task to be tracked individually by the scheduler for accounting or dependencies.

- When your tasks are long-running and require advanced scheduler features like job dependencies or per-task resource allocation.

- When your workflow is already well-suited to Slurm’s built-in job array features.

---

> **Tip**: If your tasks are shorter than the scheduler wait time (around **30 to 180 seconds**), it's better to use **GNU parallel**. Otherwise, use **Slurm Job Arrays**.

---

_Resources_

- [luncher_script_examples.zip](https://github.com/user-attachments/files/21215923/luncher_script_examples.zip)
