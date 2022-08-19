### [GObject-Introspection](https://gi.readthedocs.io/en/latest/)

* [Official website](https://gi.readthedocs.io/en/latest/)
* __Category__: Development (devel)
    -  `module load devel/GObject-Introspection[/<version>]`

Available versions of [GObject-Introspection](https://gi.readthedocs.io/en/latest/) on ULHPC platforms:

|    | Version   | Swset   | Architectures            | Clusters   |
|---:|:----------|:--------|:-------------------------|:-----------|
|  0 | 1.63.1    | 2019b   | broadwell, skylake       | iris       |
|  1 | 1.66.1    | 2020b   | broadwell, epyc, skylake | aion, iris |

> GObject introspection is a middleware layer between C libraries (using GObject) and language bindings. The C library can be scanned at compile time and generate a metadata file, in addition to the actual native C library. Then at runtime, language bindings can read this metadata and automatically provide bindings to call into the C library.
