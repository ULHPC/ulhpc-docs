
# EESSI - European Environment for Scientific Software Installations

[<img width='400px' src='https://www.eessi.io/docs/img/logos/EESSI_logo_horizontal.jpg'/>](https://www.eessi.io/)

The [European Environment for Scientific Software Installations (EESSI, pronounced as "easy")](https://www.eessi.io/) is a collaboration between different European partners in HPC community.
The goal of this project is to build a common stack of scientific software installations for HPC systems and beyond, including laptops, personal workstations and cloud infrastructure.

The EESSI software stack is available on the ULHPC platform, and gives you access to software modules maintained by the EESSI project and optimized for the CPU architectures available on the ULHPC platform.

On a compute node, to set up the EESSI environment, simply load the EESSI [module](/environment/modules/):

```
module load EESSI
```

The first usage may be slow as the files are downloaded from an upstream Stratum 1 server, but the files are cached locally.

You should see the following output:

```
$ module load EESSI
EESSI/2023.06 loaded successfully
```

The last line is the shell output.

Your environment is now set up, you are ready to start running software provided by EESSI! To see which modules (and extensions) are available, run:

```
module avail
```

Here is a short excerpt of the output produced by module avail:

```
----- /cvmfs/software.eessi.io/versions/2023.06/software/linux/x86_64/amd/zen2/modules/all -----
   ALL/0.9.2-foss-2023a           ESPResSo/4.2.1-foss-2023a        foss/2023a            h5py/3.9.0-foss-2023a
   ParaView/5.11.2-foss-2023a     PyTorch/2.1.2-foss-2023a         QuantumESPRESSO/7.2-foss-2022b   VTK/9.3.0-foss-2023a
   ELPA/2022.05.001-foss-2022b    foss/2022b                       foss/2023b (D)        OpenFOAM/11-foss-2023a
...
```

For more precise information, please refer to the [official documentation](https://www.eessi.io/docs).
