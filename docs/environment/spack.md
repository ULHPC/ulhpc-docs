# Spack: A Package Manager on the UL HPC Platform

[<img width='400px' src='https://cdn.rawgit.com/spack/spack/develop/share/spack/logo/spack-logo-text.svg'/>](https://spack.readthedocs.io/en/latest/#)



## Introduction to Spack


A brief introduction to Spack will be added here.

## Setting up Spack

!!! note
    The guide is also applicable to other HPC clusters where users need to manage components such as MPI libraries, compilers, and other software through the `module` system.


### Connection to a compute node


```{.sh .copy}
si -N 1 -n 16 -c 1 -t 0-02:00:00 # on iris: -C broadwell or -C skylake
```

??? note "Allocation Details"

    `si` is a shell function that wraps the `salloc` command to simplify interactive Slurm job allocation.  
    It stands for:

    ```bash
    salloc -p interactive --qos debug -C batch ${options}
    ```
    - `${options}`: any additional arguments passed to `si` (e.g., `-N`, `-n`, `-c`, `-t`, etc.)

    ```bash
    si -N 1 -n 16 -c 1 -t 0-02:00:00
    ```

    This allocates:

    - 1 node (`-N 1`)
    - 16 MPI tasks (`-n 16`)
    - 1 CPU per task (`-c 1`)
    - for a wall time of 2 hours (`-t 0-02:00:00`) 

    !!! info "Iris Cluster"

        On the **Iris** cluster, 

        - Use `-C broadwell` or  `-C skylake` 

        **Examples:**
        ```bash
        si -N 1 -n 16 -c 1 -t 0-02:00:00 -C broadwell
        ```


### Clone & Setup Spack

Clone and setup spack in `$HOME`  - it has better much better performance for 
small files than `$SCRATCH`

``` { .sh .copy }
cd $HOME
git clone --depth=2 https://github.com/spack/spack.git
cd spack
```
To make Spack available in your shell session, source its environment setup script:

``` { .sh .copy }
source $HOME/spack/share/spack/setup-env.sh
```
For convenience, this line can be added to the .`bashrc` file to make Spack automatically available in every new shell session.

### Define System-Provided Packages

`packages.yaml` A spack configuration file used to tell Spack what tools and versions already exist on the cluster, so Spack can use those instead of building everything again.Create a packages.yaml file under: `$HOME/.spack/packages.yaml` 

``` { .sh .copy }
touch $HOME/.spack/packages.yaml
```


with the following contents:

``` { .sh .copy }
 packages:
  gcc:
    externals:
    - spec: gcc@13.2.0+binutils languages:='c,c++,fortran'
      modules:
      - compiler/GCC/13.2.0
      extra_attributes:
        compilers:
          c: /opt/apps/easybuild/systems/aion/rhel810-20250405/2023b/epyc/software/GCCcore/13.2.0/bin/gcc
          cxx: /opt/apps/easybuild/systems/aion/rhel810-20250405/2023b/epyc/software/GCCcore/13.2.0/bin/g++
          fortran: /opt/apps/easybuild/systems/aion/rhel810-20250405/2023b/epyc/software/GCCcore/13.2.0/bin/gfortran
    buildable: false
  binutils:
    externals:
    - spec: binutils@2.40
      modules:
      - tools/binutils/2.40-GCCcore-13.2.0
    buildable: false
  libevent:
    externals:
    - spec: libevent@2.1.12
      modules:
      - lib/libevent/2.1.12-GCCcore-13.2.0
    buildable: false
  libfabric:
    externals:
    - spec: libfabric@1.19.0
      modules:
      - lib/libfabric/1.19.0-GCCcore-13.2.0
    buildable: false
  libpciaccess:
    externals:
    - spec: libpciaccess@0.17
      modules:
      - system/libpciaccess/0.17-GCCcore-13.2.0
    buildable: false
  libxml2:
    externals:
    - spec: libxml2@2.11.5
      modules:
      - lib/libxml2/2.11.5-GCCcore-13.2.0
    buildable: false
  hwloc:
    externals:
    - spec: hwloc@2.9.2+libxml2
      modules:
      - system/hwloc/2.9.2-GCCcore-13.2.0
    buildable: false
  mpi:
    buildable: false
  munge:
    externals:
    - spec: munge@0.5.13
      prefix: /usr
    buildable: false
  numactl:
    externals:
    - spec: numactl@2.0.16
      modules:
      - tools/numactl/2.0.16-GCCcore-13.2.0
    buildable: false
  openmpi:
    variants: fabrics=ofi,ucx schedulers=slurm
    externals:
    - spec: openmpi@4.1.6
      modules:
      - mpi/OpenMPI/4.1.6-GCC-13.2.0
    buildable: false
  pmix:
    externals:
    - spec: pmix@4.2.6
      modules:
      - lib/PMIx/4.2.6-GCCcore-13.2.0
    buildable: false
  slurm:
    externals:
    - spec: slurm@23.11.10 sysconfdir=/etc/slurm
      prefix: /usr
    buildable: false
  ucx:
    externals:
    - spec: ucx@1.15.0
      modules:
      - lib/UCX/1.15.0-GCCcore-13.2.0
    buildable: false
  zlib:
    externals:
    - spec: zlib@1.2.13
      modules:
      - lib/zlib/1.2.13-GCCcore-13.2.0
    buildable: false

```
This tells Spack to use the system available GCC, binutils and OpenMPI with the native fabrics.

## Building FEniCS

Create an environment and install FEniCS
``` { .sh .copy }
cd ~
spack env create -d fenicsx-main-20230126/ 
spack env activate fenicsx-main-20230126/
spack add py-fenics-dolfinx@main fenics-dolfinx+adios2 adios2+python petsc+mumps
# Change @main to e.g. @0.7.2 in the above if you want a fixed version.
spack concretize
spack install -j16
``` 
or the same directly in `spack.yaml` in `$SPACK_ENV`

``` { .sh .copy }
spack:
  # add package specs to the `specs` list
  specs:
  - py-fenics-dolfinx@main
  - fenics-dolfinx@main+adios2
  - petsc+mumps
  - adios2+python
  view: true
  concretizer:
    unify: true
```
The following are also commonly used in FEniCS scripts and may be useful

``` { .sh .copy }
spack add gmsh+opencascade py-numba py-scipy py-matplotlib
```
It is possible to build a specific version (git ref) of DOLFINx. Note that the hash must be the full hash. It is best to specify appropriate git refs on all components.

``` { .sh .copy }
# This is a Spack Environment file.
#
# It describes a set of packages to be installed, along with
# configuration settings.
spack:
  # add package specs to the `specs` list
  specs:
  - fenics-dolfinx@git.4f575964c70efd02dca92f2cf10c125071b17e4d=main+adios2
  - py-fenics-dolfinx@git.4f575964c70efd02dca92f2cf10c125071b17e4d=main

  - py-fenics-basix@git.2e2a7048ea5f4255c22af18af3b828036f1c8b50=main
  - fenics-basix@git.2e2a7048ea5f4255c22af18af3b828036f1c8b50=main

  - py-fenics-ufl@git.b15d8d3fdfea5ad6fe78531ec4ce6059cafeaa89=main

  - py-fenics-ffcx@git.7bc8be738997e7ce68ef0f406eab63c00d467092=main

  - fenics-ufcx@git.7bc8be738997e7ce68ef0f406eab63c00d467092=main

  - petsc+mumps
  - adios2+python
  view: true
  concretizer:
    unify: true
```

It is also possible to build only the C++ layer using


``` { .sh .copy }
spack add fenics-dolfinx@main+adios2 py-fenics-ffcx@main petsc+mumps
```
To rebuild FEniCSx from main branches inside an existing environment


``` { .sh .copy }
spack install --overwrite -j16 fenics-basix py-fenics-basix py-fenics-ffcx fenics-ufcx py-fenics-ufl fenics-dolfinx py-fenics-dolfinx
```


## Testing the build

Quickly test the build with
``` { .sh .copy }
srun python -c "from mpi4py import MPI; import dolfinx"
```

## Using the build

See the uni.lu documentation for full details - using the environment should be as 
simple as adding the following where `...` is the name/folder of your environment.

``` { .sh .copy }
#!/bin/bash -l
source $HOME/spack/share/spack/setup-env.sh
spack env activate ...
```

## Known issues

Workaround for broken Python module find for gmsh on uni.lu cluster

``` { .sh .copy }

export PYTHONPATH=$SPACK_ENV/.spack-env/view/lib64/:$PYTHONPATH

```
Workaround for broken Python module find for adios2 (seems broken in Spack)

``` { .sh .copy }

export PYTHONPATH=$(find $SPACK_ENV/.spack-env -type d -name 'site-packages' | grep venv):$PYTHONPATH

```