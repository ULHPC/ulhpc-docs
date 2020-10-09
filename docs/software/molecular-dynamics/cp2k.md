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

## Available versions of CP2K in UL-HPC
To check available versions of CP2K at UL-HPC type `module spider cp2k`.
Below it shows list of available versions of CP2K in UL-HPC. 
```bash
chem/CP2K/6.1-foss-2019a
chem/CP2K/6.1-intel-2018a
```

## Interactive mode
To open an CP2K in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the modules
$ module purge
$ module load chem/CP2K/6.1-intel-2018a
        
$ cp2k.popt -i example.inp 
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J CP2K
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
module load chem/CP2K/6.1-intel-2018a

srun cp2k.popt -i example.inp > outputfile.out
```
## Additional information
For more information about the tutorial and documention about CP2K,
please refer https://www.cp2k.org/howto

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).  