# GNU parallel in HPC systems

Job campaigns that allocate many small jobs quickly, either using job arrays or custom launcher scripts, should use [GNU parallel](https://www.gnu.org/software/parallel/) to reduce the scheduler load. The Slurm scheduler performs 2 jobs,

- allocates resources for a job,
- launches the [job steps](/jobs/steps/).

Slurm is designed to allocate resources in an allocation loop that runs periodically, usually every 30-180s, depending on its configuration. If many small jobs are in the queue, then operations triggered during the allocation loop, such as backfilling, become expensive. As a result, the scheduling loop can delay past its period, causing the scheduler to appear slow and unresponsive. GNU parallel executes multiple commands in parallel in a single allocation, removing the need to allocate resources and reducing the scheduler load.

!!! info "When should GNU parallel be used?"
    As a rule of thumb, if you are planning to execute jobs campaigns that require more that 10 job allocations per minute, then please consider using [GNU parallel](https://www.gnu.org/software/parallel/).

## Running HPC jobs with GNU parallel

[GNU parallel](https://www.gnu.org/software/parallel/) (command `parallel`)is a shell tool for executing jobs in parallel using one or more computers. A job can be a single command or a small script that has to be run for each of the lines in the input.

- The jobs are forked from the main job when the `parallel` command executes.
- The parallel command blocks until all forked processes exit.
- You can limit the number of jobs that run in parallel; `parallel` implements a form of process pull, where a limited number of processes running in parallel executes the jobs.

### Running a single GNU parallel job per job step

The scheduler is much more efficient in lunching job steps within a job, where resources have been allocated and there is no need to interact with the resource allocation loop. Job steps are lunched within a job with call to the blocking `srun` command, so the executable needs to be launched with the `srun` command within GNU parallel.

```bash
#!/bin/bash --login
#SBATCH --job-name=single_job_step
#SBATCH --partition=batch
#SBATCH --qos=normal
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=16
#SBATCH --time=02:00:00
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

declare test_duration=60

parallel \
  --max-procs "${SLURM_NTASKS}" \
  --max-args 0 \
  srun \
    --nodes=1 \
    --ntasks=1 \
    stress-ng \
      --cpu ${SLURM_CPUS_PER_TASK} \
      --timeout "${test_duration}" \
      ::: {0..1023}
```

This example script launches a single job step per GNU parallel job. The executable `stress-ng` is a stress test program.

- The number of GNU parallel jobs (`--max-procs`) is limited to the number of tasks, `SLURM_NTASKS`, so that there is no overallocation of GNU parallel jobs. Note that if a jobs step is launched without sufficient resources, then the job step fails.
- Each job step is consuming a single task (`--ntasks=1`) that has access to `SLURM_CPUS_PER_TASK` CPUs. The `stress-ng` program requires the explicit specification of the number of CPUs to use for the CPU benchmark with the `--cpu` flag.

??? info "Slurm environment variables (`SLURM_*`)"
    Upon starting a job step, `srun` reads the options defined in a set of environment variables, most of the starting with the prefix `SLURM_`. The scheduler it self will set many of these variables with an allocation for a job is created. Some useful variables set and their corresponding allocation (`sbatch`/`salloc`) flags are the following.

    - `--nodes`: `SLURM_NNODES`
    - `--ntasks`: `SLURM_NTASKS`
    - `--ntasks-per-node`: `SLURM_NTASKS_PER_NODE`
    - `--cpus-per-task`: `SLURM_CPUS_PER_TASK`

    Note that some environment variables are evaluated implicitly even if the corresponding option is not defined for the allocation. For instance in the example above we define `--nodes` and `--ntasks-per-node`, but not `--ntasks`, yet the `SLURM_NTASKS` is set to

    ```
    SLURM_NTASKS = SLURM_NNODES * SLURM_NTASKS_PER_NODE = 4 * 8 = 24
    ```

    and its value can be used in the submission script without defining `--nodes`.

!!! example "Job allocation rate calculation"
    - In this example jobs steps of `1 min` duration (`test_duration`) are being launched in parallel from `4` nodes (`--nodes`) and `8` tasks per node (`--ntasks-per-node`), for a total of `32` tasks.
    - If `32` tasks where launched every minute in distinct jobs the job allocation rate would be above the empirical limit of `10` jobs per minute.
    - Thus, the use of GNU parallel is justified.

### Running multiple GNU parallel jobs per job step

If a jobs contains a massive amounts of very small job steps, it can be limited by the rate in which job steps can be launched. The scheduler stores keep some information for each job step in a database, and with multiple small steps launching in parallel the throughput limits of the database system can exceeded affecting every job in the cluster. In these extreme cases, GNU parallel can limit the number of job steps by grouping multiple GNU parallel jobs in a single job step.

!!! info "When should job step be grouped with GNU parallel jobs?"
    As a rule of thumb, if you are planning to execute jobs that launch more that 1000 job steps per minute, then please consider grouping job steps using [GNU parallel](https://www.gnu.org/software/parallel/).

There are 2 options when lunching multiple GNU parallel jobs in a single jobs step, the GNU parallel jobs of the step can be launched in a script or in a function.

=== "GNU parallel jobs in a function"
    !!! example "Submission script"
        ```bash
        #!/bin/bash --login
        #SBATCH --job-name=multi_job_step_in_function
        #SBATCH --partition=batch
        #SBATCH --qos=normal
        #SBATCH --nodes=4
        #SBATCH --ntasks-per-node=8
        #SBATCH --cpus-per-task=16
        #SBATCH --time=02:00:00
        #SBATCH --output=%x-%j.out
        #SBATCH --error=%x-%j.err

        declare test_duration=5
        declare substeps=$((1024*48+11))
        declare substeps_per_step=48
        declare cpus_per_substep=4

        declare steps=$(( ${substeps} / ${substeps_per_step} ))
        declare remainder_steps=$(( ${substeps} % ${substeps_per_step} ))
        if [ ! "${remainder_steps}" -eq "0" ]; then
          steps=$(( ${steps} + 1 ))
        fi

        run_step() {
          local substeps="${1}"
          local substeps_per_step="${2}"
          local test_duration="${3}"
          local cpus_per_substep="${4}"
          local step_idx="${5}"

          local initial_substep=$(( ${step_idx} * ${substeps_per_step} ))
          local final_substep=$(( ${initial_substep} + ${substeps_per_step} ))
          if [ "${final_substep}" -gt "${substeps}" ]; then
            final_substep=${substeps}
          fi
          final_substep=$(( ${final_substep} - 1 ))

          local max_parallel_substeps=$(( ${SLURM_CPUS_PER_TASK} / ${cpus_per_substep} ))

          parallel \
            --max-procs "${max_parallel_substeps}" \
            --max-args 0 \
              stress-ng \
                --cpu "${cpus_per_substep}" \
                --timeout "${test_duration}" \
                ::: $(seq ${initial_substep} "${final_substep}")
        }

        export -f run_step

        declare final_step=$(( ${steps} - 1 ))

        parallel \
          --max-procs "${SLURM_NTASKS}" \
          --max-args 1 \
          srun \
            --nodes=1 \
            --ntasks=1 \
            bash \
              -c "\"run_step ${substeps} ${substeps_per_step} ${test_duration} ${cpus_per_substep} {1}\"" \
              ::: $(seq 0 ${final_step})
        ```

    When running the GNU parallel job steps in a function, make sure that the function is exported to the environment of `srun` with the `export -f` bash builtin command.

=== "GNU parallel jobs in a script"
    !!! example "Submission script"
        ```bash
        #!/bin/bash --login
        #SBATCH --job-name=multi_job_step_in_script
        #SBATCH --partition=batch
        #SBATCH --qos=normal
        #SBATCH --nodes=4
        #SBATCH --ntasks-per-node=8
        #SBATCH --cpus-per-task=16
        #SBATCH --time=02:00:00
        #SBATCH --output=%x-%j.out
        #SBATCH --error=%x-%j.err

        declare test_duration=5
        declare substeps=$((1024*48+11))
        declare substeps_per_step=48
        declare cpus_per_substep=4

        declare steps=$(( ${substeps} / ${substeps_per_step} ))
        declare remainder_steps=$(( ${substeps} % ${substeps_per_step} ))
        if [ ! "${remainder_steps}" -eq "0" ]; then
          steps=$(( ${steps} + 1 ))
        fi

        declare final_step=$(( ${steps} - 1 ))

        parallel \
          --max-procs "${SLURM_NTASKS}" \
          --max-args 1 \
          srun \
            --nodes=1 \
            --ntasks=1 \
            run_job_step \
              "${substeps}" \
              "${substeps_per_step}" \
              "${test_duration}" \
              "${cpus_per_substep}" \
              ::: $(seq 0 ${final_step})
        ```

    Ensure that the external script `run_job_step` is accessible from submission script, for instance, place both scripts in the same directory.


    !!! example "External job step execution script `run_job_step`"
        ```bash
        #!/bin/bash --login

        declare substeps="${1}"
        declare substeps_per_step="${2}"
        declare test_duration="${3}"
        declare cpus_per_substep="${4}"
        declare step_idx="${5}"

        declare initial_substep=$(( ${step_idx} * ${substeps_per_step} ))
        declare final_substep=$(( ${initial_substep} + ${substeps_per_step} ))
        if [ "${final_substep}" -gt "${substeps}" ]; then
          final_substep=${substeps}
        fi
        final_substep=$(( ${final_substep} - 1 ))

        declare max_parallel_substeps=$(( ${SLURM_CPUS_PER_TASK} / ${cpus_per_substep} ))

        parallel \
          --max-procs "${max_parallel_substeps}" \
          --max-args 0 \
            stress-ng \
              --cpu "${cpus_per_substep}" \
              --timeout "${test_duration}" \
              ::: $(seq ${initial_substep} "${final_substep}")
        ```

    Finally, make sure that the `run_job_step` is executable. The command
    ```console
    chmod u+x run_job_step
    ```
    is usually required to provide the user with [execution permission](/filesystems/unix-file-permissions/#chmod).

---

!!! example "Job step launch rate calculation"
    - Each node contains `128` CPUs, and each job requires `4` CPUs (`cpus_per_substep`); thus each node has `128/4 = 32` slots to execute jobs in parallel.
    - There are `4` nodes (`--nodes`), so with `32` slots per node, there are in total `128` slots to launch job steps in parallel.
    - Each jobs has a duration of `5 sec`, so each slot runs `12` jobs per minute.
    - If every parallel job was a job step, then `12*128 = 1536` jobs steps per minute are launched.
    - This is above the empirical threshold of `1000` job steps per minute, so grouping steps is justified.
    - Grouping creates groups of `48` GNU parallel jobs (`substeps_per_step`) reducing the job step launch rate to `1536/48 = 32` that is safely below the empirical limit of `1000` per minute.

<!--

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

**Tip**: If your tasks are shorter than the scheduler wait time (around **30 to 180 seconds**), it's better to use **GNU Parallel**. Otherwise, use **Slurm Job Arrays**.


---






_Resources_

- [luncher_script_examples.zip](https://github.com/user-attachments/files/21215923/luncher_script_examples.zip)

-->
