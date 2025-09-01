# Slurm job steps

A job step is a unit of work launched within a job’s resource allocation. You obtain an allocation with `sbatch` or `salloc`, then create one or more steps with `srun` to execute commands using some or all of the allocated resources.


## Job allocation vs. Job step

- Job allocation: resources reserved for the job (nodes/CPUs/memory/GPUs).

- Job step: actual processes launched within a job which consume the job resources. The job steps can execute in serial or parallel given that enough resources are available.

- Multiple steps can run sequentially or concurrently inside the same allocation.

## How steps are created

- `sbatch`: submits a non-interactive batch job. The batch script runs in a special batch step on the first node of the allocation. Additional parallel work must be launched via srun.

- `salloc`: creates an interactive allocation. The user’s shell/command runs in a special interactive step on the first node. Further parallel work is launched via srun inside that allocation.

- `srun`: inside an allocation, launches a regular job step. You can launch multiple steps, sequentially or in parallel.

## Step types

- batch step: created for jobs submitted with sbatch; runs the batch script.

- interactive step: created for jobs started with salloc, runs the interactive shell/command provided to salloc.

- extern step: optional step used to account for processes not started by Slurm within the allocation (e.g., daemons, ssh). Presence depends on site configuration (proctrack/cgroup, task plugin, containment settings).

- regular (srun) steps: created by each srun invocation inside the allocation.

Identifiers appear as JobID.StepID (e.g., 123456.0, 123456.batch, 123456.interactive, 123456.extern). Regular step IDs are numbered starting at 0 and increment per srun.

## Why steps matter

- Resource sharing: Each step consumes a portion of the job’s allocation; concurrent steps can oversubscribe CPUs/GPUs if not sized carefully.

- Accounting/monitoring: Each step has its own status and resource usage.

- Placement/binding: Steps define how tasks are distributed and bound on nodes.

## Always use srun for parallel work

Commands not launched with srun run only in the batch or interactive step (typically on the first node). Use srun to utilize the full allocation across nodes and tasks.

## Common srun options for steps

- `--ntasks` (-n),`--nodes` (-N), `--ntasks-per-node`, `--cpus-per-task` (-c)

- `--gpus`, `--gpus-per-node`, `--gpus-per-task`

- `--exclusive` (prevent CPU sharing across concurrent steps)

- `--oversubscribe` (allow sharing)

- `--hint`, `--cpu-bind`, `--distribution` (placement/binding)

- `--job-name`, `--output/--error`, `--label` (naming and I/O)

Each step must fit within the job’s allocated resources.

## Monitoring and control

- List job and steps: `squeue -j <jobid> -s`

- Show job details: `scontrol show job <jobid>`

- Show step details: `scontrol show step <jobid>.<stepid>`

- Live step stats: `sstat -j <jobid>.<stepid> --format JobID,MaxRSS,AveCPU`

- Historical accounting: `sacct -j <jobid> --format JobID,JobName,State,Elapsed,CPUTime,MaxRSS,ReqTRES,AllocTRES`

- Cancel a step: `scancel <jobid>.<stepid>`

- Cancel a job: `scancel <jobid>`

```
$ sacct -j 9457023 --format JobID,JobName,State,Elapsed,CPUTime,MaxRSS,ReqTRES,AllocTRES
9457023      single_pr+  COMPLETED   00:01:06   09:23:12            billing=7+ billing=7+ 
9457023.bat+      batch  COMPLETED   00:01:06   02:20:48    181096K            cpu=128,m+ 
9457023.ext+     extern  COMPLETED   00:01:06   09:23:12          0            billing=7+ 
9457023.0     stress-ng  COMPLETED   00:01:01   00:16:16     46320K            cpu=16,me+ 
9457023.1     stress-ng  COMPLETED   00:01:01   00:16:16     38124K            cpu=16,me+ 
9457023.2     stress-ng  COMPLETED   00:01:01   00:16:16     46628K            cpu=16,me+ 
9457023.3     stress-ng  COMPLETED   00:01:01   00:16:16     38480K            cpu=16,me+ 
9457023.4     stress-ng  COMPLETED   00:01:01   00:16:16     38092K            cpu=16,me+ 
9457023.5     stress-ng  COMPLETED   00:01:01   00:16:16     38244K            cpu=16,me+ 
9457023.6     stress-ng  COMPLETED   00:01:01   00:16:16     38524K            cpu=16,me+ 
9457023.7     stress-ng  COMPLETED   00:01:01   00:16:16     47332K            cpu=16,me+ 
9457023.8     stress-ng  COMPLETED   00:01:01   00:16:16     38280K            cpu=16,me+ 
9457023.9     stress-ng  COMPLETED   00:01:01   00:16:16     44344K            cpu=16,me+ 
9457023.10    stress-ng  COMPLETED   00:01:01   00:16:16     38364K            cpu=16,me+ 
[...]   

```


## Step environment variables

Common variables available inside a step:

- SLURM_JOB_ID, SLURM_JOB_NODELIST

- SLURM_STEP_ID (numeric ID or batch/interactive/extern)

- SLURM_STEP_NODELIST, SLURM_STEP_NUM_NODES

- SLURM_NTASKS, SLURM_NTASKS_PER_NODE, SLURM_CPUS_PER_TASK

## Input/output of steps

- By default, step stdout/stderr go to the job’s output/error.

- Control per-step I/O, e.g.:
  
  - srun --output=step_%j.%2t.out --error=step_%j.%2t.err <cmd>
  
  - srun --label <cmd> (prefix lines by task rank)

Placeholders include %j (jobid), %t (task id), %2t (zero-padded).

## Resource placement and binding

- Distribution: `--nodes`, `--ntasks-per-node`, `--distribution=block|cyclic|...`

- CPU binding: `--cpu-bind=cores|threads|rank`, `--hint=nomultithread|compute_bound`

- GPUs: request at job level (e.g., #SBATCH --gpus=4) and size each step with --gpus*, ensuring fit within allocation.

## Best practices

- Launch parallel work with srun; don’t rely on implicit shell execution.

- Size steps explicitly (tasks, CPUs per task, GPUs).

- Use --exclusive for concurrent steps that must not share CPUs; use --oversubscribe only when intentional.

- Name steps for clarity (srun --job-name=...).

- Use sacct/sstat to collect per-step accounting.

- For many small tasks, consider srun --multi-prog or job arrays.

- If you use GNU Parallel inside allocations, wrap commands with srun so tasks run as tracked steps; see the [GNU Parallel](jobs/gnu-parallel/) page for more details.

## References

- https://slurm.schedmd.com/job_launch.html
- https://slurm.schedmd.com/srun.html
