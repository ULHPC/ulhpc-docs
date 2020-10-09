1. [Introduction](#introduction)
2. [Available versions of Meep in UL-HPC](#available-versions-of-meep-in-ul-hpc)
3. [Interactive mode](#interactive mode)
4. [Batch mode](#batch-mode)
5. [Additional information](#additional-information)

## Introduction
[Meep](https://meep.readthedocs.io/en/latest/) is a free and open-source
software package for electromagnetics simulation via
the finite-difference time-domain (FDTD) method spanning a
broad range of applications.

## Available versions of Meep in UL-HPC
To check available versions of Meep at UL-HPC type `module spider meep`.
Below it shows list of available versions of Meep in UL-HPC.
```shell
phys/Meep/1.3-intel-2017a
phys/Meep/1.4.3-intel-2018a
phys/Meep/1.4.3-intel-2019a
```

## Interactive mode
To try a Meep in the interactive mode, please follow the following steps:

```shell
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the modules
$ module purge
$ module load swenv/default-env/v1.2-20191021-production 
$ module load toolchain/intel/2019a
$ module load phys/Meep/1.4.3-intel-2019a

$ meep example.ctl > result_output
```

## Batch mode
```shell
#!/bin/bash -l
#SBATCH -J Meep
#SBATCH -N 1
#SBATCH --ntasks-per-node=28
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
module load swenv/default-env/v1.2-20191021-production 
module load toolchain/intel/2019a
module load phys/Meep/1.4.3-intel-2019a

srun -n 28 meep example.ctl > result_output
```
## Additional information
For more information about the tutorial and documention
about Meep, please refer http://ab-initio.mit.edu/wiki/index.php/Meep_tutorial

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).