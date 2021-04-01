# Optimizers


Mathematical optimization (alternatively spelled optimisation) or mathematical programming is the selection of a best element (with regard to some criterion) from some set of available alternatives. Optimization problems of sorts arise in all quantitative disciplines from computer science and engineering to operations research and economics, and the development of solution methods has been of interest in mathematics for centuries

## Mathematical programming with Cplex and Gurobi

[**Cplex**](https://www.ibm.com/analytics/cplex-optimizer) is an optimization software for mathematical programming.
The Cplex optimizer can solve:

* Mixed-Integer programming problems (MIP)
* Very large linear programming problems (LP)
* Non-convex quadratic programming problems (QP)
* Convex quadratically constrained problems (QCP)

[**Gurobi**](http://www.gurobi.com) is a powerful optimization software and an alternative to Cplex for solving. Gurobi has some additionnal features compared to Cplex. For example, it can perform Mixed-Integer Quadratic Programming (MIQP) and Mixed-Integer Quadratic Constrained Programming (MIQCP).

### Loading Cplex or Gurobi

To use these optimization sfotwares, you need to load the corresponding [Lmod](https://lmod.readthedocs.io/en/latest/) module.

For Cplex

```shell
>$ module load maths/Cplex
```

or for Gurobi

```bash
>$ module load math/Gurobi
``` 

!!! warning
    Modules are not allowed on the access servers. To test interactively Singularity, rememerber to ask for an interactive job first.
    ```bash
    salloc -p interactive     # OR, use the helper script: si
    ```


### Using Cplex 

In order to test cplex and gurobi, we need an optimization instance. Hereafter, we are going to rely on instances from the [miplib](http://miplib2017.zib.de). For example, let us the following instance [ex10.mps.gz](http://miplib2017.zib.de/WebData/instances/ex10.mps.gz) described in details [here](http://miplib2017.zib.de/instance_details_ex10.html) for the interested readers.



#### Multi-threaded optimization with Cplex

In order to solve mathematical programs, cplex allows users to define a command line script that can be passed to the executable. On the Iris cluster, the following launcher can be used to perform multi-threaded MIP optimzation. A good practice is to request as many threads as available cores on the node. If you need more computing power, you have to consider a distributed version.  

```slurm
#!/bin/bash -l
#SBATCH -J Multi-threaded_cplex
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=28
#SBATCH --time=0-01:00:00
#SBATCH -p batch
#SBATCH --qos=normal

# Load cplex 
module load math/CPLEX

# Some variable
MPS_FILE=$1
RES_FILE=$2
CPLEX_COMMAND_SCRIPT="command_job${SLURM_JOBID}.lst"



# Create cplex command script
cat << EOF > ${CPLEX_COMMAND_SCRIPT}
set threads ${SLURM_CPUS_PER_TASK}
read ${MPS_FILE} 
mipopt
write "${RES_FILE}.sol" 
quit
EOF
chmod +x ${CPLEX_COMMAND_SCRIPT}

# Cplex will use the required number of thread
cplex -f ${CPLEX_COMMAND_SCRIPT}
rm ${CPLEX_COMMAND_SCRIPT}
```


Using the script ```cplex_mtt.slurm ```, you can launch a batch job with the ```sbatch``` command as follows ``` sbatch cplex_mtt.slurm ex10.mps.gz cplex_mtt```.




#### Distributed optimization with Cplex

When you require more computing power (e.g. more cores), distributed computations is the way to go. The cplex optimization software embeds a feature that allows you to perform distributed MIP. Using the Message Passing Interface (MPI), cplex will distribute the exploration of the tree search to multiple workers.
The below launcher is an example showing how to reserve ressources on multiple nodes through the Slurm scheduler. In this example, 31 tasks will be distributed over 2 nodes. 


```slurm
#!/bin/bash -l
#SBATCH -J Distrbuted\_cplex
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=14
#SBATCH -c 2    # multithreading -- #threads (slurm cpu) per task 
#SBATCH --time=0-01:00:00
#SBATCH -p batch
#SBATCH --qos=normal
module load math/CPLEX

# Some variables
MPS_FILE=$1
RES_FILE=$2
CPLEX_COMMAND_SCRIPT="command_job${SLURM_JOBID}.lst"



# Create cplex command script
cat << EOF > ${CPLEX_COMMAND_SCRIPT}
set distmip config mpi
set threads ${SLURM_CPUS_PER_TASK}
read ${MPS_FILE} 
mipopt
write "${RES_FILE}.sol" 
quit
EOF
chmod +x ${CPLEX_COMMAND_SCRIPT}

# Start Cplex with MPI
# On first host, the master is running 
mpirun -np 1 cplex -f ${CPLEX_COMMAND_SCRIPT} -mpi : -np $((SLURM_NTASKS - 1)) cplex -mpi
rm ${CPLEX_COMMAND_SCRIPT}
```

Using the script ```cplex_dist.slurm ```, you can launch a batch job with the ```sbatch``` command as follows ``` sbatch cplex_dist.slurm ex10.mps.gz cplex_dist```.

### Gurobi

#### Multi-threaded optimization with Gurobi

The script below allows you to start multi-threaded MIP optimization with Gurobi. 


```slurm
#!/bin/bash -l
#SBATCH -J Multi-threaded_gurobi
#SBATCH --ntasks-per-node=1
#SBATCH -c 28     # multithreading -- #threads (slurm cpu) per task 
#SBATCH --time=0-01:00:00
#SBATCH -p batch
#SBATCH --qos=normal

# Load Gurobi 
module load math/Gurobi

# Some variable
MPS_FILE=$1
RES_FILE=$2

# Gurobi will access use the required number of thread
gurobi_cl Threads=${SLURM_CPUS_PER_TASK} ResultFile="${RES_FILE}.sol" ${MPS_FILE}
```

Using the script ```gurobi_mtt.slurm ```, you can launch a batch job with the ```sbatch``` command as follows ``` sbatch gurobi_mtt.slurm ex10.mps.gz gurobi_mtt```.

#### Distributed optimization with Gurobi 



```slurm
#!/bin/bash -l
#SBATCH -J Distrbuted_gurobi
#SBATCH -N 3       # Number of nodes
#SBATCH --ntasks-per-node=1
#SBATCH -c 5   # multithreading -- #threads (slurm cpu) per task 
#SBATCH --time=00:15:00
#SBATCH -p batch
#SBATCH --qos normal
#SBATCH -o %x-%j.log

# Load personal modules
mu
# Load gurobi
module load math/Gurobi

export MASTER_PORT=61000
export SLAVE_PORT=61000
export MPS_FILE=$1
export RES_FILE=$2
export GUROBI_INNER_LAUNCHER="inner_job${SLURM_JOBID}.sh"

if [[ -f "grb_rs.cnf" ]];then
    sed -i "s/^THREADLIMIT.*$/THREADLIMIT=${SLURM_CPUS_PER_TASK}/g" grb_rs.cnf
else
    $GUROBI_REMOTE_BIN_PATH/grb_rs init
    echo "THREADLIMIT=${SLURM_CPUS_PER_TASK}" >> grb_rs.cnf
fi


cat << 'EOF' > ${GUROBI_INNER_LAUNCHER}
#!/bin/bash
MASTER_NODE=$(scontrol show hostname ${SLURM_NODELIST} | head -n 1)
    ## Load configuration and environment
    if [[ ${SLURM_PROCID} -eq 0 ]]; then
        ## Start Gurobi master worker in background
         $GUROBI_REMOTE_BIN_PATH/grb_rs --worker --port ${MASTER_PORT} &
         wait
    elif [[ ${SLURM_PROCID} -eq 1 ]]; then
        sleep 5
        grbcluster nodes --server ${MASTER_NODE}:${MASTER_PORT} 
        gurobi_cl Threads=${SLURM_CPUS_PER_TASK} ResultFile="${RES_FILE}.sol" Workerpool=${MASTER_NODE}:${MASTER_PORT} DistributedMIPJobs=$((SLURM_NNODES -1)) ${MPS_FILE}
    else
        sleep 2
        ## Start Gurobi slave worker in background
        $GUROBI_REMOTE_BIN_PATH/grb_rs --worker --port ${MASTER_PORT} --join ${MASTER_NODE}:${MASTER_PORT} &
        wait
fi
EOF
chmod +x ${GUROBI_INNER_LAUNCHER}

## Launch Gurobi and wait for it to start
srun ${GUROBI_INNER_LAUNCHER} &
while [[ ! -e "${RES_FILE}.sol" ]]; do
    sleep 5
done
rm ${GUROBI_INNER_LAUNCHER}
```


Using the script ```gurobi_dist.slurm ```, you can launch a batch job with the ```sbatch``` command as follows ``` sbatch gurobi_dist.slurm ex10.mps.gz gurobi_dist```.
