[![](https://company.wolfram.com/data/press-center/uploads/2016/07/Thumb_Mathematica.png){: style="width:300px;float: right;" }](https://www.wolfram.com/mathematica/)
For three decades, [MATHEMATICA](https://www.wolfram.com/mathematica/) has defined the state of the art in technical
computing-and provided the principal computation environment for millions of
innovators, educators, students, and others around the world.
Widely admired for both its technical prowess and elegant ease of use, Mathematica provides a single integrated,
continually expanding system that covers the breadth and depth of technical
computing-and seamlessly available in the cloud through any web browser, as well as natively on all modern desktop systems.

## Available versions of MATHEMATICA in ULHPC
To check available versions of MATHEMATICA at ULHPC type `module spider mathematica`.
The following list shows the available versions of MATHEMATICA in ULHPC. 
```bash
math/Mathematica/11.0.0
math/Mathematica/11.3.0
math/Mathematica/12.0.0
```

## Interactive mode
To open an MATHEMATICA in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 # OR si [...]

# Load the module MATHEMATICA and needed environment
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load math/Mathematica/12.0.0

$ math
```

## Batch mode
### An example for serial case

```bash
#!/bin/bash -l
#SBATCH -J MATHEMATICA
#SBATCH --ntasks-per-node 1
#SBATCH -c 1
#SBATCH --time=00:15:00
#SBATCH -p batch
### SBATCH -A <project_name>

# Load the module MATHEMATICA and needed environment
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load math/Mathematica/12.0.0

$ srun -n ${SLURM_NTASKS} math -run < {mathematica-script-file}.m
```

### An example for parallel case

```bash
#!/bin/bash -l
#SBATCH -J MATHEMATICA
#SBATCH -N 1
#SBATCH -c 28
#SBATCH --time=00:10:00
#SBATCH -p batch
### SBATCH -A <project_name>

# Load the module MATHEMATICA and needed environment
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load math/Mathematica/12.0.0

$ srun -n ${SLURM_NTASKS} math -run < {mathematica-script-file}.m
```

!!! exmaple
    ```bash
    # example for MATHEMATICA prallel (mathematica_script_file.m)
    //Limits Mathematica to requested resources
    Unprotect[$ProcessorCount];$ProcessorCount = 28;

    //Prints the machine name that each kernel is running on
    Print[ParallelEvaluate[$MachineName]];

    //Prints all Prime numbers less than 3000
    Print[Parallelize[Select[Range[3000],PrimeQ[2^#-1]&]]];
    ``` 



## Additional information
To know more information about MATHEMATICA tutorial and documentation,
please refer to [MATHEMATICA tutorial](https://www.wolfram.com/language/fast-introduction-for-math-students/en/).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).

