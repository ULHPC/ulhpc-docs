[![](https://upload.wikimedia.org/wikipedia/commons/9/99/CP2K_logo.png){: style="width:300px;float: right;" }](https://www.cp2k.org/)
[CP2K](https://www.cp2k.org/) is a quantum chemistry and solid state physics software package that can perform atomistic
simulations of solid state, liquid, molecular, periodic, material, crystal, and biological systems.
CP2K provides a general framework for different modeling methods such as DFT using the mixed
Gaussian and plane waves approaches GPW and GAPW. Supported theory levels include DFTB, LDA,
GGA, MP2, RPA, semi-empirical methods (AM1, PM3, PM6, RM1, MNDO, …), and classical force
fields (AMBER, CHARMM, …). CP2K can do simulations of molecular dynamics, metadynamics,
Monte Carlo, Ehrenfest dynamics, vibrational analysis, core level spectroscopy, energy minimization,
and transition state optimization using NEB or dimer method.
CP2K is written in Fortran 2008 and can be run efficiently in parallel using a combination of multi-threading,
MPI, and CUDA. It is freely available under the GPL license.
It is therefore easy to give the code a try, and to make modifications as needed.

## Available versions of CP2K in ULHPC
To check available versions of CP2K at ULHPC type `module spider cp2k`.
The following list shows the available versions of CP2K in ULHPC. 
```bash
chem/CP2K/6.1-foss-2019a
chem/CP2K/6.1-intel-2018a
```

## Interactive mode
To open CP2K in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 # OR si --x11 [...]

# Load the module cp2k and needed environment 
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load chem/CP2K/6.1-intel-2018a

$ cp2k.popt -i example.inp 
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J CP2K
#SBATCH -N 2
#SBATCH -A <project name>
#SBATCH -M --cluster iris 
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:30:00
#SBATCH -p batch

# Load the module cp2k and needed environment 
module purge
module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
module load chem/CP2K/6.1-intel-2018a 

srun -n ${SLURM_NTASKS} cp2k.popt -i example.inp > outputfile.out
```
## Additional information
To know more information about CP2K tutorial and documentation,
please refer to [CP2K HOWTOs](https://www.cp2k.org/howto).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).

