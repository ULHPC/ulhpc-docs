[The Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/) is a set of tools and Python
modules for setting up, manipulating, running, visualizing and
analyzing atomistic simulations. The code is freely available
under the GNU LGPL license. ASE provides interfaces to different
codes through `Calculators` which are used together with the
central `Atoms` object and the many available algorithms in ASE.


## Available versions of ASE in ULHPC
To check available versions of ASE at ULHPC type `module spider ase`.
The following list shows the available versions of ASE in ULHPC.
```bash
chem/ASE/3.13.0-intel-2017a-Python-2.7.13
chem/ASE/3.16.0-foss-2018a-Python-2.7.14
chem/ASE/3.16.0-intel-2018a-Python-2.7.14
chem/ASE/3.17.0-foss-2019a-Python-3.7.2
chem/ASE/3.17.0-intel-2019a-Python-2.7.15
chem/ASE/3.17.0-intel-2019a-Python-3.7.2
```

## Interactive mode
To open an ASE in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 # OR si --x11 [...]

# Load the module ase and needed environment
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load chem/ASE/3.17.0-intel-2019a-Python-3.7.2

$ python3 example.py
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J ASE
#SBATCH -N 1
#SBATCH -A <project name>
#SBATCH -M --cluster iris 
#SBATCH --ntasks-per-node=1
#SBATCH --time=00:30:00
#SBATCH -p batch

# Load the module ase and needed environment
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load chem/ASE/3.17.0-intel-2019a-Python-3.7.2

python3 example.py
```

## Additional information
To know more information about ASE tutorial and documentation,
please refer to [ASE tutorials](https://wiki.fysik.dtu.dk/ase/tutorials/tutorials.html).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).
    
