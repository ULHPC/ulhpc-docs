### [libunwind](https://www.nongnu.org/libunwind/)

* [Official website](https://www.nongnu.org/libunwind/)
* __Category__: Libraries (lib)
    -  `module load lib/libunwind[/<version>]`

Available versions of [libunwind](https://www.nongnu.org/libunwind/) on ULHPC platforms:

|    | Version   | Swset   | Architectures                 | Clusters   |
|---:|:----------|:--------|:------------------------------|:-----------|
|  0 | 1.3.1     | 2019b   | broadwell, skylake, gpu       | iris       |
|  1 | 1.4.0     | 2020b   | broadwell, epyc, skylake, gpu | aion, iris |

> The primary goal of libunwind is to define a portable and efficient C programming interface (API) to determine the call-chain of a program. The API additionally provides the means to manipulate the preserved (callee-saved) state of each call-frame and to resume execution at any point in the call-chain (non-local goto). The API supports both local (same-process) and remote (across-process) operation. As such, the API is useful in a number of applications
