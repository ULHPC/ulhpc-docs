[![](https://www.vasp.at/images/logo.png){: style="width:300px;float: right;" }](https://www.vasp.at/)
[VASP](https://www.vasp.at/documentation/) is a package for performing ab initio quantum-mechanical molecular dynamics (MD)
using pseudopotentials and a plane wave basis set. The approach implemented in VASP
is based on a finite-temperature local-density approximation (with the free energy as variational quantity)
and an exact evaluation of the instantaneous electronic ground state at each MD step
using efficient matrix diagonalization schemes and an efficient Pulay mixing.

## Available versions of VASP in ULHPC
To check available versions of VASP at ULHPC type `module spider vasp`.

??? info [ULHPC Software/Modules Environment](../../environment/modules.md)
     For the user's convenience, we are maintaining the old
     version and new version of each software that are available at
     the ULHPC. To work with different software sets and how to
     load them to your environment is clearly
     explained in [Modules](../../environment
     /modules.md). For example, if your module path is set to deprecated modules
     `export MODULEPATH=$DEPRECATED_MODULEPATH` then
     the following list shows the available versions of VASP in ULHPC.
     
```bash
phys/VASP/5.4.4-intel-2017a
phys/VASP/5.4.4-intel-2018a
phys/VASP/5.4.4-intel-2019a
```

## Interactive mode
To open VASP in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 # OR si --x11 [...]

# Load the module vasp and needed environment 
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load phys/VASP/5.4.4-intel-2019a

$ vasp_[std/gam/ncl]
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J VASP
#SBATCH -N 2
#SBATCH -A <project name>
#SBATCH -M --cluster iris 
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:30:00
#SBATCH -p batch

# Load the module vasp and needed environment 
module purge 
module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
module load phys/VASP/5.4.4-intel-2019a

srun -n ${SLURM_NTASKS} vasp_[std/gam/ncl]
```

## Additional information
To know more information about VASP tutorial and documentation,
please refer to [VASP manual](https://www.vasp.at/wiki/index.php/The_VASP_Manual).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).
