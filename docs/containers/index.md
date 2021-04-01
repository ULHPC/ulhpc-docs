# Containers

Many applications and libraries can also be used through container systems, with the updated Singularity tool providing many new features of which we can especially highlight support for Open Containers Initiative - OCI containers (including Docker OCI), and support for secure containers - building and running encrypted containers with RSA keys and passphrases.


## Singularity


![](https://sylabs.io/guides/3.0/admin-guide/_static/logo.png){: style="width:200px;float: right;"}



The ULHPC offers the possibilty to run [Singularity containers](https://sylabs.io/singularity/). Singularity is an open source container platform designed to be simple, fast, and secure. Singularity is optimized for EPC and HPC workloads, allowing untrusted users to run untrusted containers in a trusted way.



### Loading Singularity

To use Singularity, you need to load the corresponding [Lmod](https://lmod.readthedocs.io/en/latest/) module.


```shell
>$ module load tools/Singularity
```

!!! warning
    Modules are not allowed on the access servers. To test interactively Singularity, rememerber to ask for an interactive job first.
    ```shell
    salloc -p interactive --pty bash
    ```


### Pulling container images

Like [Docker](https://www.docker.com/), Singularity provide a way to pull images from a Hubs such as [DockerHub](https://hub.docker.com/) and [Singuarity Hub](https://singularity-hub.org/).

```shell

>$ singularity pull docker://ubuntu:latest

```
You should see the following output:

!!! note "Output"
    <pre><font color="#3465A4">INFO:   </font> Converting OCI blobs to SIF format
    <font color="#3465A4">INFO:   </font> Starting build...</pre>
    <pre>Getting image source signatures
    Copying blob d72e567cc804 done
    Copying blob 0f3630e5ff08 done
    Copying blob b6a83d81d1f4 done
    Copying config bbea2a0436 done
    Writing manifest to image destination
    Storing signatures
    ...
    <font color="#3465A4">INFO:   </font> Creating SIF file...
    </pre>

You may now test the container by executing some inner commands:

```shell
>$ singularity exec ubuntu_latest.sif cat /etc/os-release

```

!!! note "Output"
    <pre>NAME=&quot;Ubuntu&quot;
    VERSION=&quot;20.04.1 LTS (Focal Fossa)&quot;
    ID=ubuntu
    ID_LIKE=debian
    PRETTY_NAME=&quot;Ubuntu 20.04.1 LTS&quot;
    VERSION_ID=&quot;20.04&quot;
    HOME_URL=&quot;https://www.ubuntu.com/&quot;
    SUPPORT_URL=&quot;https://help.ubuntu.com/&quot;
    BUG_REPORT_URL=&quot;https://bugs.launchpad.net/ubuntu/&quot;
    PRIVACY_POLICY_URL=&quot;https://www.ubuntu.com/legal/terms-and-policies/privacy-policy&quot;
    VERSION_CODENAME=focal
    UBUNTU_CODENAME=focal
    </pre>


### Building container images

Building container images requires to have root privileges. Therefore, users have to build images on their local machine before transfering them to the platform.
Please refer to the [Data transfer](../data/transfer.md) section for this purpose.

!!! note
    Singularity 3 introduces the ability to build your containers in the cloud, so you can easily and securely create containers for your applications without speci    al privileges or setup on your local system. The Remote Builder can securely build a container for you from a definition file entered here or via the Singularity CLI (see https://cloud.sylabs.io/builder for more details).

### GPU-enabled Singularity containers

This section relies on the very excellent documentation from [CSCS](https://user.cscs.ch/tools/containers/singularity/). In the following example, a container with CUDA features is build, transfered and tested on the ULHPC platform. This example will pull a CUDA container from DockrHub and setup [CUDA examples](https://github.com/NVIDIA/cuda-samples.git). For this purpose, a singularity definition file, i.e., `cuda_samples.def`  needs to be created with the following content:

```shell
Bootstrap: docker
From: nvidia/cuda:10.1-devel

%post
    apt-get update
    apt-get install -y git
    git clone https://github.com/NVIDIA/cuda-samples.git /usr/local/cuda_samples
    cd /usr/local/cuda_samples
    git fetch origin --tags
    git checkout 10.1.1
    make

%runscript
    /usr/local/cuda_samples/Samples/deviceQuery/deviceQuery

```

On a local machine having singularity installed, we can build the container image, i.e., `cuda_samples.sif` using the definition file using the follwing singularity command:

```shell
sudo singularity build cuda_samples.sif cuda_samples.def

```

!!! warning
    You should have root privileges on this machine. Without this condition, you will not be able to built the definition file.


Once the container is built and transfered to your dedicated storage on the ULHPC plaform, the container can be executed with the following command:


```shell
# Inside an interactive job on a gpu-enabled node
singularity run --nv cuda_samples.sif
```

!!! warning
    In order to run a CUDA-enabled container, the --nv option has to be passed to singularity run. According to this option, singularity is going to setup the container environment to use the NVIDIA GPU and the basic CUDA libraries.


The lastest command should print:
!!! note "Output"
    <pre>CUDA Device Query (Runtime API) version (CUDART static linking)

    Detected 1 CUDA Capable device(s)

    Device 0: &quot;Tesla V100-SXM2-16GB&quot;
      CUDA Driver Version / Runtime Version          10.2 / 10.1
      CUDA Capability Major/Minor version number:    7.0
      Total amount of global memory:                 16160 MBytes (16945512448 bytes)
      (80) Multiprocessors, ( 64) CUDA Cores/MP:     5120 CUDA Cores
      GPU Max Clock rate:                            1530 MHz (1.53 GHz)
      Memory Clock rate:                             877 Mhz
      Memory Bus Width:                              4096-bit
      L2 Cache Size:                                 6291456 bytes
      Maximum Texture Dimension Size (x,y,z)         1D=(131072), 2D=(131072, 65536), 3D=(16384, 16384, 16384)
      Maximum Layered 1D Texture Size, (num) layers  1D=(32768), 2048 layers
      Maximum Layered 2D Texture Size, (num) layers  2D=(32768, 32768), 2048 layers
      Total amount of constant memory:               65536 bytes
      Total amount of shared memory per block:       49152 bytes
      Total number of registers available per block: 65536
      Warp size:                                     32
      Maximum number of threads per multiprocessor:  2048
      Maximum number of threads per block:           1024
      Max dimension size of a thread block (x,y,z): (1024, 1024, 64)
      Max dimension size of a grid size    (x,y,z): (2147483647, 65535, 65535)
      Maximum memory pitch:                          2147483647 bytes
      Texture alignment:                             512 bytes
      Concurrent copy and kernel execution:          Yes with 5 copy engine(s)
      Run time limit on kernels:                     No
      Integrated GPU sharing Host Memory:            No
      Support host page-locked memory mapping:       Yes
      Alignment requirement for Surfaces:            Yes
      Device has ECC support:                        Enabled
      Device supports Unified Addressing (UVA):      Yes
      Device supports Compute Preemption:            Yes
      Supports Cooperative Kernel Launch:            Yes
      Supports MultiDevice Co-op Kernel Launch:      Yes
      Device PCI Domain ID / Bus ID / location ID:   0 / 30 / 0
      Compute Mode:
         &lt; Default (multiple host threads can use ::cudaSetDevice() with device simultaneously) &gt;

    deviceQuery, CUDA Driver = CUDART, CUDA Driver Version = 10.2, CUDA Runtime Version = 10.1, NumDevs = 1
    Result = PASS
    </pre>


### MPI and Singularity containers
This section relies on the very excellent documentation from [CSCS](https://user.cscs.ch/tools/containers/singularity/). The following singularity definition file mpi_osu.def can be used to build a container with the osu benchmarks using mpi:


```shell
bootstrap: docker
from: debian:jessie

%post
    # Install software
    apt-get update
    apt-get install -y file g++ gcc gfortran make gdb strace realpath wget curl --no-install-recommends

    # Install mpich
    curl -kO https://www.mpich.org/static/downloads/3.1.4/mpich-3.1.4.tar.gz
    tar -zxvf mpich-3.1.4.tar.gz
    cd mpich-3.1.4
    ./configure --disable-fortran --enable-fast=all,O3 --prefix=/usr
    make -j$(nproc)
    make install
    ldconfig

    # Build osu benchmarks
    wget -q http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-5.3.2.tar.gz
    tar xf osu-micro-benchmarks-5.3.2.tar.gz
    cd osu-micro-benchmarks-5.3.2
    ./configure --prefix=/usr/local CC=$(which mpicc) CFLAGS=-O3
    make
    make install
    cd ..
    rm -rf osu-micro-benchmarks-5.3.2
    rm osu-micro-benchmarks-5.3.2.tar.gz

%runscript
    /usr/local/libexec/osu-micro-benchmarks/mpi/pt2pt/osu_bw
```
```shell
sudo singularity build mpi_osu.sif mpi_osu.def
```
Once the container image is ready, you can use it for example inside the following slurm launcher to start a best-effort job:

```slurm
#!/bin/bash -l
#SBATCH -J ParallelJob
#SBATCH -N 2
#SBATCH --ntasks-per-node=1
#SBATCH --time=05:00
#SBATCH -p batch
#SBATCH --qos=qos-besteffort

module load tools/Singularity
srun -n $SLURM_NTASKS singularity run mpi_osu.sif
```
The content of the output file:

!!! note "Output"
    <pre>
    \# OSU MPI Bandwidth Test v5.3.2
    \# Size      Bandwidth (MB/s)
    1                       0.35
    2                       0.78
    4                       1.70
    8                       3.66
    16                      7.68
    32                     16.38
    64                     32.86
    128                    66.61
    256                    80.12
    512                    97.68
    1024                  151.57
    2048                  274.60
    4096                  408.71
    8192                  456.51
    16384                 565.84
    32768                 582.62
    65536                 587.17
    131072                630.64
    262144                656.45
    524288                682.37
    1048576               712.19
    2097152               714.55
    </pre>
