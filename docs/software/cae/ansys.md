[![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/ANSYS_logo.png/320px-ANSYS_logo.png){: style="width:200px;float: right;" }](https://www.ansys.com/) [ANSYS](https://www.ansys.com/) offers a comprehensive software suite that spans the entire range of physics, providing access to virtually any field of engineering simulation that a design process requires.


## Available versions of ANSYS at ULHPC

You can check the available versions of ANSYS at ULHPC with the command `module spider ansys`.

```bash
$ module spider ansys

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  tools/ANSYS:
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    Description:
      ANSYS simulation software enables organizations to confidently predict how their products will operate in the real world. We believe that every product is a promise of something greater. 

     Versions:
        tools/ANSYS/21.1
        tools/ANSYS/2022R2
        tools/ANSYS/2024R2

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  For detailed information about a specific "tools/ANSYS" package (including how to load the modules) use the module's full name.
  Note that names that have a trailing (E) are extensions provided by other modules.
  For example:

     $ module spider tools/ANSYS/2024R2
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
```

According to the output of the module command, there are 3 versions of ANSYS available, and `2024R2` is the latest.

## Working in interactive mode

To open an ANSYS in interactive mode, [connect to the cluster](/connect/ssh/) with X11 forwarding enabled,

=== "Iris"
    ```bash
    # From your local computer
    $ ssh -X iris-cluster
    ```
=== "Aion"
    ```bash
    # From your local computer
    $ ssh -X aion-cluster
    ```

and then create and allocation with X11 forwarding enabled:

=== "Iris"
    ```bash
    # Reserve the node for interactive computation
    $ salloc --partition=interactive --qos=debug --time=02:00:00 --ntasks=1 --cpus-per-task=14 --x11

    # Load the required version of ANSYS and needed environment
    $ module purge
    $ module load tools/ANSYS/2024R2

    # To launch ANSYS workbench
    $ runwb2
    ```
=== "Aion"
    ```bash
    # Reserve the node for interactive computation
    $ salloc --partition=interactive --qos=debug --time=02:00:00 --ntasks=1 --cpus-per-task=16 --x11

    # Load the required version of ANSYS and needed environment
    $ module purge
    $ module load tools/ANSYS/2024R2

    # To launch ANSYS workbench
    $ runwb2
    ```

In this example the number of cpus is selected so that a single full socket is reserved in each cluster.

## Submitting batch scripts 

When you run ANSYS packages such as Fluent in batch mode apart from the usual input, such as [journal files](https://docs.hpc.shef.ac.uk/en/latest/referenceinfo/ANSYS/fluent/writing-fluent-journal-files.html#gsc.tab=0), you may provide options to execute the computation across multiple compute nodes.


According to the output of help function of Fluent, `fluent -h`,

- `-gu` runs the software without GUI,
- `-cnf` specifies the host file with the list of hosts available to the program,
- `-t` specifies the number of host from the host file that will be used (only `-t<number>` notation is supported for this flag),
- `-mpi` selects the MPI backend, and
- `-p` selects the interconnect (only `-p<interconnect>` notation is supported for this flag).

=== "Iris"
    ```bash
    #!/usr/bin/bash --login
    #SBATCH --job-name=VOF
    #SBATCH --mail-type=end,fail
    #SBATCH --mail-user=name.surname@uni.lu
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --nodes=4
    #SBATCH --ntasks-per-node=28
    #SBATCH --cpus-per-task=1
    #SBATCH --exclusive
    #SBATCH --time=1-00:00:00
    #SBATCH --output=%x-%j.out
    #SBATCH --error=%x-%j.err

    declare HOSTSFILE=/tmp/hostlist-${SLURM_JOB_ID}
    scontrol show hostnames > ${HOSTSFILE}

    # To get basic info. about the job
    echo "== Job ID: ${SLURM_JOBID}"
    echo "== Node list: ${SLURM_NODELIST}"
    echo "== Working directory: ${SLURM_SUBMIT_DIR}"
    echo "Starting run at $(date)"
    echo ""

    module purge
    module load tools/ANSYS/2024R2

    fluent 3ddp -gu -t${SLURM_NTASKS} -cnf=${HOSTSFILE} -mpi=openmpi -pib -i journal.txt 
    ```
=== "Aion"
    ```bash
    #!/usr/bin/bash --login
    #SBATCH --job-name=VOF
    #SBATCH --mail-type=end,fail
    #SBATCH --mail-user=name.surname@uni.lu
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --nodes=4
    #SBATCH --ntasks-per-node=128
    #SBATCH --cpus-per-task=1
    #SBATCH --exclusive
    #SBATCH --time=1-00:00:00
    #SBATCH --output=%x-%j.out
    #SBATCH --error=%x-%j.err

    declare HOSTSFILE=/tmp/hostlist-${SLURM_JOB_ID}
    scontrol show hostnames > ${HOSTSFILE}

    # To get basic info. about the job
    echo "== Job ID: ${SLURM_JOBID}"
    echo "== Node list: ${SLURM_NODELIST}"
    echo "== Working directory: ${SLURM_SUBMIT_DIR}"
    echo "Starting run at $(date)"
    echo ""

    module purge
    module load tools/ANSYS/2024R2

    fluent 3ddp -gu -t${SLURM_NTASKS} -cnf=${HOSTSFILE} -mpi=openmpi -pib -i journal.txt 
    ```

The ANSYS binaries come bundled with their own version of MPI that operates independent of the system job launcher and so they need a host list and a communication backend to start the job. This job

- runs `SLURM_NTASKS` tasks (`-t${SLURM_NTASKS}`), where `SLURM_NTASKS = SLURM_NTASKS_PER_NODE * SLURM_JOB_NUM_NODES` are assigned in a round-robin fashion along the entries of `HOSTFILE`, and
- uses the `openmpi` backend (`-mpi=openmpi`)
- with the `ib` (Infiniband) interconnect (`-pid`).

Similar options are used for other packages of ANSYS.

## Additional information

ANSYS provides the [customer support](https://support.ansys.com), if you have a license key, you should be able to get access the support, manuals, and other useful documents.

You can find an old but relevant version of the [user manual section on parallel jobs](https://www.afs.enea.it/project/neptunius/docs/fluent/html/ug/node996.htm) in the [documentation of the ENEAGRID/CRESCO](https://www.afs.enea.it/project/neptunius/docs/fluent/html/ug/node996.htm) hyper cluster. The user manual provides detailed explanation for the various parallel job options.

!!! tip
    If you find some issues with the instructions above, please file a [support ticket](https://hpc.uni.lu/support).
