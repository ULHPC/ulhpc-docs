# Job Arrays in HPC systems

In HPC systems, cluster policy may enforce job submission limits in order to protect the scheduler from overload.

When you want to submit multiple jobs that share the same initial options (e.g. qos, time limit etc.) but with different input parameters the naive way is to manually or programatically generate and submit multiple scripts with different parameters each with its own sbatch job allocation. But doing this may quickly hit the cluster limits and risks having your job submission rejected. 

If you are planning to execute jobs campaigns that require more than 10 job allocations per minute then consider [GNU parallel](/jobs/gnu-parallel/) but if your job allocations are less than 10 jobs per minute consider using [Job Arrays](https://slurm.schedmd.com/job_array.html). 

Job arrays provides you with a mechanism for submitting and managing collections of similar jobs quickly and easily, while still giving you fine control over the maximum simultaneously running tasks from the Job array.

## Using Job Arrays

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

    - `SLURM_ARRAY_JOB_ID`: job ID of the array
    - `SLURM_ARRAY_TASK_ID`: job array index value
    - `SLURM_ARRAY_TASK_COUNT`: the number of tasks in the job array
    - `SLURM_ARRAY_TASK_MAX`: the highest job array index value
    - `SLURM_ARRAY_TASK_MIN`: the lowest job array index value
