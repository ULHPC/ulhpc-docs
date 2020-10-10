[![](https://upload.wikimedia.org/wikipedia/en/a/a2/MS3_NWChem.logo3.png){: style="width:300px;float: right;" }](url)
[NWChem](https://nwchemgit.github.io/) aims to provide its users with computational chemistry tools that
are scalable both in their ability to efficiently treat large scientific
problems, and in their use of available computing resources from
high-performance parallel supercomputers to conventional workstation clusters.

## Available versions of NWChem in ULHPC
To check available versions of NWChem at ULHPC type `module spider nwchem`.
Below it shows list of available versions of NWChem in ULHPC.

```bash
chem/NWChem/6.6.revision27746-intel-2017a-2015-10-20-patches-20170814-Python-2.7.13
chem/NWChem/6.8.revision47-intel-2018a-Python-2.7.14
chem/NWChem/6.8.revision47-intel-2019a-Python-2.7.15
```

## Interactive mode
To try NWChem in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the module nwchem and needed environment 
$ module purge
$ module load swenv/default-env/v1.2-20191021-production
$ module load chem/NWChem/6.8.revision47-intel-2019a-Python-2.7.15

$ nwchem example
```

!!! warning "naming input file`"
    Please note example file should be named with extension like `example.nw`.
    

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J NWChem
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

# Load the module nwchem and needed environment 
module purge 
module load swenv/default-env/v1.2-20191021-production
module load chem/NWChem/6.8.revision47-intel-2019a-Python-2.7.15

srun -n 56 nwchem example 
```
## Additional information
For more information about the tutorial and documention about NWChem,
please refer https://nwchemgit.github.io/Home.html

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).  