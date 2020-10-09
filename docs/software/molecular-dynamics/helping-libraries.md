## libctl
This is [libctl](https://github.com/NanoComp/libctl), a Guile-based library
for supporting flexible control files in scientific simulations.
For more information about libctl, please refer https://libctl.readthedocs.io/en/latest/

### Availble versions of libctl in UL-HPC:
```bash
chem/libctl/3.2.2-intel-2017a
chem/libctl/4.0.0-intel-2018a
chem/libctl/4.0.0-intel-2019a
```

## Libint
Libint library is used to evaluate the traditional (electron repulsion) and
certain novel two-body matrix elements (integrals) over Cartesian
Gaussian functions used in modern atomic and molecular theory.

### Availble versions of Libint in UL-HPC:
```bash
chem/Libint/1.1.6-GCC-8.2.0-2.31.1
chem/Libint/1.2.1-intel-2018a
```

## Libxc
[Libxc](https://tddft.org/programs/libxc/) is a library of exchange-correlation functionals for density-functional theory.
The aim is to provide a portable, well tested and reliable set of exchange and
correlation functionals that can be used by all the ETSF codes and also other codes.

### Availble versions of Libxc in UL-HPC:
```bash
chem/libxc/3.0.0-intel-2017a
chem/libxc/3.0.1-intel-2018a
chem/libxc/4.2.3-intel-2019a
chem/libxc/4.3.4-GCC-8.2.0-2.31.1
chem/libxc/4.3.4-iccifort-2019.1.144-GCC-8.2.0-2.31.1
```

## PLUMED
[PLUMED](https://www.plumed.org/) works together with some of the most popular MD engines,
such as ACEMD, Amber, DL_POLY, GROMACS, LAMMPS, NAMD, OpenMM, DFTB+, ABIN, CP2K, i-PI, PINY-MD,
and Quantum Espresso. In addition, PLUMED can be used to augment the capabilities of
analysis tools such as VMD, HTMD, OpenPathSampling, and as a
standalone utility to analyze pre-calculated MD trajectories.

PLUMED can be interfaced with the host code using a single
well-documented API that enables the PLUMED functionalities to be imported.
The API is accessible from multiple languages (C, C++, FORTRAN, and Python),
and is thus compatible with the majority of the codes used in the community.
The PLUMED license (L-GPL) also allows it to be interfaced with proprietary software.

### Availble versions of PLUMED in UL-HPC:
```bash
chem/PLUMED/2.4.2-intel-2018a
chem/PLUMED/2.5.1-foss-2019a
chem/PLUMED/2.5.1-intel-2019a
```
For more information about tutorial and documention about PLUMED, please
refer https://www.plumed.org/doc-v2.6/user-doc/html/cambridge.html

## ESPResSo
[ESPResSo](http://espressomd.org/wordpress/) is a highly versatile software package for performing and analyzing
scientific Molecular Dynamics many-particle simulations of coarse-grained
atomistic or bead-spring models as they are used in soft matter research in physics,
chemistry and molecular biology. It can be used to simulate systems such as polymers,
liquid crystals, colloids, polyelectrolytes, ferrofluids and biological systems,
for example DNA and lipid membranes. It also has a DPD and lattice Boltzmann
solver for hydrodynamic interactions, and allows several particle couplings to the LB fluid.

ESPResSo is free, open-source software published under the GNU General Public License (GPL3).
It is parallelized and can be employed on desktop machines, convenience clusters as well as on
supercomputers with hundreds of CPUs, and some modules have also support for GPU acceleration.
The parallel code is controlled via the scripting language Python,
which gives the software its great flexibility.

### Availble versions of ESPResSo in UL-HPC:
```bash
phys/ESPResSo/3.3.1-intel-2017a-parallel
phys/ESPResSo/3.3.1-intel-2018a-parallel
phys/ESPResSo/4.0.2-intel-2019a
phys/ESPResSo/4.0.2-intelcuda-2019a
```
For more information about tutorial and documention about ESPResSo, please
refer http://espressomd.org/wordpress/documentation/

## UDUNITS
The [UDUNITS](https://www.unidata.ucar.edu/software/udunits/) package supports
units of physical quantities. Its C library provides for arithmetic
manipulation of units and for conversion of numeric values between
compatible units. The package contains an extensive unit database,
which is in XML format and user-extendable. The package also contains a
command-line utility for investigating units and converting values.

### Availble versions of UDUNITS in UL-HPC:
```bash
phys/UDUNITS/2.2.26-GCCcore-8.2.0
```
For more information about tutorial and documention about UDUNITS, please
refer https://www.unidata.ucar.edu/software/udunits/udunits-current/doc/udunits/udunits2.html

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).  