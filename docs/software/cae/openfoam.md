[![](https://i.dlpng.com/static/png/7149729_preview.png){: style="width:300px;float: right;" }](url)

[OpenFOAM](https://openfoam.org/) is the free, open source CFD software developed primarily by OpenCFD Ltd since 2004.
It has a large user base across most areas of engineering and science,
from both commercial and academic organisations. OpenFOAM has an extensive
range of features to solve anything from complex fluid flows involving chemical reactions,
turbulence and heat transfer, to acoustics, solid mechanics and electromagnetics

## Available versions of OpenFOAM in ULHPC
To check available versions of OpenFOAM at ULHPC type `module spider openfoam`.
The following versions of OpenFOAM are available in ULHPC:
```bash
# Available versions
cae/OpenFOAM/v1712-intel-2018a
cae/OpenFOAM/v1812-foss-2019a   
```

## Interactive mode
To run an OpenFOAM in the interactive mode, please follow the following steps:
```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p batch --time=00:30:00 --ntasks 1 -c 4 --x11

# Load the required version of OpenFOAM and Intel environment
$ module load swenv/default-env/v1.1-20180716-production
$ module load cae/OpenFOAM/v1712-intel-2018a

# Load the OpenFOAM environment
$ source $FOAM_BASH

$ mkdir OpenFOAM
$ cd OpenFOAM

# Copy the example to your local folder (cavity example)
$ cp -r /opt/apps/resif/data/production/v1.1-20180716/default/software/cae/OpenFOAM/v1712-intel-2018a/OpenFOAM-v1712/tutorials/incompressible/icoFoam/cavity/cavity .
$ cd cavity

# To initialize the mesh
$ blockMesh

# Run the simulation
$ icoFoam

# Visualize the solution
$ paraFoam
```

## Batch mode
Example of computational domain preparation (Dambreak example).
```bash
$ mkdir OpenFOAM
$ cd OpenFOAM
$ cp -r /opt/apps/resif/data/production/v1.1-20180716/default/software/cae/OpenFOAM/v1712-intel-2018a/OpenFOAM-v1712/tutorials/multiphase/interFoam/laminar/damBreak/damBreak .
$ blockMesh
$ cd damBreak/system
```
Open a `decomposeParDict` and set `numberOfSubdomains 16` where `n` is number of MPI processor.
And do `blockMesh` to prepare the computational domain (mesh) and finally do the `decomposePar` to
repartition the mesh domain. 

```bash
#!/bin/bash -l
#SBATCH -J OpenFOAM
#SBATCH -N 1
#SBATCH --ntasks-per-node=28
#SBATCH --ntasks-per-socket=14
#SBATCH -c 1
#SBATCH --time=00:30:00
#SBATCH -p batch

# Write out the stdout+stderr in a file
#SBATCH -o output.txt

# Mail me on job start & end
#SBATCH --mail-user=myemailaddress@universityname.domain
#SBATCH --mail-type=BEGIN,END

# To get basic info. about the job
echo "== Starting run at $(date)"
echo "== Job ID: ${SLURM_JOBID}"
echo "== Node list: ${SLURM_NODELIST}"
echo "== Submit dir. : ${SLURM_SUBMIT_DIR}"

# Load the required version of OpenFOAM and needed environment
module purge
module load swenv/default-env/v1.1-20180716-production
module load cae/OpenFOAM/v1712-intel-2018a

# Load the OpenFOAM environment
source $FOAM_BASH

srun interFoam -parallel
```

## Additional information
To know more information about OpenFOAM tutorial/documentation,
please refer https://www.openfoam.com/documentation/tutorial-guide/

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
