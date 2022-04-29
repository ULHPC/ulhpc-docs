### [hwloc](https://www.open-mpi.org/projects/hwloc/)

* [Official website](https://www.open-mpi.org/projects/hwloc/)
* __Category__: System-level software (system)
    -  `module load system/hwloc[/<version>]`

Available versions of [hwloc](https://www.open-mpi.org/projects/hwloc/) on ULHPC platforms:

|    | Version   | Swset   | Architectures                 | Clusters   |
|---:|:----------|:--------|:------------------------------|:-----------|
|  0 | 1.11.12   | 2019b   | broadwell, skylake, gpu       | iris       |
|  1 | 2.2.0     | 2020b   | broadwell, epyc, skylake, gpu | aion, iris |

> The Portable Hardware Locality (hwloc) software package provides a portable abstraction (across OS, versions, architectures, ...) of the hierarchical topology of modern architectures, including NUMA memory nodes, sockets, shared caches, cores and simultaneous multithreading. It also gathers various system attributes such as cache and memory information as well as the locality of I/O devices such as network interfaces, InfiniBand HCAs or GPUs. It primarily aims at helping applications with gathering information about modern computing hardware so as to exploit it accordingly and efficiently.
