1. [Introduction](#introduction)
2. [Available versions of NAMD in UL-HPC](#available-versions-of-namd-in-ul-hpc)
3. [Interactive mode](#interactive mode)
4. [Batch mode](#batch-mode)
5. [Additional information](#additional-information)

## Introduction
[NAMD](https://www.ks.uiuc.edu/Research/namd/), recipient of a 2002 Gordon Bell Award and a 2012 Sidney Fernbach Award,
is a parallel molecular dynamics code designed for high-performance simulation
of large biomolecular systems. Based on Charm++ parallel objects,
NAMD scales to hundreds of cores for typical simulations and beyond 500,000 cores for the largest simulations.
NAMD uses the popular molecular graphics program VMD for simulation setup and
trajectory analysis, but is also file-compatible with AMBER, CHARMM, and X-PLOR.
NAMD is distributed free of charge with source code. You can build NAMD yourself or
download binaries for a wide variety of platforms.
Our tutorials show you how to use NAMD and VMD for biomolecular modeling. 

## Available versions of NAMD in UL-HPC
To check available versions of NAMD at UL-HPC type `module spider namd`.
Below it shows list of available versions of NAMD in UL-HPC.

```shell
chem/NAMD/2.12-intel-2017a-mpi
chem/NAMD/2.12-intel-2018a-mpi
chem/NAMD/2.13-foss-2019a-mpi
```

## Interactive mode
To open an NAMD in the interactive mode, please follow the following steps:

```shell
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the modules
$ module purge
$ module load chem/NAMD/2.12-intel-2018a-mpi

$ namd2 +setcpuaffinity +p4 config_file > output_file
```

## Batch mode
```shell
#!/bin/bash -l
#SBATCH -J NAMD
#SBATCH -N 2
#SBATCH --ntasks-per-node=56
#SBATCH --time=00:30:00
#SBATCH -p batch

# Write out the stdout+stderr in a file
#SBATCH -o output.txt

# Mail me on job start & end
#SBATCH --mail-user=myemailaddress@universityname.domain
#SBATCH --mail-type=BEGIN,END

echo "== Starting run at $(date)"
echo "== Job ID: ${SLURM_JOBID}"
echo "== Node list: ${SLURM_NODELIST}"
echo "== Submit dir. : ${SLURM_SUBMIT_DIR}"

# Load the modules
module purge
module load chem/NAMD/2.12-intel-2018a-mpi

srun namd2 +setcpuaffinity +p56 config_file.namd > output_file
```
## Additional information
For more information about the tutorial and documention about NAMD,
please refer https://www.ks.uiuc.edu/Research/namd/2.14/ug/

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).  