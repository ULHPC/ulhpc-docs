# Intel Inspector
[![](https://software.intel.com/content/dam/develop/public/us/en/images/screenshots/screen-intel-inspector-16x9.png.rendition.intel.web.720.405.png){: style="width:300px;float: right;" }](https://software.intel.com/content/www/us/en/develop/tools/inspector.html)
[Intel Inspector](https://software.intel.com/content/www/us/en/develop/tools/inspector.html) is a memory and threading error checking tool for users
developing serial and multithreaded applications on Windows and Linux operating
systems. The essential features of Intel Inspector for Linux are:

* Standalone GUI and command-line environments
* Preset analysis configurations (with some configurable settings) and the
  ability to create custom analysis configurations to help the user control
  analysis scope and cost
* Interactive debugging capability so one can investigate problems more deeply
  during the analysis
* A large number of reported memory errors, including on-demand memory leak
  detection
* Memory growth measurement to help ensure that the application uses no more
  memory than expected
* Data race, deadlock, lock hierarchy violation, and cross-thread stack access
  error detection


### Options for the Collect Action

| Option | Description                     |
|--------|---------------------------------|
| mi1    | Detect memory leaks             |
| mi2    | Detect memory problems          |
| mi3    | Locate memory problems          |
| ti1    | Detect deadlocks                |
| ti2    | Detect deadlocks and data races |
| ti3    | Locate deadlocks and data races |

### Options for the Report Action

| Option       | Description |
|--------------|-------------|
| summary      | A brief statement of the total number of new problems found grouped by problem type |
| problems     | A detailed report of detected problem sets in the result, along with their location in the source code |
| observations | A detailed report of all code locations used to form new problem sets |
| status       | A brief statement of the total number of detected problems and the number that are *not investigated*, grouped by category |

For more information on Intel Inspector, please visit
https://software.intel.com/en-us/intel-inspector-xe.

## Environmental models for Inspector on UL-HPC

```bash
module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load tools/Inspector/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0
```

### Interactive Mode
To launch Inspector on Iris, we recommend that you use the command
line tool  `inspxe-cl`  to collect data via batch jobs and then display
results using the GUI, `inspxe-gui`, on a login node.

```bash
# Compilation
$ icc -qopenmp example.cc

# Result collection
$ inspxe-cl -collect mi1 -result-dir mi1 -- ./a.out

# Result view
$ cat inspxe-cl.txt
=== Start: [2020/04/08 02:11:50] ===
2 new problem(s) found
1 Memory leak problem(s) detected
1 Memory not deallocated problem(s) detected
=== End: [2020/04/08 02:11:55] ===
```

## Batch Mode
### Shared memory programming model (OpenMP)

Example for the batch script:

```bash
#!/bin/bash -l
#SBATCH -J Inspector
#SBATCH -N 1
###SBATCH -A <project_name>
#SBATCH -c 28
#SBATCH --time=00:10:00
#SBATCH -p batch

module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load tools/Inspector/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0

inspxe-cl -collect mi1 -result-dir mi1 -- ./a.out`
```
To see the result:

```bash
# Result view
$ cat inspxe-cl.txt
=== Start: [2020/04/08 02:11:50] ===
2 new problem(s) found
1 Memory leak problem(s) detected
1 Memory not deallocated problem(s) detected
=== End: [2020/04/08 02:11:55] ===
```

### Distributed memory programming model (MPI)
To compile:
```bash
# Compilation
$ mpiicc -qopenmp example.cc
```
Example for batch script:
```shell
#!/bin/bash -l
#SBATCH -J Inspector
#SBATCH -N 2
###SBATCH -A <project_name>
#SBATCH --ntasks-per-node 28
#SBATCH --time=00:10:00
#SBATCH -p batch

module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load tools/Inspector/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0

srun -n {SLURM_NTASKS} inspxe-cl -collect=ti2 -r result ./a.out
```

To see result output:
```bash
$ cat inspxe-cl.txt
0 new problem(s) found
=== End: [2020/04/08 16:41:56] ===
=== End: [2020/04/08 16:41:56] ===
0 new problem(s) found
=== End: [2020/04/08 16:41:56] ===
```

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).
