# Job dependencies

Interdependent jobs can be submitted in Slurm systems to perform tasks with dependencies between their various steps. Job dependencies are useful for instance in managing data. 

## Specifying job dependencies

Job dependencies are inserted with the [`--dependency`](https://slurm.schedmd.com/sbatch.html#OPT_dependency) (`-d` in short format) option flag.

```shell 
$ sbatch --dependency=<dependency_list> script.sh
```

The `<dependency_list>` object is composed by a number of dependencies in a comma (`,`) separated list
```
<dependency_list> = <dependency>[,<dependency>...]
```
if _all_ dependencies must be satisfied, or question mark (`?`) separated list
```
<dependency_list> = <dependency>[?<dependency>...]
```
if _any_ of the dependencies is sufficient. _Only one separator may be used_.

When a job with dependencies is queued, the job is not considered for execution until its dependencies are satisfied. The scheduler takes into account the end time of dependencies to reserve resources for depended jobs.

!!! info "Job dependencies"


    | Dependency                                  | Description                                                                                                                                                                                                      |
    |:--------------------------------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
    | `after:job_id[+time][:jobid[+time]...]`     | Enable after the listed jobs start or are canceled; wait `time` minutes before starting, start imediatelly if no `time` is specified).                                                                           |
    | `afterany:job_id[:jobid...]`<sup>[1]</sup>  | Enable after the specified jobs have terminated.                                                                                                                                                                 |
    | `afterburstbuffer:job_id[:jobid...]`        | Enable after the specified jobs have terminated and any associated burst buffer stage out operations have completed.                                                                                             |
    | `afternotok:job_id[:jobid...]`              | Enable after the specified jobs have terminated in some failed state (non-zero exit code, node failure, timed out, etc).                                                                                         |
    | `afterok:job_id[:jobid...]`                 | Enable after the specified jobs have successfully executed (ran to completion with an exit code of zero).                                                                                                        |
    | `singleton`                                 | Enable after any previously launched jobs sharing the same job name and user have terminated. In other words, only one job by that name and owned by that user can be running or suspended at any point in time. |
    | `aftercorr:job_id[:jobid...]`<sup>[2]</sup> | Enable _after the corresponding_ task ID in `job_id` array has completed successfully (ran to completion with an exit code of zero).                                                                             |
    
    1. The default dependency type.
    2. Applicable only to job arrays.

## Submitting jobs with dependencies

For instance, is you want `second_job.sh` to start after `first_job.sh` has completed successfully, then issue the commands:

```shell
$ first_job_id=$(sbatch --parsable first_job,sh)
$ sbatch --dependency=afterok:${first_job_id} second_job.sh
```

If you want `dependant_job.sh` to start after `job_0.sh` and `job_1.sh` have completed successfully, then issue the commands:

```shell
$ job_0_id=$(sbatch --parsable job_0.sh)
$ job_1_id=$(sbatch --parsable job_1.sh)
$ sbatch --dependency=afterok:${job_0_id},afterok:${job_1_id} dependant_job.sh
```

As the number of dependent job increases, it pays off to create a submission script with all the dependency information. For instance:

!!! info "Contents of `submit_jobs.sh`"

    ```bash
    #!/bin/bash --login
    
    declare copy_job_id=$(sbatch --parsable copy_data.sh)
    declare analysis_job_0_id=$(sbatch --parsable --dependency=afterok:${copy_job_id} analysis_job_0.sh)
    declare analysis_job_1_id=$(sbatch --parsable --dependency=afterok:${copy_job_id} analysis_job_1.sh)
    sbatch --dependency=afterok:${analysis_job_0_id},${analysis_job_1_id} cleanup_job.sh
    ```

Then all the jobs are submitted with the command:

```shell
$ bash submit_jobs.sh
```

??? info "The `--parsable` option of `sbatch`"

    With the option `--parsable` the `sbatch` command return a single string with the job ID that can be stored in a shell variable. For instance without `--parsable`, the output of the batch submission is
    ```shell
    $ sbatch job.sh
    Submitted batch job 12345
    ```
    and with `--parsable` the output is
    ```
    $ sbatch --parsable job.sh
    12345
    ```
    that is only the job ID.

## Examples

These are 2 cases that appear often in our systems. The first is an example of transferring data between the available storage tiers. The second involves running a light database to support a serries of jobs that are submitted automatically for the duration of a project.

### Using `afterok` dependencies to transfer data

When using the [scratch](/filesystems/#scratch-directory) you typically need to transfer data from a [project directory](/filesystems/#project-directories) or the [long term storage](/filesystems/#cold-project-data-and-archives) to the scratch before the jobs starts, and then transfer the results back and clear your scratch after the job finishes. With job dependencies you can schedule

- a job to perform the data transfer to scratch,
- a job that runs your program with data in scratch that starts _after_ the data transfer completes successfully,
- a job to transfer the results back and clean the scratch that starts _after_ your program execution finished successfully.


### Using `singleton` dependency to run a lightweight database

Job dependencies can be used to provide a service that runs continuously for the duration of running some experiment. Imagine for instance that

- you maintain an [SQLite](https://www.sqlite.org/) database in the [Isilon file system](/filesystems/#cold-project-data-and-archives),

and you run an application in a external machine that,

- writes data in files in Isilon, and
- periodically submits a job to analyse the data and store them in the database.

For this setup, you need a script that runs an SQLite database in the cluster at all times.

The singleton job provides an appropriate method that is integrated with the Slurm scheduler. Remember that the singleton flag ensure that there is single job running in the cluster for each combination of job name (`--job-name`) and user id. If you submit multiple job with the same name and the `--dependency=singleton` they will run one at a time. The following script assumes that the database engine is contained in a singularity container.

!!! info "The database script `run_database.sh`"
    ```bash
    #!/bin/bash --login
    
    #SBATCH --job-name=database_service
    #SBATCH --mail-type=all
    #SBATCH --mail-user=name.surname@uni.lu
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=16
    #SBATCH --time=1-00:05:00
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --output=%x-%j.out
    #SBATCH --error=%x-%j.err
    
    declare end_time="${1}"
    
    convert_to_unix_time() {
      local time="${1}"
      date -d "${time}" '+%s'
    }
    
    get_slurm_job_script() {
      local job_id="${1}"
      scontrol show job "${job_id}" | awk 'BEGIN {FS="="} /^[[:space:]]*Command=/{print $2}'
    }
    
    declare time_now=$(date +%s)
    if [ -n "${end_time}" ] && [ "${time_now}" -lt "$(convert_to_unix_time "${end_time}")" ]; then
      sbatch --dependency=singleton "$(get_slurm_job_script ${SLURM_JOBID})" "${end_time}"
    fi
    
    module load tools/Singularity
    singularity run ${PROJECTHOME}/project_name/containers/database.sif &
    
    sleep $((24*60*60)) # 1 day in sec
    ```

The container is launched, and the job is killed a few minutes before the job maximum duration is reached. The scheduler has enough information to schedule the next instance of the database container close to the time the first job ends. Thus, given that enough resources are available, there will be a small gap between the two instances of the database process. Any application that is designed to be resilient to small interruptions in the database service will ride through the relaunch of the database.

!!! warning "Avoid fork-bombs"

    If you forget to specify `--dependency=singleton` in the line
    ```bash
    sbatch --dependency=singleton "$(get_slurm_job_script ${SLURM_JOBID})" "${end_time}"
    ```
    then `run_database.sh` jobs are recursively queued, and can crush of the scheduler. This is the equivalent of an accidental [fork bomb](https://en.wikipedia.org/wiki/Fork_bomb) for the Slurm scheduler.

The job scripts that use the database assume that the analysis job is in a Singularity container. The only input to the singularity run script is an HDF5 (`.h5`) file with the data. It is assumed that the container is configured correctly to access the database.

!!! info "Job script `run_analysis`"
    ```bash
    #!/bin/bash --login
    
    #SBATCH --job-name=data_analysis
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=128
    #SBATCH --time=0-00:30:00
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --output=%x-%j.out
    #SBATCH --error=%x-%j.err

    local data="${1}"

    module load tools/Singularity
    singularity run ${PROJECTHOME}/project_name/containers/analysis.sif "${data}"
    ```

With the database job running, the data analysis job can be submitted remotely for a server with the command
```bash
ssh aion-cluster "sbatch ${PROJECTHOME}/project_name/scripts/run_analysis.sh /mnt/isilon/projects/project_name/data/datafile_${id}.h5"
```
given that you have [setup in your SSH configuration](/connect/ssh/#ssh-configuration) an alias for the Aion cluster.

!!! warning "Providing services with HPC systems"

    The HPC system is not designed to provide continuously running services. The provided script provides constraints for the service running time, however, the constraints are not visible to the Slurm scheduler which reduces the effectiveness of the scheduling algorithm. Please use the provided method only for lightweight services.

    If you need to run large services for unspecified amounts of time, consider [setting up a virtual machine](https://service.uni.lu/sp?id=sc_cat_item&table=sc_cat_item&sys_id=a9f01d86db165c902fa838aa7c9619ba&searchTerm=virtual%20machine).

## _Resources_

1. [Documentation for `sbatch`](https://slurm.schedmd.com/sbatch.html#OPT_dependency)
