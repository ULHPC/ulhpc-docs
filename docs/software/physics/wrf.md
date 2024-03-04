# Weather Research and Forecasting

[Weather Research and Forecasting Model (WRF)](https://www2.mmm.ucar.edu/wrf/users/) is a state-of-the-art atmospheric modeling system designed for both meteorological research and numerical weather prediction. The official source code, models, usage instruction, and most importantly the user license, are found in the [official repository](https://github.com/wrf-model/WRF/).

## The University of Manchester distribution

In our systems we provide repackaged containers developed by the Central Research IT Service of the University of Manchester. The [repository for `wrf-docker`](https://github.com/UoMResearchIT/wrf-docker/) provides individual Docker containers for the following packages:

- [WRF-WPS (`wrf-wps`)](https://github.com/UoMResearchIT/wrf-docker/pkgs/container/wrf-wps/): provides the main WRF and WPS applications
- [WRF-Chem (`wrf-chem`)](https://github.com/UoMResearchIT/wrf-docker/pkgs/container/wrf-chem/): provides the WRF-Chem application
- [WRF-4DVar (`wrf-4dvar`)](https://github.com/UoMResearchIT/wrf-docker/pkgs/container/wrf-4dvar/): provides the WRFPLUS and WRF-4DVar extensions

## Available versions in the UL HPC systems

In the UL HPC system we support [Singularity containers](/containers). The University of Manchester containers have been repackaged as Singularity containers for use in our systems. The Singularity containers are:

- WRF-WPS version 4.3.3: `/work/projects/singularity/ulhpc/wrf-wps-4.3.3.sif`
- WRF-Chem version 4.3.3: `/work/projects/singularity/ulhpc/wrf-chem-4.3.3.sif`
- WRF-4DVar version 4.3.3: `/work/projects/singularity/ulhpc/wrf-4dvar-4.3.3.sif`

There should be one-to-one correspondence when running the Singularity containers in UL HPC systems and when running the Docker containers in a local machine.

!!! tip
    If you find any issues with the information above, please file a [support ticket](https://hpc.uni.lu/support).
