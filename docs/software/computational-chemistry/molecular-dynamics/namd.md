[![](https://d7umqicpi7263.cloudfront.net/img/product/9615ba9a-d797-4aab-852a-e5c0bc869e44/c85079c9-c6f0-4c93-9576-4b0c7a3eaedf.png){: style="width:300px;float: right;" }](https://www.ks.uiuc.edu/Research/namd/)
[NAMD](https://www.ks.uiuc.edu/Research/namd/), recipient of a 2002 Gordon Bell Award and a 2012 Sidney Fernbach Award,
is a parallel molecular dynamics code designed for high-performance simulation
of large biomolecular systems. Based on Charm++ parallel objects,
NAMD scales to hundreds of cores for typical simulations and beyond 500,000 cores for the largest simulations.
NAMD uses the popular molecular graphics program VMD for simulation setup and
trajectory analysis, but is also file-compatible with AMBER, CHARMM, and X-PLOR.
NAMD is distributed free of charge with source code. You can build NAMD yourself or
download binaries for a wide variety of platforms.
Our tutorials show you how to use NAMD and VMD for biomolecular modeling. 

## Available versions of NAMD in ULHPC
To check available versions of NAMD at ULHPC type `module spider namd`.
The following list shows the available versions of NAMD in ULHPC.
```bash
chem/NAMD/2.12-intel-2017a-mpi
chem/NAMD/2.12-intel-2018a-mpi
chem/NAMD/2.13-foss-2019a-mpi
```

## Interactive mode
To open NAMD in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 # OR si --x11 [...]

# Load the module namd and needed environment 
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load chem/NAMD/2.12-intel-2018a-mpi

$ namd2 +setcpuaffinity +p4 config_file > output_file
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J NAMD
#SBATCH -N 2
#SBATCH -A <project name>
#SBATCH -M --cluster iris 
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:30:00
#SBATCH -p batch

# Load the module namd and needed environment 
module purge
module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
module load chem/NAMD/2.12-intel-2018a-mpi

srun -n ${SLURM_NTASKS} namd2 +setcpuaffinity +p56 config_file.namd > output_file
```
## Additional information
To know more information about NAMD tutorial and documentation,
please refer to [NAMD User's Guide](https://www.ks.uiuc.edu/Research/namd/2.14/ug/).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).
