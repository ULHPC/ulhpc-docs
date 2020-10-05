# VTune

## Table of Contents
1. [Introduction](#introduction)
2. [Environmental models for VTune on UL-HPC](#environmental-models-for-vtune-on-ul-hpc)
3. [Interactive Mode](#interactive-mode)
4. [Batch Mode](#batch-mode)
5. [Additional Information](#additional-information)

## Introduction

See the [Intel VTune Amplifier documentation](https://software.intel.com/en-us/vtune-help) for general usage.

!!! tip "VTune command name changes in version 2020"
	Version 2020 of VTune includes several significant upgrades in 
	functionality. It also includes some command name changes. The 
	command line interface to VTune has changed from `amplxe-cl` to 
	simply `vtune`, and the GUI has changed from `amplxe-gui` to 
	`vtune-gui`. Intel provides symbolic links such that the old 
	commands `amplxe-cl` and `amplxe-gui` will continue to work, 
	but those symbolic links may be removed in a future version.

<!--
VTune is available on all NERSC production systems by loading the
VTune module.

```shell
module load vtune
```
-->


!!! tip "Recommended compiler flags for VTune performance collection"
    Intel provides a
    [page](https://software.intel.com/en-us/vtune-help-compiler-switches-for-performance-analysis-on-linux-targets)
    documenting their recommended compiler flags for compiling applications
    when collecting performance data with VTune. Users will generally have the
    best results when compiling codes using the Intel compilers, although the
    [CCE](../../compilers/native#cray) and [GCC](../../compilers/native/#gnu)
    compilers can also produce application suitable for analysis with VTune.

When collecting performance data with VTune, it is **strongly
recommended** to add the Slurm flag `--perf=vtune` or
`--perf=<vtune_module_version>` to your job allocation, where
`<vtune_module_version>` is the full module name of the VTune version
you want to use.

!!! warning 
	Certain VTune collections can function without the 
	`#SBATCH --perf=vtune` flag, but many others will fail.

!!! tip "Defer finalization" 
	It is generally recommended to defer finalization when running 
	on KNL. Finalization is an inherently serial process and the 
	individual core performance on KNL is very poor. Thus, when 
	running VTune on KNL, add the parameter	`-finalization-mode=deferred`

## Environmental models for VTune on UL-HPC:
```
module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load tools/VTune/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0
```




## Interactive Mode

```
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
```shell
#!/bin/bash -l
#SBATCH -J VTune
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

```shell
#!/bin/bash -l
#SBATCH -J VTune
#SBATCH -N 2
#SBATCH --ntasks-per-node=56
#SBATCH --time=00:10:00
#SBATCH -p batch

module purge 
module load swenv/default-env/v1.2-20191021-production
module load toolchain/intel/2019a
module load tools/VTune/2019_update4
module load vis/GTK+/3.24.8-GCCcore-8.2.0

srun -n 56 amplxe-cl -collect uarch-exploration -r vtune_mpi -- ./a.out
```

```
# Report collection
$ amplxe-cl -report uarch-exploration -report-output output -r vtune_mpi

# Result visualization 
$ amplxe-gui vtune_mpi
```
The below figure shows the hybrid(MPI+OpenMP) programming analysis results:

![VTune MPI result](images/MPI-VTune.png)






















<!--
```slurm
#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=1
#SBATCH --time=00:30:00
#SBATCH --perf=vtune
# ... additional sbatch parameters ...

module load vtune

vtune -finalization-mode=deferred -collect ... -r <result-dir> -- <command-to-profile>

# in some cases, it one might want to copy over the libraries need to finalize
vtune -archive -r <result-dir>
```

and then finalize on a login node:

```shell
vtune -finalize -result-dir <PATH>
```

## Using VTune with Shifter

VTune can be attached to a Shifter container by executing the process
in the background and then attaching VTune to the process via the PID
(process identifier).

!!! fail "Cannot directly run collection on containers"
	The following will not work:

	```shell
	vtune -collect ... -- shifter <command-to-execute-in-container>
	```

The recommended method is as follows:

```slurm
#!/bin/bash
#SBATCH --qos=debug
#SBATCH --nodes=1
#SBATCH --time=00:30:00
#SBATCH --perf=vtune
#SBATCH --image=<username/some-image>
# ... additional sbatch parameters ...

module load vtune

PID_FILE=$(mktemp pid.XXXXXXX)

# the first "&" causes the command to execute in the background
# "echo $!" prints the PID
# "&> ${PID_FILE}" writes the PID to the temporary file
shifter <command-to-execute-in-container> & echo $! &> ${PID_FILE}

# read the PID from the file
TARGET_PID=$(cat ${PID_FILE})

# attach VTune to the process
vtune -collect <collection-mode> --target-pid=${TARGET_PID} ...
```

!!! warning "VTune finalization with Shifter"
        In the [Using VTune](#using-vtune) section, it was recommended to not finalize
        on KNL. However, when using containers, deferring finalization creates a
        problem because the binaries needed for finalization exist only within the
        container. Due to this fact, it is recommended to not defer finalization when
        using containers.

## VTune + Shifter Example

```slurm
#!/bin/bash
#SBATCH --qos=regular
#SBATCH --constraint=knl
#SBATCH --nodes=1
#SBATCH --time=03:00:00
#SBATCH --job-name=tomopy_gridrec
#SBATCH --output=out_tomopy_%j.log
#SBATCH --image=jrmadsen/tomopy-reference:gcc
#SBATCH --perf=vtune

set -o errexit

# ensure VTune module is loaded
module load vtune

# this format of assignment only sets the variable to the specified value
# if not already set in the environment
: ${OMP_NUM_THREADS:=1}
: ${NUMEXPR_MAX_THREADS:=$(nproc)}
: ${VTUNE_COLLECTION_MODE:="advanced-hotspots"}
: ${VTUNE_SAMPLING_INTERVAL:=25}
: ${VTUNE_RESULTS_DIR:=$(mktemp -d ${PWD}/run-${VTUNE_COLLECTION_MODE}-XXXXX)}

export OMP_NUM_THREADS
export NUMEXPR_MAX_THREADS
export VTUNE_COLLECTION_MODE
export VTUNE_SAMPLING_INTERVAL
export VTUNE_RESULTS_DIR

# make sure empty, let vtune create directory
rm -rf ${VTUNE_RESULTS_DIR}

# use mktemp to ensure guard against multiple jobs in same dir
PID_FILE=$(mktemp pid.XXXXXX)

echo -e "\n### Submitting shifter job into background and storing PID in file: ${PID_FILE} ###\n"
shifter /opt/conda/bin/python ./run_tomopy.py -a gridrec -n 256 -s 512 -f jpeg -S 1 -c 8 -p shepp3d -i 5 & echo $! &> ${PID_FILE}

echo -e "\n### Reading PID file: ${PID_FILE} ###\n"
TARGET_PID=$(cat ${PID_FILE})

# echo the ps for debugging
echo -e "\n### Target PID: ${TARGET_PID} ###\n"
ps

# echo the environment for reference
echo -e "\n### Environment ###\n"
env

echo -e "\n### Attaching VTune process to PID ${TARGET_PID} ###\n"
vtune \
    -collect ${VTUNE_COLLECTION_MODE} \
    -knob collection-detail=hotspots-sampling \
    -knob event-mode=all \
    -knob analyze-openmp=true \
    -knob sampling-interval=${VTUNE_SAMPLING_INTERVAL} \
    -data-limit=0 \
    --target-pid=${TARGET_PID} \
    -r ${VTUNE_RESULTS_DIR}

echo -e "\nCompleted\n"
```
-->