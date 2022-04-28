[![](https://www.paraview.org/wp-content/uploads/2018/02/ParaView_Logo.svg){: style="width:300px;float: right;" }](https://www.paraview.org/)

[ParaView](https://www.paraview.org/) is an open-source, multi-platform data analysis
and visualization application. ParaView users can quickly build visualizations
to analyze their data using qualitative and quantitative techniques.
The data exploration can be done interactively in 3D or programmatically
using ParaView’s batch processing capabilities.

ParaView was developed to analyse extremely large datasets using distributed
memory computing resources. It can be run on supercomputers to analyse datasets of
petascale size as well as on laptops for smaller data, has become an integral tool
in many national laboratories, universities and industry,
and has won several awards related to high performance computation.

ParaView ia an open-source, interactive, scalable, data analysis and
scientific visualization tools. It can be used to visualize the
simulation data or processing the data by using [GUI](https://www.paraview.org/Wiki/Beginning_GUI) or non-interactive
mode by using the [Python scripting](https://www.paraview.org/Wiki/ParaView/Python_Scripting). Using non-interacting mode,
that is using the python scripting is much faster than using the interactive mode,
when the data set is larger in both ParaView and VisIt.


## Available versions of ParaView in ULHPC
To check available versions of ParaView at ULHPC type `module spider paraview`.
The following list shows the available versions of ParaView in ULHPC.
```shell
vis/ParaView/5.5.0-intel-2018a-mpi
vis/ParaView/5.6.2-foss-2019a-mpi
vis/ParaView/5.6.2-intel-2019a-mpi
```

## Interactive mode
To open an ParaView in the interactive mode, please follow the following steps:

```shell
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11  # OR si --x11 [...]

# Load the module abinit and needed environment
$ module purge 
$ module load swenv/default-env/latest
$ module load vis/ParaView/5.6.2-intel-2019a-mpi

$ paraview &
```

## Batch mode
```shell
#!/bin/bash -l
#SBATCH -J ParaView
###SBATCH -A <project name>
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:30:00
#SBATCH -p batch

# Load the module Paraview and needed environment
module purge 
module load swenv/default-env/latest
module load vis/ParaView/5.6.2-intel-2019a-mpi

srun -n ${SLURM_NTASKS} pvbatch python-script.py
```

## Additional information
[ParaView's User Manual](https://www.paraview.org/Wiki/The_ParaView_Tutorial) has a
detail instructions about visualization and processing data in ParaView. There are two
ways of getting or writing the python script for the ParaView:

1. Reading the [ParaView's python scripting wiki](https://www.paraview.org/Wiki/ParaView/Python_Scripting) and [ParaView's Python Scripting Manual](https://www.paraview.org/Wiki/ParaView/Python_Scripting).
2. Record the commands that we do in ParaView GUI. Later this commands put into python script and it can be run as python scripting in ParaView.



!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).
