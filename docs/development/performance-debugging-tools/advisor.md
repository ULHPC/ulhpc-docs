# Intel Advisor
[![](https://software.intel.com/content/dam/develop/public/us/en/images/diagrams-infographics/all-tools-16x9.png.rendition.intel.web.978.550.png){: style="width:300px;float: right;" }](https://software.intel.com/content/www/us/en/develop/tools/advisor.html)
[Intel Advisor](https://software.intel.com/content/www/us/en/develop/tools/advisor.html) provides two workflows to help ensure that Fortran, C, and C++
applications can make the most of modern Intel processors. Advisor contains
three key capabilities:

* [Vectorization
  Advisor](https://software.intel.com/en-us/advisor/features/vectorization)
  identifies loops that will benefit most from vectorization, specifies what is
  blocking effective vectorization, finds the benefit of alternative data
  reorganizations, and increases the confidence that vectorization is safe.
* [Threading
  Advisor](https://software.intel.com/en-us/advisor/features/threading) is used
  for threading design and prototyping and to analyze, design, tune, and check
  threading design options without disrupting normal code development.
* [Advisor
  Roofline](https://software.intel.com/en-us/articles/getting-started-with-intel-advisor-roofline-feature)
  enables visualization of actual performance against hardware-imposed
  performance ceilings (rooflines) such as memory bandwidth and compute
  capacity - which provide an ideal roadmap of potential optimization steps.

The links to each capability above provide detailed information regarding how
to use each feature in Advisor. For more information on Intel Advisor, visit
[this page](https://software.intel.com/en-us/advisor).

## Environmental models for Advisor on UL-HPC¶
```bash
module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load perf/Advisor/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0
```

## Interactive mode
```bash
# Compilation
$ icc -qopenmp example.c

# Code execution
$ export OMP_NUM_THREADS=16
$ advixe-cl -collect survey -project-dir my_result -- ./a.out

# Report collection
$ advixe-cl -report survey -project-dir my_result

# To see the result in GUI
$ advixe-gui my_result
```
![VTune OpenMP result](images/OpenMP-VTune.png)

`$ advixe-cl` will list out the analysis types and `$ advixe-cl -hlep report` will list out available reports in Advisor.


## Batch mode
### Shared memory programming model (OpenMP)
Example for the batch script:
```bash
#!/bin/bash -l
#SBATCH -J Advisor
#SBATCH -N 1
###SBATCH -A <project_name>
#SBATCH -c 28
#SBATCH --time=00:10:00
#SBATCH -p batch

module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load perf/Advisor/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0

export OMP_NUM_THREADS=16
advixe-cl -collect survey -project-dir my_result -- ./a.out
```


### Distributed memory programming model (MPI)
To compile just `MPI` application run `$ mpiicc example.c` and for `MPI+OpenMP` run `$ mpiicc -qopenmp example.c`

Example for the batch script:
```bash
#!/bin/bash -l
#SBATCH -J Advisor
#SBATCH -N 2
###SBATCH -A <project_name>
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:10:00
#SBATCH -p batch

module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load perf/Advisor/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0

srun -n ${SLURM_NTASKS} advixe-cl --collect survey --project-dir result -- ./a.out
```
To collect the result and see the result in GUI use the below commands
```bash
# Report collection
$ advixe-cl --report survey --project-dir result

# Result visualization 
$ advixe-gui result
```
The below figure shows the hybrid(MPI+OpenMP) programming analysis results:

![VTune MPI result](images/MPI-VTune.png)

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).
