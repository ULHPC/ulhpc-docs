[![](https://www.abinit.org/themes/abinit/logo-abinit-2015.svg){: style="width:300px;float: right;" }](https://www.abinit.org/)
[ABINIT](https://www.abinit.org/) is a software suite to calculate the optical, mechanical, vibrational,
and other observable properties of materials. Starting from the quantum equations
of density functional theory, you can build up to advanced applications with
perturbation theories based on DFT, and many-body Green's functions (GW and DMFT) .
ABINIT can calculate molecules, nanostructures and solids with any chemical composition,
and comes with several complete and robust tables of atomic potentials.
On-line tutorials are available for the main features of the code,
and several schools and workshops are organized each year.

## Available versions of ABINIT in ULHPC
To check available versions of ABINIT at ULHPC type `module spider abinit`.
The following list shows the available versions of ABINIT in ULHPC. 
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
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 # OR si --x11 [...]

# Load the module abinit and needed environment
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load chem/ABINIT/8.10.2-intel-2019a

$ export SRUN_CPUS_PER_TASK=$SLURM_CPUS_PER_TASK

$ abinit < example.in 
```

## Batch mode
```shell
#!/bin/bash -l
#SBATCH -J ABINIT
#SBATCH -A <project name>
#SBATCH -M --cluster iris 
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:30:00
#SBATCH -p batch

# Load the module abinit and needed environment
module purge
module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
module load chem/ABINIT/8.10.2-intel-2019a

srun -n ${SLURM_NTASKS} abinit < input.files &> out
```
## Additional information
To know more information about ABINIT tutorial and documentation,
please refer to [ABINIT tutorial](https://docs.abinit.org/tutorial/).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).

