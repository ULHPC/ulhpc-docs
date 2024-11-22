[![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e5/ANSYS_logo.png/320px-ANSYS_logo.png){: style="width:200px;float: right;" }](https://www.ansys.com/) [ANSYS](https://www.ansys.com/) offers a comprehensive software suite that spans the entire range of physics, providing access to virtually any field of engineering simulation that a design process requires.


## Available versions of ANSYS in ULHPC
To check available versions of ANSYS at ULHPC type `module spider ansys`. The following versions of ANSYS are available in ULHPC:
```bash
# Available versions 
tools/ANSYS/18.0
tools/ANSYS/19.0
tools/ANSYS/19.4
```

## Interactive mode
To open an ANSYS in the interactive mode, please follow the following steps:
```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 

# Load the required version of ANSYS and needed environment
$ module purge
$ module load toolchain/intel/2019a
$ module load tools/ANSYS/19.4

# To launch ANSYS workbench
$ runwb2
```

## Batch mode

```bash
#!/bin/bash -l
#SBATCH -J ANSYS-CFX
#SBATCH -N 2
#SBATCH --ntasks-per-node=28
#SBATCH --ntasks-per-socket=14
#SBATCH -c 1
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

# Load the required version of ANSYS and needed environment
module purge
module load toolchain/intel/2019a
module load tools/ANSYS/19.4

# The Input file
defFile=Benchmark.def

MYHOSTLIST=$(srun hostname | sort | uniq -c | awk '{print $2 "*" $1}' | paste -sd, -)
echo $MYHOSTLIST
cfx5solve -double -def $defFile -start-method "Platform MPI Distributed Parallel" -par-dist $MYHOSTLIST
```

## Additional information
ANSYS provides the [customer support](https://support.ansys.com), if you have a license key, you should be able to get all the support and needed documents.

!!! tip
    If you find some issues with the instructions above, please file a [support ticket](https://hpc.uni.lu/support).
