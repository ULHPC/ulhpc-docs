## Abaqus

1. [Introduction](#introduction)
2. [Available versions of Abaqus in UL-HPC](#available-versions-of-openfoam-in-ul-hpc)
3. [Interactive mode](#interactive mode)
4. [Batch mode](#batch mode)
5. [Additional information](#additional information)

## Introduction
The Abaqus Unified FEA product suite offers powerful and complete solutions
for both routine and sophisticated engineering problems covering a vast
spectrum of industrial applications. In the automotive industry engineering
work groups are able to consider full vehicle loads, dynamic vibration,
multibody systems, impact/crash, nonlinear static, thermal coupling, and
acoustic-structural coupling using a common model data structure and integrated
solver technology. Best-in-class companies are taking advantage of
Abaqus Unified FEA to consolidate their processes and tools,
reduce costs and inefficiencies, and gain a competitive advantage

## Available versions of Abaqus in UL-HPC
The following versions of Abaqus are available in UL-HPC
```shell
# Available versions
 cae/ABAQUS/6.14.2
 cae/ABAQUS/2017-hotfix-1729
 cae/ABAQUS/2017-hotfix-1740
 cae/ABAQUS/2017-hotfix-1745
 cae/ABAQUS/2017-hotfix-1803
 cae/ABAQUS/2018-hotfix-1806
```

## Interactive mode
To open an ANSYS in the interactive mode, please follow the following steps:

```shell
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p batch --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the required version of Abaqus and needed environment
module purge
module load swenv/default-env/v0.1-20170602-production
module load cae/ABAQUS/2017-hotfix-1803
module load vis/libGLU/9.0.0-intel-2017a
export LM_License_file=xyz

abaqus job=job-name input=input.inp cpus=n gpus=n
```
where `n=number of cores` and for gpus `n=number of GPUs`.

The following options for simulation to stop and resume it:
```shell
abaqus job=job-name suspend
abaqus job=job-name resume
```

## Batch mode
Example for Abaqus batch job
```shell
#!/bin/bash -l
#SBATCH -J Abaqus
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

module purge
module load swenv/default-env/v0.1-20170602-production
module load cae/ABAQUS/2017-hotfix-1803
module load vis/libGLU/9.0.0-intel-2017a
export LM_License_file=xyz

abaqus-mpi job=job input=input.inp interactive
```

## Additional information



