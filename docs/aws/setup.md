# Environment Setup

AWS suggest to use Spack to setup your software environment. There is no hard requirement that you must use Spack. However we have included it here, as it is a quick, simple way to setup a development environment.
The official ULHPC swsets are not available on the AWS cluster. If you prefer to use [EasyBuild](../environment/easybuild) or manually compile softwares, please refer to the [ULHPC software documentation](../software/build) for this purpose.

## Install [Spack](ihttps://spack.io/)

* To do this, please clone the Spack GitHub repository into a `SPACK_ROOT` which is defined to be on a your project directory, i.e., `/shared/project/<project_id>`.

* Then add the configuration to you `~/.bashrc` file.

* You may wish to change the location of the` SPACK_ROOT` to fit your specific cluster configuration.

* Here, we consider the release v0.19 of Spack from the releases/v0.19 branch, however, you may wish to checkout the develop branch for the latest packages.

```bash
git clone -c feature.manyFiles=true -b releases/v0.19 https://github.com/spack/spack $SPACK_ROOT
```

* Then, add the following lines in your .bashrc

```bash
export PROJECT="/shared/projects/<project_id>"
export SPACK_ROOT="${PROJECT}/spack"
if [[ -f "${SPACK_ROOT}/share/spack/setup-env.sh" ]];then
    source ${SPACK_ROOT}/share/spack/setup-env.sh" 
fi
```

!!! danger "Adapt accordingly"
    * Do **NOT** forget to replace `<project_id>` with your project name


## Spack Binary Cache

At [ISC'22](https://www.isc-hpc.com/), in conjunction with the Spack v0.18 release, AWS announced a collaborative effort to host a Binary Cache .
The binary cache stores prebuilt versions of common HPC packages, meaning that the installation process is reduced to relocation rather than compilation. To increase flexibility the binary cache contains package builds with different variants and built with different compilers.
The purpose of the binary cache is to drastically speed up package installation, especially when long dependency chains exist.


The binary cache is periodically updated with the latest versions of packages, and is released in conjunction with Spack releases. Thus you can use the v0.18 binary cache to have packages specifically from that Spack release. Alternatively, you can make use of the develop binary cache, which is kept up to date with the Spack develop branch.

* To add the develop binary cache, and trusting the associated gpg keys:

```bash
spack mirror add binary_mirror https://binaries.spack.io/develop
spack buildcache keys -it
```

## Installing packages

The notation for installing packages, when the binary cache has been enabled is unchanged. Spack will first check to see if the package is installable from the binary cache, and only upon failure will it install from source. We see confirmation of this in the output:

```bash
$ spack install bzip2
==> Installing bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k
==> Fetching https://binaries.spack.io/develop/build_cache/linux-amzn2-x86_64_v4-gcc-7.3.1-bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k.spec.json.sig
gpg: Signature made Fri 01 Jul 2022 04:21:22 AM UTC using RSA key ID 3DB0C723
gpg: Good signature from "Spack Project Official Binaries <maintainers@spack.io>"
==> Fetching https://binaries.spack.io/develop/build_cache/linux-amzn2-x86_64_v4/gcc-7.3.1/bzip2-1.0.8/linux-amzn2-x86_64_v4-gcc-7.3.1-bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k.spack
==> Extracting bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k from binary cache
[+] /shared/spack/opt/spack/linux-amzn2-x86_64_v4/gcc-7.3.1/bzip2-1.0.8-paghlsmxrq7p26qna6ml6au4fj2bdw6k
```

## Bypassing the binary cache

* Sometimes we might want to install a specific package from source, and bypass the binary cache. To achieve this we can pass the `--no-cache` flag to the install command. We can use this notation to install cowsay.
```bash
spack install --no-cache cowsay
```

* To compile any software we are going to need a compiler. Out of the box Spack does not know about any compilers on the system. To list your registered compilers, please use the following command:
```bash
spack compiler list
```

It will return an empty list the first time you used after installing Spack
```bash
 ==> No compilers available. Run `spack compiler find` to autodetect compilers
```

* AWS ParallelCluster installs GCC by default, so you can ask Spack to discover compilers on the system:
```bash
spack compiler find
```

This should identify your GCC install. In your case a conmpiler should be found.
```bash
==> Added 1 new compiler to /home/ec2-user/.spack/linux/compilers.yaml
     gcc@7.3.1
 ==> Compilers are defined in the following files:
     /home/ec2-user/.spack/linux/compilers.yaml
```

## Install other compilers

This default GCC compiler may be sufficient for many applications, we may want to install a newer version of GCC or other compilers in general. Spack is able to install compilers like any other package.


## Newer GCC version

For example we can install a version of GCC 11.2.0, complete with binutils, and then add it to the Spack compiler list.
```·bash
spack install -j [num cores] gcc@11.2.0+binutils
spack load gcc@11.2.0
spack compiler find
spack unload
```
As Spack is building GCC and all of the dependency packages this install can take a long time (>30 mins).

## Arm Compiler for Linux

The Arm Compiler for Linux (ACfL) can be installed by Spack on Arm systems, like the Graviton2 (C6g) or Graviton3 (C7g).o
```bash
spack install arm@22.0.1
spack load arm@22.0.1
spack compiler find
spack unload
```

## Where to build softwares

The cluster has quite a small headnode, this means that the compilation of complex software is prohibited. One simple solution is to use the compute nodes to perform the Spack installations, by submitting the command through Slurm.
```bash
srun -N1 -c 36 spack install -j36 gcc@11.2.0+binutils
```

## AWS Environment

* The versions of these external packages may change and are included for reference.

* The Cluster comes pre-installed with [Slurm](https://slurm.schedmd.com/) , [libfabric](https://ofiwg.github.io/libfabric/) , [PMIx](https://pmix.github.io/standard) , [Intel MPI](https://www.intel.com/content/www/us/en/developer/tools/oneapi/mpi-library.html#gs.hvr8xx) , and [Open MPI](https://www.open-mpi.org/) . To use these packages, you need to tell spack where to find them.
```bash
cat << EOF > $SPACK_ROOT/etc/spack/packages.yaml
packages:
    libfabric:
        variants: fabrics=efa,tcp,udp,sockets,verbs,shm,mrail,rxd,rxm
        externals:
        - spec: libfabric@1.13.2 fabrics=efa,tcp,udp,sockets,verbs,shm,mrail,rxd,rxm
          prefix: /opt/amazon/efa
        buildable: False
    openmpi:
        variants: fabrics=ofi +legacylaunchers schedulers=slurm ^libfabric
        externals:
        - spec: openmpi@4.1.1 %gcc@7.3.1
          prefix: /opt/amazon/openmpi
    pmix:
        externals:
          - spec: pmix@3.2.3 ~pmi_backwards_compatibility
            prefix: /opt/pmix
    slurm:
        variants: +pmix sysconfdir=/opt/slurm/etc
        externals:
        - spec: slurm@21.08.8-2 +pmix sysconfdir=/opt/slurm/etc
          prefix: /opt/slurm
        buildable: False
    armpl:
        externals:
        - spec: armpl@21.0.0%gcc@9.3.0
          prefix: /opt/arm/armpl/21.0.0/armpl_21.0_gcc-9.3/
EOF
```

## Add the GCC 9.3 Compiler

The Graviton image ships with an additional compiler within the ArmPL project. We can add this compiler to the Spack environment with the following command: `spack compiler add /opt/arm/armpl/gcc/9.3.0/bin/`

## Open MPI

For Open MPI we have already made the definition to set libfabric as a dependency of Open MPI. So by default it will configure it correctly.
```bash
spack install openmpi%gcc@11.2.0
```


## Additional resources

* Job submission relies on the Slurm scheduler. Please refer to the following [page](../jobs/submit.md) for more details.
* [Spack tutorial on AWS ParallelCluster](https://catalog.us-east-1.prod.workshops.aws/workshops/dd0ffcb3-ffc1-4b58-8c4b-09f9846549c7/en-US)












