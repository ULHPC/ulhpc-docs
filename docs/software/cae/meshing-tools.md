# Meshing Tools

## Gmsh

![](https://gitlab.onelab.info/uploads/-/system/project/avatar/3/gmsh.png){: style="width:200px;float: right;" } [Gmsh](https://gmsh.info/) is an open source 3D finite element mesh generator with a built-in CAD engine and post-processor.
Its design goal is to provide a fast, light and user-friendly meshing tool with parametric
input and advanced visualization capabilities. Gmsh is built around four modules: geometry, mesh,
solver and post-processing. The specification of any input to these modules is done either
interactively using the graphical user interface, in ASCII text files using Gmsh's
own scripting language (.geo files), or using the C++, C, Python or Julia Application Programming Interface (API).

See this general [presentation](https://gmsh.info/doc/course/general_overview.pdf)
for a high-level overview of Gmsh and recent developments,
the screencasts for a quick tour of Gmsh's graphical user interface, and the [reference manual](https://gmsh.info/doc/texinfo/gmsh.html)
for a more thorough overview of Gmsh's capabilities, some [frequently
asked questions](https://gmsh.info/doc/texinfo/gmsh.html#Frequently-asked-questions) and the documentation of the C++, C, Python and Julia API.

The [source code repository](https://gitlab.onelab.info/gmsh/gmsh/) contains many examples written using both the
built-in script language and the API (see e.g. the tutorials and the and [demos](https://gitlab.onelab.info/gmsh/gmsh/tree/master/demos)).

### Available versions of Gmsh in ULHPC
To check available versions of Gmsh at ULHPC type `module spider gmsh`.
Below it shows list of available versions of Gmsh in ULHPC. 
```bash
cae/gmsh/4.3.0-intel-2018a
cae/gmsh/4.4.0-intel-2019a
```
### To work with Gmsh interactively on ULHPC:
```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11

# Load the module for Gmesh and neeed environment
$ module purge
$ module load swenv/default-env/v1.2-20191021-production
$ module load cae/gmsh/4.4.0-intel-2019a

$ gmsh example.geo
```
## Salome
[SALOME](https://www.salome-platform.org/) is an open-source software that provides a generic
Pre- and Post-Processing platform for numerical simulation.
It is based on an open and flexible architecture made of reusable components.

SALOME is a cross-platform solution. It is distributed under the terms of the GNU LGPL license.
You can download both the source code and the executables from this site.

To know more about salome documentation please refer https://www.salome-platform.org/user-section/salome-tutorials

### Available versions of SALOME in ULHPC
To check available versions of SALOME at ULHPC type `module spider salome`.
Below it shows list of available versions of SALOME in ULHPC.

```bash
cae/Salome/8.5.0-intel-2018a
cae/Salome/8.5.0-intel-2019a
```

### To work with SALOME interactively on ULHPC:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p batch --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the module Salome and needed environment
$ module purge
$ module load swenv/default-env/v1.2-20191021-production
$ module load cae/Salome/8.5.0-intel-2019a

$ salome start
```

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
