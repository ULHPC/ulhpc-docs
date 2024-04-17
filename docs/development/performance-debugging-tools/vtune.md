# VTune

[![](https://software.intel.com/content/dam/develop/public/us/en/images/diagrams-infographics/screen-intel-vtune-profiler-16x9.png.rendition.intel.web.720.405.png){: style="width:300px;float: right;" }](https://software.intel.com/content/www/us/en/develop/tools/vtune-profiler.html)
Use [Intel VTune](https://software.intel.com/content/www/us/en/develop/tools/vtune-profiler.html) Profiler to profile serial and multithreaded applications that are executed on a variety of hardware platforms (CPU, GPU, FPGA). The tool is delivered as a Performance Profiler with Intel Performance Snapshots and supports local and remote target analysis on the Windows*, Linux*, and Android* platforms.
Without the right data, you’re guessing about how to improve software performance and are unlikely to make the most effective improvements.
Intel® VTune™ Profiler collects key profiling data and presents it with a powerful interface that simplifies its analysis and interpretation. 

## Environmental models for VTune on ULHPC:
```bash
module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load tools/VTune/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0
```

## Interactive Mode

```bash
# Compilation
$ icc -qopenmp example.c

# Code execution
$ export OMP_NUM_THREADS=16
$ amplxe-cl -collect hotspots -r my_result ./a.out
```
To see the result in GUI `$ amplxe-gui my_result`

![VTune OpenMP result](images/OpenMP-VTune.png)

`$ amplxe-cl` will list out the analysis types and `$ amplxe-cl -hlep report` will list out available reports in VTune.

## Batch Mode

### Shared Memory Programming Model (OpenMP)
```bash
#!/bin/bash -l
#SBATCH -J VTune
###SBATCH -A <project_name>
#SBATCH -N 1
#SBATCH -c 28
#SBATCH --time=00:10:00
#SBATCH -p batch

module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load tools/VTune/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0

export OMP_NUM_THREADS=16
amplxe-cl -collect hotspots-r my_result ./a.out
```

### Distributed Memory Programming Model

To compile just `MPI` application run `$ mpiicc example.c`
and for `MPI+OpenMP` run `$ mpiicc -qopenmp example.c`

```bash
#!/bin/bash -l
#SBATCH -J VTune
###SBATCH -A <project_name>
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:10:00
#SBATCH -p batch

module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load tools/VTune/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0

srun -n ${SLURM_NTASKS} amplxe-cl -collect uarch-exploration -r vtune_mpi -- ./a.out
```

```bash
# Report collection
$ amplxe-cl -report uarch-exploration -report-output output -r vtune_mpi

# Result visualization 
$ amplxe-gui vtune_mpi
```
The below figure shows the hybrid(MPI+OpenMP) programming analysis results:

![VTune MPI result](images/MPI-VTune.png)

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).



