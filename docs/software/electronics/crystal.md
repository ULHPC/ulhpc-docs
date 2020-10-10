[![](https://www.crystal.unito.it/images/slide2_cry17.png){: style="width:300px;float: right;" }](url)
The  [CRYSTAL](https://www.crystal.unito.it/index.php) package
performs `ab  initio` calculations  of  the  ground
state  energy,  energy gradient, electronic wave function and properties
of periodic systems.  Hartree-Fock or Kohn-Sham Hamiltonians
(that adopt an Exchange-Correlation potential following the postulates of
Density-Functional Theory) can be used.  Systems periodic in 0 (molecules, 0D),
1 (polymers,1D), 2 (slabs, 2D), and 3 dimensions (crystals, 3D)
are treated on an equal footing.  In eachcase the fundamental approximation
made is the expansion of the single particle wave functions(’Crystalline Orbital’, CO)
as a linear combination of Bloch functions (BF) defined in terms of
local functions (hereafter indicated as ’Atomic Orbitals’, AOs). 


## Available versions of CRYSTAL in ULHPC
To check available versions of CRYSTAL at UL-HPC type `module spider crystal`.
Below it shows list of available versions of CRYSTAL in ULHPC. 
```bash
chem/CRYSTAL/17-intel-2017a-1.0.1
chem/CRYSTAL/17-intel-2018a-1.0.1
chem/CRYSTAL/17-intel-2019a-1.0.2
```

## Interactive mode
To test CRYTAL in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the module crytal and needed environment
$ module purge
$ module load chem/CRYSTAL/17-intel-2019a-1.0.2

$ Pcrystal >& log.out
```

!!! warning 
    Please note your input file should be named just as `INPUT`. Pcrytal automatically
    will recognize the INPUT file from the folder where you are currently in.
    

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J CRYSTAL
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

# Load the module crytal and needed environment
module purge
module load chem/CRYSTAL/17-intel-2019a-1.0.2

srun -n 56 Pcrystal >& log.out
```
## Additional information
For more information about the tutorial and documention
about CRYSTAL, please refer http://tutorials.crystalsolutions.eu/

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
    