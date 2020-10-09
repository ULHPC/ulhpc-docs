[VASP](https://www.vasp.at/documentation/) is a package for performing ab initio quantum-mechanical molecular dynamics (MD)
using pseudopotentials and a plane wave basis set. The approach implemented in VASP
is based on a finite-temperature local-density approximation (with the free energy as variational quantity)
and an exact evaluation of the instantaneous electronic ground state at each MD step
using efficient matrix diagonalization schemes and an efficient Pulay mixing.


## Available versions of VASP in UL-HPC
To check available versions of VASP at UL-HPC type `module spider vasp`.
Below it shows list of available versions of VASP in UL-HPC.
```bash
phys/VASP/5.4.4-intel-2017a
phys/VASP/5.4.4-intel-2018a
phys/VASP/5.4.4-intel-2019a
```

## Interactive mode
To open an Quantum VASP in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the modules
$ module purge
$ module load phys/VASP/5.4.4-intel-2019a

$ vasp_[std/gam/ncl]
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J VASP
#SBATCH -N 2
#SBATCH --ntasks-per-node=56
#SBATCH --time=00:30:00
#SBATCH -p batch

# Write out the stdout+stderr in a file
#SBATCH -o output.txt

# Mail me on job start & end
#SBATCH --mail-user=myemailaddress@universityname.domain
#SBATCH --mail-type=BEGIN,END

echo "== Starting run at $(date)"
echo "== Job ID: ${SLURM_JOBID}"
echo "== Node list: ${SLURM_NODELIST}"
echo "== Submit dir. : ${SLURM_SUBMIT_DIR}"

# Load the modules
module purge
module load phys/VASP/5.4.4-intel-2019a

srun vasp_[std/gam/ncl]
```

## Additional information
For more information about the tutorial and documention about VASP,
please refer https://www.vasp.at/wiki/index.php/The_VASP_Manual

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).        