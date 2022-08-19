### [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/)

* [Official website](https://www.freedesktop.org/wiki/Software/pkg-config/)
* __Category__: Development (devel)
    -  `module load devel/pkg-config[/<version>]`

Available versions of [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/) on ULHPC platforms:

|    | Version   | Swset   | Architectures           | Clusters   |
|---:|:----------|:--------|:------------------------|:-----------|
|  0 | 0.29.2    | 2019b   | broadwell, skylake, gpu | iris       |
|  1 | 0.29.2    | 2020b   | broadwell, skylake, gpu | iris       |

> pkg-config is a helper tool used when compiling applications and libraries. It helps you insert the correct compiler options on the command line so an application can use gcc -o test test.c `pkg-config --libs --cflags glib-2.0` for instance, rather than hard-coding values on where to find glib (or other libraries).
