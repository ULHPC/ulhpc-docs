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


To run jobs successfully, the resources you request from Slurm (#SBATCH directives) must match what your commands (parallel, srun, and your program) actually use. Let's break down the previous examples to see how the numbers connect.


??? info "How the Resources Are Calculated and Used"

    1.  **Total Tasks (The "Slots" for Work)**
        *   We request `#SBATCH --nodes=4` and `#SBATCH --ntasks-per-node=8`.
        *   Slurm calculates the total number of tasks it will create for our job: `4 nodes × 8 tasks/node = 32 total tasks`.
        *   This total value is automatically stored in the `$SLURM_NTASKS` environment variable.

    2.  **CPUs for Each Task**
        *   We request `#SBATCH --cpus-per-task=16`.
        *   This tells Slurm: "For each of the 32 tasks, reserve **16 dedicated CPU cores**." This is the resource pool for a single piece of work.

    3.  **GNU Parallel's Role**
        *  We use `parallel --max-procs "${SLURM_NTASKS}" ...`
        *  This instructs GNU Parallel to run up to `$SLURM_NTASKS` (which is 32) commands concurrently. It will launch 32 `srun` commands at once, filling every available task "slot" that Slurm prepared for us.

     4.  **The `srun` Command (The Job Step)**
        *  The command being run by `parallel` is `srun --nodes=1 --ntasks=1 ...`
        * Each of these `srun` commands consumes exactly **one** of the 32 available task slots.

     5.  **The `stress` Program (The Actual Work)**
        * Finally, the program being run is `stress --cpu 16`.
        * This is the crucial link: we instruct our program to use **16 CPUs**, which perfectly matches the `#SBATCH --cpus-per-task=16` directive. The `srun` command ensures this `stress` test runs within the 16 cores that Slurm reserved for it.


> **The Golden Rule:** The `--cpu` (or `--threads`, etc.) value in your final program should match the value you requested in `#SBATCH --cpus-per-task`. This ensures your job uses exactly what it asked for, leading to maximum efficiency and stability.



## Launch concurrent Programs in One Allocation

Often, real workflows need to run different commands or executables within one job. GNU Parallel can take a command list from a file and execute each line. For example, create a tab-separated file `cmdlist.txt` listing programs and their arguments for each task:

```txt
# prog  args
python3 data_processing.py    sample1.dat sample1.proc
python3 model_training.py    sample1.csv sample1.model
```

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

* `{1}` is the program; `{2..}` expands to the remaining columns (its arguments).
* `--colsep ' +'` treats runs of spaces or tabs as column separators.



## Collect Logs and Monitor Progress

```bash
parallel --joblog run.log \
         --results results/{#}/ \
         --bar --eta \
         srun ... ::: ${TASKS}
```

* `run.log` — TSV with start/finish, runtime, exit status.
* `results/{#}` — one directory per task; stdout/stderr captured automatically.
* `--bar` — live progress bar; **`--eta`** — estimated completion time.

Tail the bar in real time:

```bash
tail -f --pid=${PARALLEL_PID} parallel_bar.log
```


## Error Handling and Automatic Retries

Enable bounded retries for flaky tasks:

```bash
parallel --retries 3 --halt now,fail=1 \
         srun ... ::: ${TASKS}
```

* `--retries 3` — attempt each job up to 3 times.
* `--halt now,fail=1` — abort the whole allocation if any task keeps failing.

For *checkpointable* binaries, pair Parallel’s resume file with `--resume`:

```bash
parallel --joblog run.log --resume-failed ...
```


## GNU Parallel vs Slurm Job Arrays

| **Use Case**                             | **Use GNU Parallel**                          | **Use Slurm Job Arrays**                        |
|------------------------------------------|-----------------------------------------------|--------------------------------------------------|
| Interactive or quick testing             | Runs tasks immediately                        | May wait for each task to be scheduled           |
| Thousands of very short tasks            | Reduces load on the scheduler                 | Can overload the scheduler                       |
| Need individual job tracking             | All tasks share the same job record           | Each task has its own job record                 |
| Different commands per task              | Can run different commands in each task       | Usually runs the same script for all tasks       |
| Restart failed tasks easily              | Needs manual scripting to resume tasks        | Has built-in support for retrying failed tasks   |

---

> **Tip**: If your tasks are shorter than the scheduler wait time (around **30 to 180 seconds**), it's better to use **GNU Parallel**. Otherwise, use **Slurm Job Arrays**.


---






_Resources_

- [luncher_script_examples.zip](https://github.com/user-attachments/files/21215923/luncher_script_examples.zip)
