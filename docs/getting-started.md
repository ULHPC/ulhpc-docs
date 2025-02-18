# Getting Started on ULHPC Facilities

![](images/logo_ULHPC.png){: style="width:150px; float: right;"}

Welcome to the [High Performance Computing (HPC)](https://hpc.uni.lu) Facility of the University of Luxembourg (ULHPC)!

!!! success ""
	This page will guide you through the basics of using ULHPC's
	supercomputers, storage systems, and services.

## What is ULHPC ?

HPC is crucial in academic environments to achieve high-quality results in all application areas.
All world-class universities require this type of facility to accelerate its research and ensure cutting-edge results in time to face the global competition.

??? info "What is High Performance Computing?"
    If you're new to all of this, this is probably the first question you have in mind. Here is a possible definition:

    "_High Performance Computing (HPC) most generally refers to the practice of aggregating computing power in a way that delivers much higher performance than one could get out of a typical desktop computer or workstation in order to solve large problems in science, engineering, or business._"

    Indeed, with the advent of the technological revolution and the digital transformation that made all scientific disciplines becoming computational nowadays, High-Performance Computing (HPC) is increasingly identified as a **strategic asset** and enabler to **accelerate** the research performed in all areas requiring intensive computing and large-scale Big Data analytic capabilities. Tasks which would typically require several years or centuries to be computed on a typical desktop computer may only require a couple of hours, days or weeks over an HPC system.

    For more details, you may want to refer to this [Inside HPC article](https://insidehpc.com/hpc-basic-training/what-is-hpc/).


Since 2007, the [University of Luxembourg](https://www.uni.lu) (UL) has invested tens of millions of euros into its own HPC facilities to responds to the growing needs for increased computing and storage.
[ULHPC](https://hpc.uni.lu) (sometimes referred to as Uni.lu HPC) is the entity  providing High Performance Computing and Big Data Storage services and support for UL researchers and its external partners.

The University manages several research computing facilities located on the [Belval campus](https://wwwen.uni.lu/contact/campus_de_belval), offering a **cutting-edge research infrastructure to Luxembourg public research** while serving as _edge_ access to bigger systems from PRACE or EuroHPC, such as the Euro-HPC Luxembourg supercomputer "[MeluXina](https://luxprovide.lu)".

!!! warning
    In particular, the [ULHPC](https://hpc.uni.lu) is **NOT** the national HPC center of Luxembourg, but simply one of its strategic partner operating the second largest HPC facility of the country.

The HPC facility is one element of the extensive digital research infrastructure and expertise developed by the University over the last years. It also supports the University’s ambitious digital strategy and in particular the creation of a Facility for Data and HPC Sciences. This facility aims to provide a world-class user-driven digital infrastructure and services for fostering the development of collaborative activities related to frontier research and teaching in the fields of Computational and Data Sciences, including High Performance Computing, Data Analytics, Big Data Applications, Artificial Intelligence and Machine Learning.

!!! important "Reference ULHPC Article to cite"
    If you want to get a good overview of the way our facility is setup, managed and evaluated, you can refer to the [reference article](https://orbilu.uni.lu/handle/10993/51857) you are in all cases entitled to refer to when crediting the ULHPC facility as per [AUP](https://hpc-docs.uni.lu/policies/aup/).
    > __ACM Reference Format__ | [ORBilu entry](https://orbilu.uni.lu/handle/10993/51857) | [slides](https://hpc-docs.uni.lu/system/2022-07-10-ACM-HPCCT22.pdf) :<br/>
    > Sebastien Varrette, Hyacinthe Cartiaux, Sarah Peter, Emmanuel Kieffer, Teddy Valette, and Abatcha Olloh. 2022. Management of an Academic HPC & Research Computing Facility: The ULHPC Experience 2.0. In 6th High Performance Computing and Cluster Technologies Conference (HPCCT 2022), July 08-10, 2022, Fuzhou, China. ACM, New York, NY, USA, 14 pages.
    > https://doi.org/10.1145/3560442.3560445


--------------------------------------------------------
## Supercomputing and Storage Resources at a glance


[ULHPC](https://hpc.uni.lu) is a strategic asset of the university and an important factor for the scientific and therefore also economic competitiveness of the Grand Duchy of Luxembourg.
We provide a key research infrastructure featuring state-of-the-art computing and storage resources serving the UL HPC community primarily composed by UL researchers.

The UL HPC platform has kept growing over time thanks to the continuous efforts of the core HPC / Digital Platform team - contact: [hpc-team@uni.lu](mailto:hpc-team@uni.lu), recently completed with the [EuroHPC Competence Center](https://www.eurocc-project.eu/) Task force (A. Vandeventer (Project Manager), L. Koutsantonis).

!!! info "ULHPC Computing and Storage Capacity (2022)"
    Installed in the premises of the University’s _Centre de Calcul_ (CDC), the UL HPC facilities provides a total computing capacity of __2.76 PetaFlops__ and a shared storage capacity of around **10 PetaBytes**.

??? question "How big is 1 PetaFlops? 1 PetaByte?"
    * 1 PetaFlops = 10<sup>15</sup> floating-point operations per second (PFlops or PF for short), corresponds to the cumulative performance of more than 3510 Macbook Pro 13" laptops [^1], or 7420 iPhone XS [^2]
    * 1 PetaByte = 10<sup>15</sup> bytes = 8*10<sup>15</sup> bits, corresponding to the cumulative raw capacity of more than 1950 SSDs 512GB.

![](images/plots/plot_piechart_compute_cluster.png){: style="width:325px;"}
![](images/plots/plot_piechart_storage_fs.png){: style="width:325px;"}

This places the HPC center of the University of Luxembourg as one of the major actors in HPC and Big Data for the Greater Region Saar-Lor-Lux.

In practice, the UL HPC Facility features 3 types of computing resources:

* "__regular__" nodes: Dual CPU, no accelerators, 128 to 256 GB of RAM
* "__gpu__" nodes:     Dual CPU, 4 Nvidia accelerators, 768 GB RAM
* "__bigmem__" nodes:  Quad-CPU, no accelerators, 3072 GB RAM

These resources can be reserved and allocated for the execution of jobs scheduled on the platform thanks to a Resource and Job Management Systems (RJMS) - [Slurm](https://slurm.schedmd.com/documentation.html) in practice. This tool allows for a fine-grain analysis and accounting of the used resources, facilitating the generation of activity reports for a given time period.


[^1]: The best MacBook Pro 13" in 2020 is equiped with Ice Lake 2 GHz Intel Quad-Core i5 processors with an estimated computing performance of 284.3 Gflops as measured by the [Geekbench 4 multi-core benchmarks platform, with SGEMM](https://browser.geekbench.com/v4/cpu/15611876)


[^2]: Apple A12 Bionic, the 64-bit ARM-based system on a chip (SoC) proposed on the iPhone XS has an estimated performance of 134.7 GFlops as measured by the [Geekbench 4 multi-core benchmarks platform, with SGEMM](https://browser.geekbench.com/v4/cpu/15612041)

### Iris

[`iris`](systems/iris/index.md), in production since June 2017, is a Dell/Intel supercomputer with a theoretical peak performance of **1082 TFlop/s**, featuring 196 computing nodes (totalling 5824 computing cores) and 96 GPU accelerators (NVidia V100).

[:fontawesome-solid-sign-in-alt: Iris Detailed system specifications](systems/iris/index.md){: .md-button .md-button--link }

### Aion

[`aion`](systems/aion/index.md), in production since October 2020, is a [Bull Sequana XH2000](https://atos.net/en/solutions/high-performance-computing-hpc/bullsequana-x-supercomputers)/AMD supercomputer offering a peak performance of **1692 TFlop/s**, featuring 318 compute nodes (totalling 40704 computing cores).

[:fontawesome-solid-sign-in-alt: Aion Detailed system specifications](systems/aion/index.md){: .md-button .md-button--link }


### GPFS/SpectrumScale File System (`$HOME`, project)

[IBM Spectrum Scale](https://www.ibm.com/products/scale-out-file-and-object-storage), formerly known as the General Parallel File System (GPFS), is global _high_-performance clustered file system available on all ULHPC computational systems. It is deployed over Dell-based storage hardware.

It allows sharing **homedirs and project data** between users, systems, and eventually (i.e. if needed) with the "outside world".

[:fontawesome-solid-sign-in-alt: GPFS/Spectrumscale Detailed specifications](filesystems/gpfs.md){: .md-button .md-button--link }

### Lustre File System (`$SCRATCH`)

The [Lustre](http://lustre.org/) file system is an open-source, parallel file system that supports many requirements of leadership class HPC simulation environments. It is available as a global _high_-performance file system on all ULHPC computational systems through a [DDN ExaScaler](https://www.ddn.com/products/lustre-file-system-exascaler/)
and is meant to host **temporary scratch data**.

[:fontawesome-solid-sign-in-alt: Lustre Detailed specifications](filesystems/lustre.md){: .md-button .md-button--link }

### OneFS File System (project, backup, archival)

In 2014, the SIU, the UL HPC and the LCSB join their forces (and their funding) to acquire a scalable and modular NAS solution able to sustain the need for an internal big data storage, i.e. provides space for centralized data and backups of all devices used by the UL staff and all research-related data, including the one proceed on the UL HPC platform.
A global _low_-performance [Dell/EMC Isilon](https://www.dellemc.com/en-us/collaterals/unauth/data-sheets/products/storage/h10717-isilon-onefs-ds.pdf) system is available on all ULHPC computational systems. It is intended for long term storage of data that is not frequently accessed. For more details, see [Isilon specifications](filesystems/isilon.md).


### Fast Infiniband Network

High Performance Computing (HPC) encompasses advanced computation over parallel processing, enabling faster execution of highly compute intensive tasks. The execution time of a given simulation depends upon many factors, such as the number of CPU/GPU cores and their utilisation factor and the interconnect performance, efficiency, and scalability.
[InfiniBand](https://en.wikipedia.org/wiki/InfiniBand) is the fast interconnect technology implemented within all [ULHPC supercomputers](interconnect/ib.md), more specifically:

* [Iris](systems/iris/interconnect.md) relies on a **EDR** Infiniband (IB) Fabric in a **Fat-Tree** Topology
* [Aion](systems/iris/interconnect.md) relies on a **HDR100** Infiniband (IB) Fabric in a **Fat-Tree** Topology

For more details, see [ULHPC IB Network Detailed specifications](interconnect/ib.md).


## Acceptable Use Policy (AUP)

{%
   include-markdown "policies/aup.md"
   start="<!--intro-start-->"
   end="<!--intro-end-->"
%}

## ULHPC Accounts

In order to use the ULHPC facilities, you need to have a user account with an associated user login name (also called username) placed under an account hierarchy.

* [Get a ULHPC account](accounts/index.md)
* [Understanding Slurm account hierarchy and accounting rules](slurm/accounts.md)
* [ULHPC Identity Management (IPA portal)](connect/ipa.md)
* [Password policy](policies/passwords.md)
* [Usage Charging Policy](policies/usage-charging.md)

## Connecting to ULHPC supercomputers

!!! check "MFA is *strongly encouraged* for all ULHPC users"
    It will be soon become mandatory - detailed instructions will be provided soon.

<!-- * [Multi-Factor Authentication (MFA)](connect/mfa.md)-->

* [SSH](connect/ssh.md)
* [Open On Demand Portal](connect/ood.md)
* [ULHPC Login/Access servers](connect/access.md)
* [Troubleshooting connection problems](connect/troubleshooting.md)


## Data Management

* [Global Directory Structure](data/layout.md)
* [Transferring data](data/transfer.md): Tools and recommendations to transfer data both inside and outside
of ULHPC.
* [Quotas](filesystems/quotas.md)
* Understanding [Unix File Permissions](filesystems/unix-file-permissions.md)


## User Environment

!!! info
	`$HOME`, Project and `$SCRATCH` directories are shared
	across all ULHPC systems, meaning that

    * every file/directory pushed or created on the front-end is available on the computing nodes
    * every file/directory pushed or created on the computing nodes is available on the front-end

[:fontawesome-solid-sign-in-alt: ULHPC User Environment](environment/index.md){: .md-button .md-button--link }

<!-- * [Understanding and customizing your environment](environment/index.md) -->
<!-- * [ULHPC Modules Environment](environment/modules.md) -->
<!-- * [ULHPC Easybuild Configuration](environment/easybuild.md) -->

<!-- ### User Software Management -->

## Computing Software Environment

The ULHPC Team supplies a large variety of HPC utilities, scientific applications and programming libraries to its user community.
The user software environment is generated using [Easybuild](https://easybuild.readthedocs.io) (EB) and is made available as environment modules through [LMod](https://lmod.readthedocs.io/). <!-- We have developped a specific tool named [RESIF](software/resif.md) -->

* [ULHPC Modules Environment](environment/modules.md)
* [ULHPC Supported Software List](./software/index.md).
    - Available [modules](./environment/modules.md) are reachable **from the compute nodes only** via `module avail`
* [ULHPC Easybuild Configuration](environment/easybuild.md)

<!-- * [RESIF Architecture-at-a-glance](software/resif.md) -->
<!-- * [Software Sets, compilers and toolchains at ULHPC](software/swsets.md) -->
<!-- * [Compiling/building software](development/software/index.md) -->
<!--     - [Building missing software with Easybuild](development/software/easybuild.md) -->
* [Running Containers](containers/index.md)
<!-- * [Contributing to the ULHPC User Software](development/software/contributing.md) -->

!!! question "Software building support"
	If you need help to build / develop software, we encourage you to first try using [Easybuild](environment/easybuild.md) as a recipe probably exist for the software you consider.
    You can then open a ticket on [HPC Help Desk Portal](support/index.md#help-desk) and we will evaluate the cost and effort required.
    You may also ask the help of other ULHPC users using the HPC User community mailing list: (moderated): [`hpc-users@uni.lu](mailto:hpc-users 'at' uni.lu).

## Running Jobs

Typical usage of the ULHPC supercomputers involves the reservation and allocation of computing resources for the execution of jobs (submitted via _launcher scripts_) and scheduled on the platform thanks to a Resource and Job Management Systems (RJMS) - [Slurm](https://slurm.schedmd.com/documentation.html) in our case.

[:fontawesome-solid-sign-in-alt: Slurm on ULHPC clusters](slurm/index.md){: .md-button .md-button--link }
[:fontawesome-solid-sign-in-alt: Convenient Slurm Commands](slurm/commands.md){: .md-button .md-button--link }

* [Rich set of launcher scripts examples](slurm/launchers.md)
* [Fairshare](slurm/fairsharing.md)
* [Job Priority and Backfilling](jobs/priority.md)
* [Job Accounting and Billing](jobs/billing.md)


## Interactive Computing

ULHPC also supports interactive computing.

* [Interactive jobs](jobs/interactive.md)
* [Jupyter Notebook](services/jupyter.md)
<!-- * [Interactive Big Data Analytics with Spark](bigdata/spark.md) -->


## Getting Help

ULHPC places a very strong emphasis on enabling science and providing
user-oriented systems and services.



### Documentation

We have always maintained an extensive [documentation](https://hpc-docs.uni.lu) and [HPC tutorials](https://ulhpc-tutorials.readthedocs.io) available online, which aims at being the most up-to-date and comprehensive while covering many (many) topics.

[:fontawesome-solid-sign-in-alt: ULHPC Technical Documentation](https://hpc-docs.uni.lu/support){: .md-button .md-button--link }
[:fontawesome-solid-chalkboard-teacher: ULHPC Tutorials](ttps://ulhpc-tutorials.readthedocs.io/){: .md-button .md-button--link }

!!! tip "The ULHPC Team welcomes your contributions"
	These pages are hosted from a [git repository](https://github.com/ULHPC/ulhpc-docs) and [contributions](contributing/)
	are welcome!
	[Fork this repo](https://docs.github.com/en/get-started/quickstart/fork-a-repo)

### Support

[:fontawesome-solid-sign-in-alt: ULHPC Support Overview](support/index.md){: .md-button .md-button--link }
[:fontawesome-solid-hand-holding-medical: Service Now HPC Support Portal](https://hpc.uni.lu/support){: .md-button .md-button--link }

!!! info "Availability and Response Time"
    HPC support is provided on a volunteer basis by UL HPC staff and associated UL experts working at normal business hours. We offer **no guarantee** on response time except with paid support contracts.

