[The Atomic Simulation Environment (ASE)](https://wiki.fysik.dtu.dk/ase/) is a set of tools and Python
modules for setting up, manipulating, running, visualizing and
analyzing atomistic simulations. The code is freely available
under the GNU LGPL license. ASE provides interfaces to different
codes through `Calculators` which are used together with the
central `Atoms` object and the many available algorithms in ASE.


## Available versions of ASE in ULHPC
To check available versions of ASE at ULHPC type `module spider ase`.
Below it shows list of available versions of ASE in ULHPC.
```bash
chem/ASE/3.13.0-intel-2017a-Python-2.7.13
chem/ASE/3.16.0-foss-2018a-Python-2.7.14
chem/ASE/3.16.0-intel-2018a-Python-2.7.14
chem/ASE/3.17.0-foss-2019a-Python-3.7.2
chem/ASE/3.17.0-intel-2019a-Python-2.7.15
chem/ASE/3.17.0-intel-2019a-Python-3.7.2
```

## Interactive mode
To open an ASE in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the module ase and needed environment
$ module purge
$ module load swenv/default-env/v1.2-20191021-production
$ module load chem/ASE/3.17.0-intel-2019a-Python-3.7.2

$ python3 example.py
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J ASE
#SBATCH -N 1
#SBATCH --ntasks-per-node=1
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

# Load the module ase and needed environment
module purge
module load swenv/default-env/v1.2-20191021-production
module load chem/ASE/3.17.0-intel-2019a-Python-3.7.2

python3 example.py
```

## Additional information
For more information about the tutorial and documention about ASE,
please refer https://wiki.fysik.dtu.dk/ase/tutorials/tutorials.html

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
    