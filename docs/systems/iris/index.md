# Iris Overview

Iris is a [Dell](https://www.delltechnologies.com/lb-lu/solutions/high-performance-computing/index.htm)/Intel supercomputer which consists of **196 compute nodes, totaling 5824 compute cores** and 52224 GB RAM,
with a peak performance of about **1,072 PetaFLOP/s**.

All nodes are interconnected through a **fully non-blocking [Fat-Tree](https://clusterdesign.org/fat-trees/) InfiniBand EDR network**[^1], and are equipped with **Intel** [Broadwell](https://en.wikipedia.org/wiki/Broadwell_(microarchitecture)) or [Skylake](https://en.wikipedia.org/wiki/Skylake_(microarchitecture))  processors.
Several nodes are equipped with 4 [Nvidia Tesla V100](https://www.nvidia.com/en-us/data-center/v100/) SXM2 GPU accelerators.
In total, Iris features **96 Nvidia V100** GPU-AI accelerators allowing for high speedup of GPU-enabled applications and AI/Deep Learning-oriented workflows.
Finally,  a few large-memory (fat) computing nodes offer multiple high-core density CPUs and a large live memory capacity of 3 TB RAM/node,  meant for in-memory processing of huge data sets.

Two global [_high_-performance clustered file systems](../../filesystems/index.md) are available on all ULHPC computational systems: one based on GPFS/SpectrumScale, one on Lustre.

[:fontawesome-solid-sign-in-alt: Iris Hardware Overview](compute.md){: .md-button .md-button--link } [:fontawesome-solid-sign-in-alt: Iris Interconnect](interconnect.md){: .md-button .md-button--link } [:fontawesome-solid-sign-in-alt: ULHPC Storage](../../filesystems/index.md){: .md-button .md-button--link }

The cluster runs a [Red Hat Linux Family](https://en.wikipedia.org/wiki/Red_Hat_Enterprise_Linux_derivatives) operating system.
The ULHPC Team supplies on all clusters a large variety of HPC utilities, scientific applications and programming libraries to its user community.
The [user software environment](../../software/index.md) is generated using [Easybuild](https://easybuild.readthedocs.io) (EB) and is made available as [environment modules](../../environment/modules.md) from the compute nodes only.

[Slurm](https://slurm.schedmd.com/documentation.html) is the Resource and Job Management Systems (RJMS) which provides computing resources allocations and job execution.<br/>
For more information: see [ULHPC slurm documentation](../../slurm/index.md).

[![](images/iris_cluster_overview.png)](images/iris_cluster_overview.pdf)



[^1]: Infiniband (IB) EDR networks offer a 100 Gb/s throughput with a very low latency (0,6$\mu$s).
