[![](https://www.openmp.org/wp-content/uploads/openmp-enabling-hpc-since-1997.png){: style="width:300px;float: right;" }](https://www.openmp.org/)
[OpenMP](https://www.openmp.org/)(Open Multi-Processing) is a popular parallel
programming model for multi-threaded applications. More precisely, it is an
Application Programming Interface (API) that supports **multi-platform shared
memory multiprocessing** programming in C, C++, and Fortran on most platforms,
instruction set architectures and operating systems.

OpenMP is designed for multi-processor/core, shared memory machine (nowadays NUMA).
OpenMP programs accomplish parallelism **exclusively** through the use of threads.

* A thread of execution is the smallest unit of processing that can be scheduled by an operating system.
    - Threads exist within the resources of a single process. Without the process, they cease to exist.
* Typically, the number of threads match the number of machine processors/cores.
    - _Reminder_: **Iris**: 2x14 cores
    - However, the actual use of threads is up to the application.
    - `OMP_NUM_THREADS` (if present) specifies initially the max number of threads;
        - you can use `omp_set_num_threads()` to override the value of `OMP_NUM_THREADS`;
        - the presence of the `num_threads` clause overrides both other values.
* OpenMP is an explicit (not automatic) programming model, offering the
  programmer full control over parallelization.  
    - parallelization can be as simple as taking a serial program and inserting compiler directives....
    - in general, this is way more complex
* OpenMP uses the fork-join model of parallel execution
    - **FORK**: the master thread then creates a team of parallel threads.
        - The statements in the program that are enclosed by the parallel region
          construct are then executed in parallel among the various team threads.
    - **JOIN**: When the team threads complete the statements in the parallel region construct,
      they synchronize and terminate, leaving only the master thread.

[![](https://upload.wikimedia.org/wikipedia/commons/f/f1/Fork_join.svg){: style="width:900px;float: center;" }](url)


OpenMP compilers in ULHPC:

|Toolchain|Compilation(C)|Compilation(Fortran)|
| - | - | - |
|`toolchain/intel`|`icc -qopenmp [...]`|`gfortran -qopenmp [...]`|
|`toolchain/foss`|`gcc -fopenmp [...]`|`ifort -fopenmp [...]`|

## How to use the OpenMP in ULHPC
### Interactive mode:
```bash

# Reserve the node
$ srun -p batch --time=00:10:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the {intel | foss} toolchain and whatever module(s) you need
module purge
module load toolchain/intel    # or toolchain/foss

# Compilation
$ icc -qopenmp hello.c

# Code execution
$ export OMP_NUM_THREADS=4
$ ./a.out
```

### Batch job:
```bash
#!/bin/bash -l
#SBATCH --ntasks-per-node=1 # Run a single task per node, more explicit than '-n 1'
#SBATCH -c 28               #  number of CPU cores i.e. OpenMP threads per task
#SBATCH --time=0-00:10:00
#SBATCH -p batch

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

# Load the {intel | foss} toolchain and whatever module(s) you need
module purge
module load toolchain/intel    # or toolchain/foss

# srun /path/to/your/openmp_program
srun ./a.out
```

## Tuning (Thread Affinity) using environmental varibales

The Intel runtime library has the ability to bind OpenMP threads to physical processing units.
The interface is controlled using the `KMP_AFFINITY`
environment variable. Depending on the system (machine) topology, application, and operating system, thread affinity can have a dramatic effect on the application speed.
`Thread affinity`
restricts execution of certain threads (virtual execution units) to a subset of the physical processing units in a multiprocessor computer. Depending upon the topology of the machine, thread affinity can have a dramatic effect on the execution speed of a program.

Similary GNU Compiler Collection has `OMP_PLACES` and `OMP_PROC_BIND` will bind the OpenMP threads to the physical processing units. 


??? tip "To see hardware of the compute node (understanding your machine architecture)"

    ```bash
    # To see compute node hardware
    $ numactl --hardware
    available: 2 nodes (0-1)
    node 0 cpus: 0 2 4 6 8 10 12 14 16 18 20 22 24 26
    node 0 size: 65442 MB
    node 0 free: 37136 MB
    node 1 cpus: 1 3 5 7 9 11 13 15 17 19 21 23 25 27
    node 1 size: 65536 MB
    node 1 free: 54071 MB
    node distances:
    node   0   1
      0:  10  21
      1:  21  10

    # Another approach to see cores and socket
    $ lscpu | grep -i 'core\|thread\|Socket'
    Thread(s) per core:    1
    Core(s) per socket:    14
    Socket(s):             2
    ```

Batch script for Intel:
```bash
#!/bin/bash -l
#SBATCH -J Intel-OpenMP
#SBATCH --ntasks-per-node=1    # Run a single task per node, more explicit than '-n 1'
#SBATCH -c 28                  #  number of CPU cores i.e. OpenMP threads per task
#SBATCH --time=0-00:10:00
#SBATCH -p batch

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

# Load the {intel | foss} toolchain and whatever module(s) you need
module purge
module load toolchain/intel    # or toolchain/foss

# Bind your OpenMP threads
export OMP_NUM_THREADS=56
export KMP_AFFINITY=verbose,granularity=core,compact

# srun /path/to/your/openmp_program
srun ./a.out
```

Batch script for GNU Compiler Collection:
```bash
#!/bin/bash -l
#SBATCH -J GCC-OpenMP
#SBATCH --ntasks-per-node=1    # Run a single task per node, more explicit than '-n 1'
#SBATCH -c 28                  # Number of CPU cores i.e. OpenMP threads per task
#SBATCH --time=0-00:10:00
#SBATCH -p batch

export OMP_NUM_THREADS=${SLURM_CPUS_PER_TASK}

# Load the {intel | foss} toolchain and whatever module(s) you need
module purge
module load toolchain/foss     # or toolchain/foss

# Bind your OpenMP threads
export OMP_PLACES=cores 
export OMP_PROC_BIND=close

# srun /path/to/your/openmp_program
srun ./a.out
```

## Addtional information
To know more about the OpenMP at ULHPC, please
refer [ULHPC OpenMP Tutorial](https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/basics/#parallel-openmp-jobs)

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).