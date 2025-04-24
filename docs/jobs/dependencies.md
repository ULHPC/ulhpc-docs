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

When using the [scratch](/filesystems/#scratch-directory) data typically needs to be transferred from a [project directory](/filesystems/#project-directories) or the [long term storage](/filesystems/#cold-project-data-and-archives) to the scratch before the jobs starts, and then the results must be transferred back and the scratch cleared after the job finishes. With job dependencies someone can schedule

- a job to perform the data transfer to scratch,
- a job that runs their program with data in scratch that starts _after_ the data transfer completes successfully,
- a job to transfer the results back and clean the scratch that starts _after_ their program execution has finished successfully.


### Using `singleton` dependency to run a lightweight database

Job dependencies can be used to provide a service that runs continuously for the duration of some experiment. Imagine for instance that

- you maintain an [SQLite](https://www.sqlite.org/) database in the [Isilon file system](/filesystems/#cold-project-data-and-archives) containing measurement data and analysis results, and
- that you run an application in a external machine that periodically writes data files in Isilon, and submits a job to analyse the data and store them in the database.

For this setup, you need a script that runs an SQLite database in the cluster at all times.

The singleton job provides an appropriate method for maintaining a jobs running in manner accounted by the Slurm scheduler. The singleton dependency ensure that there is single job running in the cluster for each combination of job name (`--job-name`) and user id. If you submit multiple job with the same name and the `--dependency=singleton` they will run one at a time.

#### The database job service

There are 2 options for running a database to collect processed results, run for a fixed amount of time, or for until a specific time instance. The following scripts assume that the database engine is contained in a singularity container.

=== "Run for a fixed duration"

    Running the database for a fixed duration is the simplest option. Split your job in jobs of smaller duration, and submit all the jobs at once. For instance this script splits the job in one day chunks.

    !!! info "Database script `run_database.sh`"
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

        module load tools/Apptainer
        apptainer run ${PROJECTHOME}/project_name/containers/database.sif &

        sleep $((24*60*60)) # 1 day in sec
        ```

    If you want to run your job for `${N}` days, submit `${N}` copies:
    ```bash
    for i in $(seq "${N}"); do sbatch run_database.sh; done; unset i
    ```

=== "Run until a specific time instance"

    Running a job until a specific time instance is also possible but more involved. The following script takes as argument the end date and time of the service.


    !!! info "Database script `run_database.sh`"
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
          date --date="${time}" '+%s'
        }

        get_slurm_job_script() {
          local job_id="${1}"
          scontrol show job "${job_id}" | awk 'BEGIN {FS="="} /^[[:space:]]*Command=/{print $2}'
        }

        declare time_now=$(date '+%s')
        if [ -n "${end_time}" ] && [ "${time_now}" -lt "$(convert_to_unix_time "${end_time}")" ]; then
          sbatch --dependency=singleton "$(get_slurm_job_script ${SLURM_JOBID})" "${end_time}"
        fi

        module load tools/Apptainer
        apptainer run ${PROJECTHOME}/project_name/containers/database.sif &

        sleep $((24*60*60)) # 1 day in sec
        ```

    Submit the script providing the end date and time of your job with the command
    ```bash
    sbatch run_database.sh "${end_time}"
    ```
    where `${end_time}` should be a string interpretable by the [`date`](https://man7.org/linux/man-pages/man1/date.1.html) command. A very flexible format is ISO 8601; for instance, `Wed Apr 23 04:49:36 PM CEST 2025` becomes `2025-04-23T16:49:36+02:00` in ISO 8601. The `date` can parse both aforementioned strings.

    !!! danger "Avoid fork-bombs"

        If you forget to specify `--dependency=singleton` in the command
        ```bash
        sbatch --dependency=singleton "$(get_slurm_job_script ${SLURM_JOBID})" "${end_time}"
        ```
        then `run_database.sh` jobs are recursively queued, and can crush of the scheduler. This is the equivalent of an accidental [fork bomb](https://en.wikipedia.org/wiki/Fork_bomb) for the Slurm scheduler.

    !!! danger "Ensure proper scheduling"

        If the service is scheduled after the command is called,
        ```bash
        apptainer run ${PROJECTHOME}/project_name/containers/database.sif
        sbatch --dependency=singleton "$(get_slurm_job_script ${SLURM_JOBID})" "${end_time}"
        ```
        where you first wait for the process to finish (note the absence of `&`) and then schedule the next job, there may be a long wait for resources and thus an unacceptably long interruption of your service.

---

The job scripts for the database, `run_database.sh`, schedule the future database job, launch a containerized database job in the background, and wait for the job for a fixed amount of time, a bit smaller that the job maximum duration. Thus, the scheduler has enough information an leeway to schedule the next instance of the database container close to the time the first job ends. Thus, given that enough resources are available, there will be a small gap between the two instances of the database process. Any application that is designed to be resilient to small interruptions in the database service will ride through the relaunch of the database without issues.

!!! warning "Providing services with HPC systems"

    The HPC system is not designed to provide continuously running services. The provided script provides constraints for the service running time, however, the constraints are not visible to the Slurm scheduler which reduces the effectiveness of the scheduling algorithm. Please use the provided method only for lightweight services.

    If you need to run large services for unspecified amounts of time, consider [setting up a virtual machine](https://service.uni.lu/sp?id=sc_cat_item&table=sc_cat_item&sys_id=a9f01d86db165c902fa838aa7c9619ba&searchTerm=virtual%20machine).


#### Submitting jobs that use the database

To periodically submit jobs that use the database it is assumed that the analysis procedure is contained in a Singularity container and that the job is configured to access the database. For instance, the database machine IP and the port used by the database may be stored and read from a specific location in the cluster file system. It is assumed that the single input to the analysis is a binary `dat` file.

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

    module load tools/Apptainer
    apptainer run ${PROJECTHOME}/project_name/containers/analysis.sif "${data}"
    ```

With the database job running, the data analysis job can be submitted remotely for a server with the command
```bash
ssh aion-cluster "sbatch ${PROJECTHOME}/project_name/scripts/run_analysis.sh /mnt/isilon/projects/project_name/data/datafile_${id}.dat"
```
given that the [SSH configuration](/connect/ssh/#ssh-configuration) of the server contains the `aion-cluster` entry for the Aion cluster.

## _Resources_

1. [Documentation for `sbatch`](https://slurm.schedmd.com/sbatch.html#OPT_dependency)
