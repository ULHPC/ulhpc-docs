[![](https://6lli539m39y3hpkelqsm3c2fg-wpengine.netdna-ssl.com/wp-content/uploads/2017/05/MPIlogo2.gif){: style="width:300px;float: right;" }](https://computing.llnl.gov/tutorials/mpi/)
The [Message Passing Interface Standard (MPI)](https://computing.llnl.gov/tutorials/mpi/) is a message passing library standard
based on the consensus of the MPI Forum, which has over 40 participating organizations,
including vendors, researchers, software library developers, and users.
The goal of the Message Passing Interface is to establish a portable, efficient,
and flexible standard for message passing that will be widely used for writing message
passing programs. As such, MPI is the first standardized, vendor independent, message
passing library. The advantages of developing message passing software using
MPI closely match the design goals of portability, efficiency, and flexibility.
MPI is not an IEEE or ISO standard, but has in fact, become the "industry standard"
for writing message passing programs on HPC platforms.


The UL HPC platform offers to you different MPI implementations:

| MPI suit     |Version(latest)| Compiler                                      |             Compilation command (C )       |
| ------------ | ------------- | --------------------------                    | -----------------------------------------  |
| OpenMPI      | 17.0.1        |C: `mpicc`; C++: `mpicxx`; Fortran `mpifort`   |`mpicc  -Wall [-fopenmp] -O2 [...]`         |
| Intel MPI    | 2.1.1         |C: `mpiicc`; C++: `mpiicpc`; Fortran `mpiifort`|`mpiicc -Wall [-qopenmp] [-xhost] -O2 [...]`|
| MVAPICH2     | 2.3a          |C: `mpicc`; C++: `mpicxx`; Fortran `mpif77` `mpif90` |`mpicc  -Wall [-fopenmp] -O2 [...]`   |



## How to use the OpenMPI in ULHPC
[![](https://miro.medium.com/max/300/0*jOJ8c4u_V4hsQpaV.png){: style="width:300px;float: right;" }](https://www.open-mpi.org/)
The [Open MPI Project](https://www.open-mpi.org/) is an open source [Message Passing Interface](https://www.mpi-forum.org/)
implementation that is developed and maintained by a consortium of academic, research, and industry partners.
Open MPI is therefore able to combine the expertise, technologies, and resources
from all across the High Performance Computing community in order to build the best MPI library available.
Open MPI offers advantages for system and software vendors, application developers and computer science researchers.

To check available versions of OpenMPI at ULHPC type `module spider openmpi`.

??? tip "Available versions of OpenMPI in ULHPC:"

    ```bash
    mpi/OpenMPI/2.1.1-GCC-6.3.0-2.27
    mpi/OpenMPI/2.1.1-GCC-6.3.0-2.28
    mpi/OpenMPI/2.1.3-GCC-6.4.0-2.28
    mpi/OpenMPI/3.1.3-GCC-8.2.0-2.31.1
    mpi/OpenMPI/3.1.3-gcccuda-2019a
    mpi/OpenMPI/3.1.4-GCC-8.2.0-2.31.1
    mpi/OpenMPI/3.1.4-gcccuda-2019a
    ```
### Interactive mode

```bash
# Reserve the node
$ srun -p interactive --time=00:10:00 -N 2 --ntasks-per-node=3 --pty bash -i
# OR, use the 'si' helper script
$ si --time=00:10:00 -N 2 --ntasks-per-node=3 

# Module the OpenMPI and needed environment 
$ module purge             # Clean all previously loaded modules
$ module load swenv/default-env/latest
$ module load mpi/OpenMPI/3.1.4-GCC-8.2.0-2.31.1

# Code execution
$ mpirun --oversubscribe -np 6 ./a.out
```

### Batch job

Example for MPI:

```bash
#!/bin/bash -l
#SBATCH -J OpenMPI (MPI)
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:10:00
#SBATCH -p batch

# Use the RESIF build modules of the UL HPC platform
if [ -f  /etc/profile ]; then
   .  /etc/profile
fi

# Load module openmpi and needed environment 
module purge             # Clean all previously loaded modules
module load swenv/default-env/latest
module load mpi/OpenMPI/3.1.4-GCC-8.2.0-2.31.1

# srun -n $SLURM_NTASKS /path/to/your/hybrid_program
srun -n 56 ./a.out
```

Example for MPI+OpenMP (hybrid):

```bash
#!/bin/bash -l
#SBATCH -J OpenMPI (MPI+OpenMP)
#SBATCH -N 2
#SBATCH --ntasks-per-node=14
#SBATCH --ntasks-per-socket=7
#SBATCH -c 2
#SBATCH --time=00:05:00
#SBATCH -p batch

# Use the RESIF build modules of the UL HPC platform
if [ -f  /etc/profile ]; then
   .  /etc/profile
fi

# Load module openmpi and needed environment 
module purge             # Clean all previously loaded modules
module load mpi/OpenMPI/3.1.4-GCC-8.2.0-2.31.1

export OMP_NUM_THREADS=2

# srun -n $SLURM_NTASKS /path/to/your/hybrid_program
srun -n 56 ./a.out                                                                                         
```


## How to use the Intel MPI in ULHPC
[![](https://www.qbssoftware.com/image/cache/catalog/qbs/intelmpi-1000x1000.png){: style="width:250px;float: right;" }](https://software.intel.com/content/www/us/en/develop/tools/mpi-library.html)
[Intel® MPI](https://software.intel.com/content/www/us/en/develop/tools/mpi-library.html) Library is a multifabric message-passing library that implements
the open-source MPICH specification. Use the library to create, maintain,
and test advanced, complex applications that perform better on high-performance computing (HPC)
clusters based on Intel® processors.


To check available versions of Intel MPI at ULHPC type `module -r spider '.*toolchain/intel.*'`.

??? tip "Available versions of Intel MPI in ULHPC:"

    ```bash
    toolchain/intel/2017a
    toolchain/intel/2018a
    toolchain/intel/2019a
    ```

### Interactive mode
```bash
# Reserve the node
$ srun -p interactive --time=00:10:00 -N 2 --ntasks-per-node=3 --x11 --pty bash -i

# Load module Intel MPI and needed environment 
module purge             # Clean all previously loaded modules
module load swenv/default-env/latest
module load toolchain/intel/2019a
unset I_MPI_PMI_LIBRARY  # This is to use mpirun

# Code execution
$ mpirun -np 6 ./a.out
```

### Batch job

Example for MPI:
```bash
#!/bin/bash -l
#SBATCH -J Intel-MPI (MPI)
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:10:00
#SBATCH -p batch

# Use the RESIF build modules of the UL HPC platform
if [ -f  /etc/profile ]; then
   .  /etc/profile
fi

# Load module Intel MPI and needed environment 
module purge             # Clean all previously loaded modules
module load swenv/default-env/latest
module load toolchain/intel/2019a

# srun -n $SLURM_NTASKS /path/to/your/hybrid_program
srun -n 56 ./a.out
```

Example for MPI+OpenMP (hybrid):
```bash
#!/bin/bash -l
#SBATCH -J Intel-MPI (MPI+OpenMP)
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:05:00
#SBATCH -p batch

# Use the RESIF build modules of the UL HPC platform
if [ -f  /etc/profile ]; then
   .  /etc/profile
fi

# Load module Intel MPI and needed environment 
module purge             # Clean all previously loaded modules
module load swenv/default-env/latest
module load toolchain/intel/2019a

export OMP_NUM_THREADS=2

# srun -n $SLURM_NTASKS /path/to/your/hybrid_program
srun -n 56 ./a.out
```

## How to use the MVAPICH2 in UL-HPC
[![](https://mvapich.cse.ohio-state.edu/static/images/MVAPICH-Stacked.png){: style="width:300px;float: right;" }](https://mvapich.cse.ohio-state.edu/)
[MVAPICH](https://mvapich.cse.ohio-state.edu/) project, led by Network-Based Computing Laboratory (NBCL)
of The Ohio State University. The MVAPICH2 software,
based on MPI 3.1 standard, delivers the best performance,
scalability and fault tolerance for high-end computing systems and
servers using InfiniBand, Omni-Path, Ethernet/iWARP, and RoCE networking technologies.
This software is being used by more than 3,100 organizations in 89
countries worldwide to extract the potential of these emerging networking
technologies for modern systems. As of Oct '20, more than 890,000 downloads
have taken place from this project's site.
This software is also being distributed by many vendors as part of their software distributions.



To check available versions of Intel MPI at MVAPICH2 type `module spider mvapich2`.

??? tip "Available versions of MVAPICH2 in ULHPC:"

    ```bash
    mpi/MVAPICH2/2.2b-GCC-4.9.3-2.25
    mpi/MVAPICH2/2.3a-GCC-6.3.0-2.28
    ```

### Interactive mode
```bash
# Reserve the node
$ srun -p interactive --time=00:10:00 -N 2 --ntasks-per-node=3 --x11 --pty bash -i

# Load the module MVAPICH2 and needed environment 
$ module purge             # Clean all previously loaded modules
$ module load swenv/default-env/v0.1-20170602-production
$ module load mpi/MVAPICH2/2.3a-GCC-6.3.0-2.28

# Compilation
$ mpicc hello.c

# Code execution
$ mpirun -np 4 ./a.out
```

### Batch job

Example for MPI:
```bash
#!/bin/bash -l
#SBATCH -J MVAPICH2 (MPI)
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:10:00
#SBATCH -p batch

# Use the RESIF build modules of the UL HPC platform
if [ -f  /etc/profile ]; then
   .  /etc/profile
fi

# Load the module MVAPICH2 and needed environment
module purge             # Clean all previously loaded modules
module load swenv/default-env/v0.1-20170602-production
module load mpi/MVAPICH2/2.3a-GCC-6.3.0-2.28

# srun -n $SLURM_NTASKS /path/to/your/hybrid_program
srun -n 56 ./a.out
```

Example for MPI+OpenMP (hybrid):

```bash
#!/bin/bash -l
#SBATCH -J MVAPICH2 (MPI+OpenMP)
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:10:00
#SBATCH -p batch

# Use the RESIF build modules of the UL HPC platform
if [ -f  /etc/profile ]; then
   .  /etc/profile
fi

# Load the module MVAPICH2 and needed environment
module purge             # Clean all previously loaded modules
module load swenv/default-env/v0.1-20170602-production
module load mpi/MVAPICH2/2.3a-GCC-6.3.0-2.28

export OMP_NUM_THREADS=2

# srun -n $SLURM_NTASKS /path/to/your/hybrid_program
srun -n 56 ./a.out
```

To know more about MPI programming techniques and optimization,
please refer [ULHPC MPI tutorial](https://ulhpc-tutorials.readthedocs.io/en/latest/parallel/basics/)

##Tuning (or processes pinning) using environmental varibales:
Pinning threads for shared-memory parallelism or binding processes for distributed-memory
parallelism is an advanced way to control how your system distributes the threads or
processes across the available cores. It is important for improving the performance
of your application by avoiding costly remote memory accesses and keeping the
threads or processes close to each other.

### OpenMPI

??? info "Example for MPI"
    ```bash
    #!/bin/bash -l
    #SBATCH -J MPI
    #SBATCH -N 2                         # Number of nodes
    #SBATCH --ntasks-per-node=28         # Number of tasks per node
    #SBATCH --time=00:05:00              # Total run time of the job allocation
    #SBATCH -p batch

    # Load module OpenMPI and needed environment        
    module purge                         # Clean all previously loaded modules
    module load swenv/default-env/latest               
    module load mpi/OpenMPI/3.1.4-GCC-8.2.0-2.31.1

    # Set mpi processes close to each other  and print out CPU affinity    
    mpirun -np 56 --bind-to core --map-by core --report-bindings ./a.out
    ```

??? info "Example for MPI+OpenMP (hybrid)"
    ```bash
    #!/bin/bash -l
    #SBATCH -J MPI+OpenMP (hybrid)
    #SBATCH -N 2                         # Number of nodes
    #SBATCH --ntasks-per-node=28         # Number of tasks per node
    #SBATCH --time=00:05:00              # Total run time of the job allocation
    ##SBATCH --cpus-per-task=2           # Option for OpenMP 
    #SBATCH -p batch

    # Load module OpenMPI and needed environment 
    module purge                         # Clean all previously loaded modules
    module load swenv/default-env/latest         
    module load mpi/OpenMPI/3.1.4-GCC-8.2.0-2.31.1

    # Option for OpenMP threads 
    #export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
    # Or 
    export OMP_NUM_THREADS=2            # Number of threads (openmp)

    # Set mpi processes close to each other  and print out CPU affinity    
    mpirun -np 56 --bind-to core --map-by core --report-bindings ./a.out
    ```
     
To know more information about process pinning for OpenMPI please refer [OpenMPI pinning](https://www.open-mpi.org/doc/v3.0/man1/mpirun.1.php)


### Intel MPI

??? info "Example for MPI"
    ```bash
    #!/bin/bash -l
    #SBATCH -J Intel MPI (MPI)
    #SBATCH -N 2                         # Number of nodes
    #SBATCH --ntasks-per-node=28         # Number of tasks per node
    #SBATCH --time=00:05:00              # Total run time of the job allocation
    #SBATCH -p batch                    

    # Load module Intel MPI and needed environment 
    module purge             # Clean all previously loaded modules
    module load swenv/default-env/latest        
    module load toolchain/intel/2019a

    set I_MPI_PIN=1                      # Enable processes pinning     
    set I_MPI_PIN_DOMAIN=core            # Treat logical core as a MPI Processors  
    set I_MPI_PIN_ORDER=compact          # Order the processes in a compact way to avoid costly memory access. 

    #srun -n $SLURM_NTASKS /path/to/your/hybrid_program
    srun -n 56 ./a.out
    ```

??? info "Example for MPI+OpenMP (hybrid)"
    ```bash
    #!/bin/bash -l
    #SBATCH -J Intel MPI (hybrid)
    #SBATCH -N 2                         # Number of nodes
    #SBATCH --ntasks-per-node=28         # Number of tasks per node
    #SBATCH --time=00:05:00              # Total run time of the job allocation
    #SBATCH -p batch

    # Load module Intel MPI and needed environment 
    module purge                         # Clean all previously loaded modules
    module load swenv/default-env/latest
    module load toolchain/intel/2019a

    set I_MPI_PIN=1                      # Enable processes pinning     
    set I_MPI_PIN_DOMAIN=core            # Treat logical core as a MPI Processors  
    set I_MPI_PIN_ORDER=compact          # Order the processes in a compact way to avoid costly memory access. 

    export OMP_NUM_THREADS=2             # Number of threads (openmp)

    #srun -n $SLURM_NTASKS /path/to/your/hybrid_program
    srun -n 56 ./a.out
    ```
To know more information about process pinning for Intel MPI please refer [Intel MPI pinning](https://software.intel.com/content/www/us/en/develop/documentation/mpi-developer-reference-linux/top/environment-variable-reference/process-pinning/interoperability-with-openmp.html)


### MVAPICH2

??? info "Example for MPI"
    ```bash
    #!/bin/bash -l
    #SBATCH -J MVAPICH2 (MPI)
    #SBATCH -N 2                         # Number of nodes
    #SBATCH --ntasks-per-node=28         # Number of tasks per node
    #SBATCH --time=00:05:00              # Total run time of the job allocation
    #SBATCH -p batch

    # Load module MVAPICH2 and needed environmental modules 
    module purge                          # Clean all previously loaded modules 
    module load swenv/default-env/v0.1-20170602-production
    module load mpi/MVAPICH2/2.3a-GCC-6.3.0-2.28

    export MV2_CPU_BINDING_POLICY=bunch   # Uniform processes distribution (hybrid|bunch|scatter)
    export MV2_CPU_BINDING_LEVEL=core     # Binding MPI processes (core|socket|numanode)
    export MV2_SHOW_CPU_BINDING=1         # Print out the CPU affinity 
    
    #srun -n $SLURM_NTASKS /path/to/your/hybrid_program
    srun -n 56 ./a.out
    ```

??? info "Example for MPI+OpenMP (hybrid)"
    ```bash
    #!/bin/bash -l
    #SBATCH -J MVAPICH2 (hybrid)
    #SBATCH -N 2                         # Number of nodes
    #SBATCH --ntasks-per-node=28         # Number of tasks per node
    #SBATCH --time=00:05:00              # Total run time of the job allocation
    #SBATCH -p batch

    # Load module MVAPICH2 and needed environmental modules 
    module purge                          # Clean all previously loaded modules 
    module load swenv/default-env/v0.1-20170602-production
    module load mpi/MVAPICH2/2.3a-GCC-6.3.0-2.28

    export MV2_ENABLE_AFFINITY=0          # Disable for hybrid mode 
    export MV2_CPU_BINDING_POLICY=hybrid  # Enable hybrid (hybrid|bunch|scatter)
    export MV2_CPU_BINDING_LEVEL=core     # Binding MPI processes (core|socket|numanode)
    export MV2_SHOW_CPU_BINDING=1         # Print out the CPU affinity 
    
    export OPM_NUM_THREADS=2              # Number of threads (openmp)
    
    #srun -n $SLURM_NTASKS /path/to/your/hybrid_program
    srun -n 56 ./a.out
    ```
To know more information about process pinning for MVAPICH2 please refer [MVAPICH2 pinning](http://mvapich.cse.ohio-state.edu/userguide/)

## Additional information
* [mpi-forum](https://www.mpi-forum.org/docs/)
* [Intel® C++ Compiler 19.1 Developer Guide and Reference](https://software.intel.com/content/www/us/en/develop/documentation/cpp-compiler-developer-guide-and-reference/top.html)
* [Step by Step Performance Optimization with Intel® C++ Compiler](https://software.intel.com/content/www/us/en/develop/articles/step-by-step-optimizing-with-intel-c-compiler.html)


