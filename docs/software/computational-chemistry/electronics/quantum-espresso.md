[![](https://www.quantum-espresso.org/user/themes/quantum/images/logo_header.jpg){: style="width:300px;float: right;" }](https://www.quantum-espresso.org/project/manifesto)
[Quantum ESPRESSO](https://www.quantum-espresso.org/project/manifesto)
is an integrated suite of Open-Source computer codes for electronic-structure
calculations and materials modeling at the nanoscale.
It is based on density-functional theory, plane waves, and pseudopotentials.

Quantum ESPRESSO has evolved into a distribution of independent and
inter-operable codes in the spirit of an open-source project.
The Quantum ESPRESSO distribution consists of a “historical”
core set of components, and a set of plug-ins that perform more advanced tasks,
plus a number of third-party packages designed to be inter-operable with
the core components. Researchers active in the field of electronic-structure
calculations are encouraged to participate in the project by
contributing their own codes or by implementing their own
ideas into existing codes.


## Available versions of Quantum ESPRESSO in ULHPC
To check available versions of Quantum ESPRESSO at ULHPC type `module spider quantum espresso`.
The following list shows the available versions of Quantum ESPRESSO in ULHPC. 
```bash
chem/QuantumESPRESSO/6.1-intel-2017a
chem/QuantumESPRESSO/6.1-intel-2018a-maxter500
chem/QuantumESPRESSO/6.1-intel-2018a
chem/QuantumESPRESSO/6.2.1-intel-2018a
chem/QuantumESPRESSO/6.4.1-intel-2019a
```

## Interactive mode
To open an Quantum ESPRESSO in the interactive mode, please follow the following steps:

```bash
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ salloc -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11  # OR si --x11 [...]

# Load the module quantumespresso and needed environment 
$ module purge
$ module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
$ module load chem/QuantumESPRESSO/6.4.1-intel-2019a

$ pw.x -input example.in
```

## Batch mode
```bash
#!/bin/bash -l
#SBATCH -J QuantumESPRESSO
#SBATCH -N 2
#SBATCH -A <project name>
#SBATCH -M --cluster iris 
#SBATCH --ntasks-per-node=28
#SBATCH --time=00:30:00
#SBATCH -p batch

# Load the module quantumespresso and needed environment 
module purge
module load swenv/default-env/devel # Eventually (only relevant on 2019a software environment) 
module load chem/QuantumESPRESSO/6.4.1-intel-2019a

srun -n ${SLURM_NTASKS} pw.x -input example.inp
```

## Additional information
To know more information about Quantum ESPRESSO tutorial and documentation,
please refer to [Quantum ESPRESSO user manual](https://www.quantum-espresso.org/resources/users-manual).

!!! tip
    If you find some issues with the instructions above,
    please report it to us using [support ticket](https://hpc.uni.lu/support).
