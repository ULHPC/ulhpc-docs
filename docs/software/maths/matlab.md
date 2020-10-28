[![](https://pbs.twimg.com/profile_images/1041686882915155968/qw90wxxo.jpg){: style="width:300px;float: right;" }](https://nl.mathworks.com/)
[MATLAB®](https://nl.mathworks.com/products/matlab.html) combines
a desktop environment tuned for iterative analysis and design processes
with a programming language that expresses matrix and array mathematics directly.
It includes the Live Editor for creating scripts that combine code, output,
and formatted text in an executable notebook.


## Available versions of MATLAB in ULHPC
To check available versions of MATLAB at ULHPC type `module spider matlab`.
Below it shows list of available versions of MATLAB in ULHPC. 
```shell
base/MATLAB/2017a
base/MATLAB/2018a
base/MATLAB/2019a
base/MATLAB/2019b
```

## Interactive mode
To open an MATLAB in the interactive mode, please follow the following steps:

```shell
# From your local computer
$ ssh -X iris-cluster

# Reserve the node for interactive computation
$ srun -p interactive --time=00:30:00 --ntasks 1 -c 4 --x11 --pty bash -i

# Load the module MATLAB and needed environment
$ module purge
$ module load base/MATLAB/2019b

$ matlab &
```

## Batch mode
### An example for serial case

```shell
#!/bin/bash -l
#SBATCH -J MATLAB
#SBATCH -A <project name>
#SBATCH --ntasks-per-node 1
#SBATCH -c 1
#SBATCH --time=00:15:00
#SBATCH -p batch

# Load the module Julia and needed environment
module purge
module load swenv/default-env/devel
module load base/MATLAB/2019b

srun matlab -nodisplay -r matlab_script_file -logfile output.out

# example for if you need to have a input parameters for the computations
srun matlab -nodisplay -r 'iteration(2,2,1)' -logfile output.out

rm -rf /home/users/ur_user_name/.matlab
rm -rf /home/users/ur_user_name/java*
```

### An example for parallel case

```shell
#!/bin/bash -l
#SBATCH -J MATLAB
#SBATCH -A <project name>
#SBATCH -N 1
#SBATCH -c 28
#SBATCH --time=00:10:00
#SBATCH -p batch

# Load the module Julia and needed environment
module purge
module load swenv/default-env/devel
module load base/MATLAB/2019b

srun -c $SLURM_CPUS_PER_TASK matlab -nodisplay -r matlab_script_file -logfile output.out

rm -rf /home/users/ur_user_name/.matlab
rm -rf /home/users/ur_user_name/java*
```

!!! exmaple

    ```shell
    # example for MATLAB ParFor (matlab_script_file.m)
    parpool('local', str2num(getenv('SLURM_CPUS_PER_TASK'))) % set the default cores
    %as number of threads
    tic
    n = 50;
    A = 50;
    a = zeros(1,n);
    parfor i = 1:n
    a(i) = max(abs(eig(rand(A))));
    end
    toc
    delete(gcp); % you have to delete the parallel region after the work is done
    exit;
    ```

## Additional information
To know more information about MATLAB tutorial and documentation,
please refer to [MATLAB tutorial](https://nl.mathworks.com/academia/books.html).

!!! tip
If you find some issues with the instructions above,
please file a [support ticket](https://hpc.uni.lu/support).