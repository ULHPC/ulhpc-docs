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
    srun -p interactive --pty bash
    ```


### Pulling container images

Like [Docker](https://www.docker.com/), Singularity provide a way to pull images from a Hubs such as [DockerHub](https://hub.docker.com/) and [Singuarity Hub](https://singularity-hub.org/). 

```shell

>$ singularity pull docker://ubuntu:latest

```
You should see the following output:


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
Please refer to the [Data transfer](data/transfer.md) section for this purpose.

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


### MPI and Singularity containers
This section relies on the very excellent documentation from [CSCS](https://user.cscs.ch/tools/containers/singularity/). The following singularity definition file mpi_osu.def can be used to build a container with the osu benchmarks using mpi: 


```shell
bootstrap: docker
from: debian:jessie

%post
    # Install software
    apt-get update
    apt-get install -y file g++ gcc gfortran make gdb strace realpath wget --no-install-recommends

    # Install mpich
    wget -q http://www.mpich.org/static/downloads/3.1.4/mpich-3.1.4.tar.gz
    tar xf mpich-3.1.4.tar.gz
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
#SBATCH -n 128
#SBATCH -c 1
#SBATCH --time=0-01:00:00
#SBATCH -p batch
#SBATCH --qos=qos-besteffort

# Multi-node parallel application OpenMPI launcher, using 128 distributed cores
module load tools/Singularity
srun -n $SLURM_NTASKS run singularity run mpi_osu.sif
```

