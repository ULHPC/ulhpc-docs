## Running jobs with GNU parallel

The Slurm scheduler performs 2 jobs,

- allocate resources for a job (allocation),
- lunches the job steps.

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

_Resources_

- [luncher_script_examples.zip](https://github.com/user-attachments/files/21215923/luncher_script_examples.zip)
