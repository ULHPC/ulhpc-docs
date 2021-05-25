[![](https://images.g2crowd.com/uploads/product/image/large_detail/large_detail_d05e3566f966e83e3ef9753e3aed4086/abaqus.png){: style="width:300px;float: right;" }](https://www.3ds.com/products-services/simulia/products/abaqus/abaquscae/)

The [Abaqus Unified FEA](https://www.3ds.com/products-services/simulia/products/abaqus/abaquscae/)
product suite offers powerful and complete solutions
for both routine and sophisticated engineering problems covering a vast
spectrum of industrial applications. In the automotive industry engineering
work groups are able to consider full vehicle loads, dynamic vibration,
multibody systems, impact/crash, nonlinear static, thermal coupling, and
acoustic-structural coupling using a common model data structure and integrated
solver technology. Best-in-class companies are taking advantage of
Abaqus Unified FEA to consolidate their processes and tools,
reduce costs and inefficiencies, and gain a competitive advantage

## Available versions of Abaqus in ULHPC

??? info [ULHPC Software/Modules Environment](../../environment/modules.md)
     For the user's convenience, we are maintaining the old
     version and new version of each software that are available at
     the ULHPC. To work with different software sets and how to
     load them to your environment is clearly explained
     in [Modules](ulhpc-docs/docs/environment
     /modules.md). For example, if your module path is set to deprecated modules
     `export MODULEPATH=$DEPRECATED_MODULEPATH` then the
     following versions of Abaqus are available in ULHPC:

```bash
# Available versions
 cae/ABAQUS/6.14.2
 cae/ABAQUS/2017-hotfix-1729
 cae/ABAQUS/2017-hotfix-1740
 cae/ABAQUS/2017-hotfix-1745
 cae/ABAQUS/2017-hotfix-1803
 cae/ABAQUS/2018-hotfix-1806
```

## Interactive mode
To open an Abaqus in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p batch --time=00:30:00 --ntasks 1 -c 4 --x11

# Load the required version of Abaqus and needed environment
$ module purge
$ module load swenv/default-env/v0.1-20170602-production
$ module load cae/ABAQUS/2017-hotfix-1803
$ module load vis/libGLU/9.0.0-intel-2017a
# /!\ IMPORTANT: ADAPT the url to point to YOUR licence server!!!
$ export LM_LICENSE_FILE=xyz
# Check License server token available
$ abaqus licensing lmstat -a
lmutil - Copyright (c) 1989-2015 Flexera Software LLC. All Rights Reserved.
Flexible License Manager status on Wed 4/8/2020 14:25
[...]
$ abaqus job=job-name input=input.inp cpus=n gpus=n
```
where `n=number of cores` and for gpus `n=number of GPUs`.

??? info

    To check available license and group you belongs to:`$ abaqus licensing lmstat -a`
    
The following options for simulation to stop and resume it:
```bash
$ abaqus job=job-name suspend
$ abaqus job=job-name resume
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J Abaqus
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:30:00
#SBATCH -p batch

# Write out the stdout+stderr in a file
#SBATCH -o output.txt

# Mail me on job start & end
#SBATCH --mail-user=myemailaddress@universityname.domain
#SBATCH --mail-type=BEGIN,END

# To get basic info. about the job
echo "== Starting run at $(date)"
echo "== Job ID: ${SLURM_JOBID}"
echo "== Node list: ${SLURM_NODELIST}"
echo "== Submit dir. : ${SLURM_SUBMIT_DIR}"

# Load the required version of Abaqus and needed environment
module purge
module load swenv/default-env/v0.1-20170602-production
module load cae/ABAQUS/2017-hotfix-1803
module load vis/libGLU/9.0.0-intel-2017a
# /!\ IMPORTANT: ADAPT the url to point to YOUR licence server!!!
export LM_LICENSE_FILE=xyz
# check licenses available
abaqus licensing lmstat -a
abaqus-mpi job=job input=input.inp interactive
```

## Additional information
To know more about Abaqus documentation and tutorial,
please refer [Abaqus CAE](http://130.149.89.49:2080/v6.11/pdf_books/CAE.pdf)

??? Tutorial 
     * http://www.franc3d.com/wp-content/uploads/2012/05/FRANC3D_V7_ABAQUS_Tutorial.pdf
     * https://sig.ias.edu/files/Abaqus%20tutorial.pdf
     * https://sites.engineering.ucsb.edu/~tshugar/GET_STARTED.pdf?fbclid=IwAR2MQTzCTISqdPuM4D3PiDwXk9oVTBqZWXJUvMccVPYsd1kKPwPOZcnq078


!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).

