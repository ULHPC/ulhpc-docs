### [numactl](https://github.com/numactl/numactl)

* [Official website](https://github.com/numactl/numactl)
* __Category__: Utilities (tools)
    -  `module load tools/numactl[/<version>]`

Available versions of [numactl](https://github.com/numactl/numactl) on ULHPC platforms:

|    | Version   | Swset   | Architectures                 | Clusters   |
|---:|:----------|:--------|:------------------------------|:-----------|
|  0 | 2.0.12    | 2019b   | broadwell, skylake, gpu       | iris       |
|  1 | 2.0.13    | 2020b   | broadwell, epyc, skylake, gpu | aion, iris |

> The numactl program allows you to run your application program on specific cpu's and memory nodes. It does this by supplying a NUMA memory policy to the operating system before running your program. The libnuma library provides convenient ways for you to add NUMA memory policies into your own program.
