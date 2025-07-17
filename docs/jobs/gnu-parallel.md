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


## Launching concurrent programs in one allocation

Many real‑world pipelines need to run several different executables inside a single Slurm allocation. The simplest way to orchestrate them is to provide a space‑ or tab‑delimited command table:

```bash
#!/bin/bash --login
#SBATCH --job-name=many_programs
# ... Slurm directives ...

cat > cmdlist.txt <<'EOF'
fastqc   sample1.fastq.gz
samtools sort sample1.bam -o sample1.sorted.bam
python   train_model.py --epochs 10
EOF

parallel --colsep ' +' --max-procs "${SLURM_NTASKS}" \
        srun --nodes=1 --ntasks=1 {1} {2..}  \
        :::: cmdlist.txt
```

* `{1}` is the program; `{2..}` expands to the remaining columns (its arguments).
* `--colsep ' +'` treats runs of spaces or tabs as column separators.



## Collecting Logs and Monitoring Progress

```bash
parallel --joblog run.log \
         --results results/{#}/ \
         --bar --eta \
         srun ... ::: ${TASKS}
```

* **`run.log`** — TSV with start/finish, runtime, exit status.
* **`results/{#}`** — one directory per task; stdout/stderr captured automatically.
* **`--bar`** — live progress bar; **`--eta`** — estimated completion time.

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


## Performance Tuning Tips

| Symptom                     | Lever                | Example                           |
| --------------------------- | -------------------- | --------------------------------- |
| I/O saturation on shared FS | `--compress`         | pipe‑compress large stdout chunks |
| Many tiny files             | `--results /scratch` | stage results to local SSD first  |
| CPU under‑utilisation       | `--block 10M`        | batch stdin in 10 MB chunks       |
| SSH startup cost            | `--sshloginfile`     | reuse control master via `-M`     |

Benchmark one tweak at a time; use `sar`/`iostat` on compute nodes to confirm bottlenecks.



## Comparing GNU Parallel and Slurm Job Arrays

GNU Parallel and Slurm job arrays both launch many similar tasks, but they solve *different* bottlenecks.

| Use Case                                           | Prefer GNU Parallel                               | Prefer Slurm Array                          |
| -------------------------------------------------- | ------------------------------------------------- | ------------------------------------------- |
| **Interactive/rapid turn‑around** (e.g. dev nodes) | ✔ Parallel runs immediately inside one allocation | ✖ Array needs scheduler cycle for each task |
| **Thousands of ultra‑short jobs**                  | ✔ Drastically reduces queue chatter               | ✖ Creates scheduling overhead               |
| **Need individual Slurm accounting per task**      | ✖ All tasks share one Slurm step                  | ✔ Each array index has its own record       |
| **Mix heterogeneous commands**                     | ✔ Parallel can vary executable per line           | ✖ Arrays assume one script                  |
| **Checkpoint/re‑queue tasks**                      | ✖ Must script custom resume                       | ✔ Native `--array` + `--requeue`            |

A quick rule‑of‑thumb:

> *If the run time of the task is **less than the scheduler cycle** (≈30‑180 s), package the tasks with GNU Parallel.*

---






_Resources_

- [luncher_script_examples.zip](https://github.com/user-attachments/files/21215923/luncher_script_examples.zip)
- 