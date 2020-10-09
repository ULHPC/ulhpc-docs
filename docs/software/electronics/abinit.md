1. [Introduction](#introduction)
2. [Available versions of ABINIT in UL-HPC](#available-versions-of-abinit-in-ul-hpc)
3. [Interactive mode](#interactive mode)
4. [Batch mode](#batch-mode)
5. [Additional information](#additional-information)

## Introduction

[ABINIT](https://www.abinit.org/) is a software suite to calculate the optical, mechanical, vibrational,
and other observable properties of materials. Starting from the quantum equations
of density functional theory, you can build up to advanced applications with
perturbation theories based on DFT, and many-body Green's functions (GW and DMFT) .
ABINIT can calculate molecules, nanostructures and solids with any chemical composition,
and comes with several complete and robust tables of atomic potentials.
On-line tutorials are available for the main features of the code,
and several schools and workshops are organized each year.

## Available versions of ABINIT in UL-HPC
To check available versions of ABINIT at UL-HPC type `module spider abinit`.
Below it shows list of available versions of ABINIT in UL-HPC. 
```shell
chem/ABINIT/8.2.3-intel-2017a
chem/ABINIT/8.6.3-intel-2018a-trio-nc
chem/ABINIT/8.6.3-intel-2018a
chem/ABINIT/8.10.2-intel-2019a
```

## Interactive mode
To open an ABINIT in the interactive mode, please follow the following steps:

```shell
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the modules
$ module purge
$ module load chem/ABINIT/8.10.2-intel-2019a

$ abinit < example.in 
```

## Batch mode
```shell
#!/bin/bash -l
#SBATCH -J ABINIT
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
module load chem/ABINIT/8.10.2-intel-2019a

srun abinit < input.files &> out
```
## Additional information
For more information about the tutorial and documention
about ABINIT, please refer https://docs.abinit.org/tutorial/

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).