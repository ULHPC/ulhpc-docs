[![](https://raw.githubusercontent.com/docker-library/docs/520519ad7db3ea9fd5d3590e836c839a0ffd6f19/julia/logo.png){: style="width:300px;float: right;" }](https://julialang.org/)
Scientific computing has traditionally required the highest performance, yet domain experts have largely moved to slower dynamic languages for daily work. We believe there are many good reasons to prefer dynamic languages for these applications, and we do not expect their use to diminish. Fortunately, modern language design and compiler techniques make it possible to mostly eliminate the performance trade-off and provide a single environment productive enough for prototyping and efficient enough for deploying performance-intensive applications. The [Julia](https://julialang.org/) programming language fills this role: it is a flexible dynamic language, appropriate for scientific and numerical computing, with performance comparable to traditional statically-typed languages.

## Available versions of Julia in ULHPC
To check available versions of Julia at ULHPC type `module spider julia`.
The following list shows the available versions of Julia in ULHPC. 
```bash
lang/Julia/1.1.1
lang/Julia/1.3.0
```

## Interactive mode
To open an MATLAB in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 # OR si [...]

# Load the module Julia and needed environment
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load lang/Julia/1.3.0

$ julia
```

## Batch mode
### An example for serial code

```bash
#!/bin/bash -l
#SBATCH -J Julia
###SBATCH -A <project name>
#SBATCH --ntasks-per-node 1
#SBATCH -c 1
#SBATCH --time=00:15:00
#SBATCH -p batch

# Load the module Julia and needed environment
module purge
module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
module load lang/Julia/1.3.0

julia {example}.jl
```


### An example for parallel code

```bash
#!/bin/bash -l
#SBATCH -J Julia
###SBATCH -A <project name>
#SBATCH -N 1
#SBATCH --ntasks-per-node 28
#SBATCH --time=00:10:00
#SBATCH -p batch

# Load the module Julia and needed environment
module purge
module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
module load lang/Julia/1.3.0

srun -n ${SLURM_NTASKS} julia {example}.jl
```

!!! example

    ```julia
    using Distributed
    
    # launch worker processes
    num_cores = parse(Int, ENV["SLURM_CPUS_PER_TASK"])
    addprocs(num_cores)
    
    println("Number of cores: ", nprocs())
    println("Number of workers: ", nworkers())
    
    # each worker gets its id, process id and hostname
    for i in workers()
    id, pid, host = fetch(@spawnat i (myid(), getpid(), gethostname()))
    println(id, " " , pid, " ", host)
    end
    
    # remove the workers
    for i in workers()
    rmprocs(i)
    end
    ```



## Additional information
To know more information about Julia tutorial and documentation,
please refer to [Julia tutorial](https://julialang.org/learning/tutorials/).

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
