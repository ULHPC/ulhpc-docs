### [LLVM](https://llvm.org/)

* [Official website](https://llvm.org/)
* __Category__: Compilers (compiler)
    -  `module load compiler/LLVM[/<version>]`

Available versions of [LLVM](https://llvm.org/) on ULHPC platforms:

|    | Version   | Swset   | Architectures                 | Clusters   |
|---:|:----------|:--------|:------------------------------|:-----------|
|  0 | 10.0.1    | 2020b   | broadwell, epyc, skylake, gpu | aion, iris |
|  1 | 11.0.0    | 2020b   | broadwell, epyc, skylake, gpu | aion, iris |
|  2 | 9.0.0     | 2019b   | broadwell, skylake, gpu       | iris       |
|  3 | 9.0.1     | 2019b   | broadwell, skylake, gpu       | iris       |

> The LLVM Core libraries provide a modern source- and target-independent optimizer, along with code generation support for many popular CPUs (as well as some less common ones!) These libraries are built around a well specified code representation known as the LLVM intermediate representation ("LLVM IR"). The LLVM Core libraries are well documented, and it is particularly easy to invent your own language (or port an existing compiler) to use LLVM as an optimizer and code generator.
