[![](https://www.nvidia.com/content/dam/en-zz/Solutions/Data-Center/gromacs/GROMACS-Logo.png){: style="width:300px;float: right;" }](http://www.gromacs.org/)
[GROMACS](http://www.gromacs.org/) is a versatile package to perform molecular dynamics, i.e. simulate
the Newtonian equations of motion for systems with hundreds to millions of particles.
It is primarily designed for biochemical molecules like proteins, lipids and nucleic
acids that have a lot of complicated bonded interactions, but since GROMACS
is extremely fast at calculating the nonbonded interactions
(that usually dominate simulations) many groups are also using it
for research on non-biological systems, e.g. polymers.

## Available versions of GROMACS in ULHPC
To check available versions of GROMACS at ULHPC type `module spider gromacs`.
Below it shows list of available versions of GROMACS in ULHPC. 
```bash
bio/GROMACS/2016.3-intel-2017a-hybrid
bio/GROMACS/2016.5-intel-2018a-hybrid
bio/GROMACS/2019.2-foss-2019a
bio/GROMACS/2019.2-fosscuda-2019a
bio/GROMACS/2019.2-intel-2019a
bio/GROMACS/2019.2-intelcuda-2019a
```

## Interactive mode
To try GROMACS in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the module gromacs and needed environment 
$ module purge
$ module load bio/GROMACS/2019.2-intel-2019a

$ gmx_mpi mdrun <all your GMX job specification options in here>
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J GROMACS
#SBATCH -N 2
#SBATCH --ntasks-per-node=56
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

# Load the module gromacs and needed environment 
module purge
module load bio/GROMACS/2019.2-intel-2019a

srun gmx_mpi mdrun <all your GMX job specification options in here>
```
## Additional information
To know more information about GROMACS tutorial and documentation,
please refer to [GROMACS documentation](http://manual.gromacs.org/).

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).  