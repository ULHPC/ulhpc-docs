[![](https://meep.readthedocs.io/en/latest/images/Meep-banner.png){: style="width:300px;float: right;" }](https://meep.readthedocs.io/en/latest/)
[Meep](https://meep.readthedocs.io/en/latest/) is a free and open-source
software package for electromagnetics simulation via
the finite-difference time-domain (FDTD) method spanning a
broad range of applications.

## Available versions of Meep in ULHPC
To check available versions of Meep at ULHPC type `module spider meep`.
The following list shows the available versions of Meep in ULHPC.
```bash
phys/Meep/1.3-intel-2017a
phys/Meep/1.4.3-intel-2018a
phys/Meep/1.4.3-intel-2019a
```

## Interactive mode
To try Meep in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 # OR si --x11 [...]

# Load the module meep and needed environment 
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load toolchain/intel/2019a
$ module load phys/Meep/1.4.3-intel-2019a

$ meep example.ctl > result_output
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J Meep
#SBATCH -N 2
#SBATCH -A <project name>
#SBATCH -M --cluster iris 
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:30:00
#SBATCH -p batch

# Load the module meep and needed environment 
module purge
module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
module load toolchain/intel/2019a
module load phys/Meep/1.4.3-intel-2019a

srun -n ${SLURM_NTASKS} meep example.ctl > result_output
```
## Additional information
To know more information about Meep tutorial and documentation,
please refer to [Meep tutorial](http://ab-initio.mit.edu/wiki/index.php/Meep_tutorial).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).



