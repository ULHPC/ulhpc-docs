[![](https://upload.wikimedia.org/wikipedia/en/a/a2/MS3_NWChem.logo3.png){: style="width:300px;float: right;" }](https://nwchemgit.github.io/)
[NWChem](https://nwchemgit.github.io/) aims to provide its users with computational chemistry tools that
are scalable both in their ability to efficiently treat large scientific
problems, and in their use of available computing resources from
high-performance parallel supercomputers to conventional workstation clusters.

## Available versions of NWChem in ULHPC
To check available versions of NWChem at ULHPC type `module spider nwchem`.
The following list shows the available versions of NWChem in ULHPC.

```bash
chem/NWChem/6.6.revision27746-intel-2017a-2015-10-20-patches-20170814-Python-2.7.13
chem/NWChem/6.8.revision47-intel-2018a-Python-2.7.14
chem/NWChem/6.8.revision47-intel-2019a-Python-2.7.15
```

## Interactive mode
To try NWChem in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 # OR si --x11 [...]

# Load the module nwchem and needed environment 
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load chem/NWChem/6.8.revision47-intel-2019a-Python-2.7.15

$ nwchem example
```

!!! warning "naming input file"
    Please note example file should be named with extension like `example.nw`.
    

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J NWChem
#SBATCH -N 2
#SBATCH -A <project name>
#SBATCH -M --cluster iris 
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:30:00
#SBATCH -p batch

# Load the module nwchem and needed environment 
module purge 
module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
module load chem/NWChem/6.8.revision47-intel-2019a-Python-2.7.15

srun -n ${SLURM_NTASKS} nwchem example 
```
## Additional information
To know more information about NWChem tutorial and documentation,
please refer to [NWChem User Documentation](https://nwchemgit.github.io/Home.html).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).
