[Fire Dynamics Simulator (FDS)](https://pages.nist.gov/fds-smv/) is a large-eddy simulation (LES)
code for low-speed flows, with an emphasis on smoke and heat transport from fires.

## Available versions of FDS in ULHPC
To check available versions of FDS at ULHPC type `module spider abaqus`.
The following versions of FDS are available in ULHPC: 
```shell
# Available versions
phys/FDS/6.7.1-intel-2018a
phys/FDS/6.7.1-intel-2019a
phys/FDS/6.7.3-intel-2019a
```

## Interactive mode
To try FDS in the interactive mode, please follow the following steps:
```shell
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11

# Load the required version of FDS and needed environment
$ module purge
$ module load swenv/default-env/devel
$ module load phys/FDS/6.7.3-intel-2019a

# Example in fds 
$ fds example.fds
```

## Batch mode

### MPI only:
```shell
#!/bin/bash -l
#SBATCH -J FDS-mpi
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --ntasks-per-socket=14
#SBATCH -c 1
#SBATCH --time=00:30:00
#SBATCH -p batch

# Write out the stdout+stderr in a file
#SBATCH -o output.txt

# Mail me on job start & end
#SBATCH --mail-user=myemailaddress@universityname.domain
#SBATCH --mail-type=BEGIN,END

# To get basic info. about the job
echo "== Starting run at $(date)"
echo "== Job ID: ${SLURM_JOBID}"
echo "== Node list: ${SLURM_NODELIST}"
echo "== Submit dir. : ${SLURM_SUBMIT_DIR}"

# Load the required version of FDS and needed environment
module purge
module load swenv/default-env/devel
module load phys/FDS/6.7.3-intel-2019a

srun fds example.fds
```

### MPI+OpenMP (hybrid):
```shell
#!/bin/bash -l
#SBATCH -J FDS-hybrid
#SBATCH -N 2
#SBATCH --ntasks-per-node=56
#SBATCH --cpus-per-task=2
#SBATCH --time=00:30:00
#SBATCH -p batch

# Write out the stdout+stderr in a file
#SBATCH -o output.txt

# Mail me on job start & end
#SBATCH --mail-user=myemailaddress@universityname.domain
#SBATCH --mail-type=BEGIN,END

# To get basic info. about the job
echo "== Starting run at $(date)"
echo "== Job ID: ${SLURM_JOBID}"
echo "== Node list: ${SLURM_NODELIST}"
echo "== Submit dir. : ${SLURM_SUBMIT_DIR}"

# Load the required version of FDS and needed environment
module purge
module load swenv/default-env/devel
module load phys/FDS/6.7.3-intel-2019a

srun --cpus-per-task=2 fds_hyb example.fds
```

## Additional information
To know more about FDS documentation and tutorial,
please refer https://pages.nist.gov/fds-smv/manuals.html

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
