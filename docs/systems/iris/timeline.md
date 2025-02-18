# Iris Timeline

This page records a brief timeline of significant events and user environment changes on Iris.
The **Iris** cluster exists since the beginning of 2017 as the flagship HPC supercomputer within the [University of Luxembourg](http://www.uni.lu) until 2020 and the release of the [Aion](../aion/index.md) supercomputer.

## 2016

### September 2016

* Official Public release of Iris cluster tenders on TED European tender and Portail des Marchés Publiques (PMP)
    - __RFP 160019__: **High Performance Storage** System for the High Performance Computing Facility of the University of Luxembourg.
    - __RFP 160020__: **High Performance Computing Facility (incl. Interconnect)** for the University of Luxembourg.

### October 2016

* Bids Opening for both RFPs on October 12, 2016.
    - Starting offers analysis by the ULHPC team, together with the procurement and legal departments of the University

### November 2016

* Awarding notification to the vendors
    -  __RFP 160019__ attributed to the **Telindus/HPE/DDN** consortium to provide High Performance Storage solution of capacity **1.44 PB (raw)** (over `GPFS/SpectrumScale` Filesystem), with a **RW performance above 10GB/s**
    - __RFP 160020__ attributed to the **Post/DELL** consortium to provide a High Performance Computing (HPC) cluster of **effective** capacity **$R_\text{max}$ = 94.08 TFlops** (raw capacity $R_\text{peak}$ = 107.52 TFlops)

## 2017

### March-April 2017

Delivery and installation of the `iris` cluster composed of:

* `iris-[1-100]`, Dell PowerEdge C6320, 100 nodes, 2800 cores, 12.8 TB RAM
* 10/40GB Ethernet network, high-speed Infiniband EDR 100Gb/s interconnect
* SpectrumScale (GPFS) core storage, 1.44 PB
* Redundant / load-balanced services with:
    - 2x adminfront servers (cluster management)
    - 2x access servers (user frontend)

### May-June 2017

* End of cluster validation
* 8 new regular nodes added
    - `iris-[101-108]`, Dell PowerEdge C6320, 8 nodes, 224 cores, 1.024 TB RAM
* Official release of the `iris` cluster for production on **June 12, 2017** at the occasion of the UL HPC School 2017.

### October 2017

* Official Public release of Iris Lustre Storage acquisition tenders on TED European tender and Portail des Marchés Publiques (PMP)
    - __RFP 170035__: **Complementary Lustre High Performance Storage System** for the High Performance Computing Facility of the University of Luxembourg.

### November 2017

* Bids Opening for Lustre RFP on November 28, 2017.
    - Starting offers analysis by the ULHPC team, together with the procurement and legal departments of the University

### December 2017

* Awarding notification to the vendors
    - Lustre RFP 170035 attributed to the **Fujitsu/DDN** consortium to provide High Performance Storage solution of capacity **1.28 PB (raw)**
* 60 new regular nodes added yet based on Skylake processors
    - `iris-[109-168]`, Dell PowerEdge C6420, 60 nodes, 1680 cores, 7.68 TB RAM

## 2018

### February 2018

* `iris` cluster moved from CDC S-01 to CDC S-02

### April 2018

* SpectrumScale (GPFS) DDN GridScaler extension to reach 2284TB raw capacity
    - new expansion unit and provisioning of enough complementary disks to feed the system.
* Delivery and installation of the complementary Lustre storage, with 1280 TB raw capacity


### July 2018

* Official Public release of tenders on [TED European tender](https://ted.europa.eu/udl?uri=TED:NOTICE:328963-2018:TEXT:EN:HTML) and [Portail des Marchés Publiques](https://pmp.b2g.etat.lu/?page=entreprise.EntrepriseAdvancedSearch&searchAnnCons&keyWord=180027) (PMP)
    - __RFP 180027__: **Complementary Multi-GPU and Large-Memory Computer Nodes** for the High Performance Computing Facility of the University of Luxembourg.

### September 2018

* Bids Opening for Multi-GPU and Large-Memory nodes RFP on September 10, 2018.
    - Starting offers analysis by the ULHPC team, together with the procurement and legal departments of the University

### October 2018

* Awarding notification to the vendors
    - RFP 180027 attributed to the **Dimension Data/Dell** consortium

### Dec 2018

* New Multi-GPU and Bigmem compute nodes added
    - `iris-[169-186]`: Dell C4140, 18 GPU nodes x 4 Nvidia V100 SXM2 16GB, part of the `gpu` partition
    - `iris-[187-190]`: Dell R840, 4 Bigmem nodes 4x28c i.e. 112 cores per node, part of the `bigmem` partition

## 2019

### May 2019

* 6 new Multi-GPU nodes added
    - `iris-[191-196]`: Dell C4140, 6 GPU nodes x 4 Nvidia V100 SXM2 32GB, part of the `gpu` partition

### October 2019

* SpectrumScale (GPFS) extension to allow 1Bn files capacity
    - replacement of 2 data pools (HDD-based) with new metadata pools (SSD-based)
