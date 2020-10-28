[![](https://static.macupdate.com/products/27014/l/nvidia-cuda-toolkit-logo.png?v=1568301809){: style="width:300px;float: right;" }](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html)
[CUDA](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html) is a parallel computing platform and programming model developed by NVIDIA
for general computing on graphical processing units (GPUs).
With CUDA, developers are able to dramatically speed up computing
applications by harnessing the power of GPUs.
In GPU-accelerated applications, the sequential part of the
workload runs on the CPU - which is optimized
for single-threaded performance - while the compute intensive portion
of the application runs on thousands of GPU cores in parallel.
When using CUDA, developers program in popular languages such as C, C++, Fortran, Python
and MATLAB and express parallelism through extensions in the form of a few basic keywords.

The CUDA Toolkit from NVIDIA provides everything you need to develop GPU-accelerated applications.
The CUDA Toolkit includes GPU-accelerated libraries, a compiler, development tools and the CUDA runtime.


## Available versions of CUDA in ULHPC
To check available versions of CUDA at ULHPC type `module spider system cuda`.

??? info "The following versions of CUDA are available in ULHPC:"
    ```bash
    # Available versions
    system/CUDA/8.0.61
    system/CUDA/9.1.85
    system/CUDA/9.2.148.1
    system/CUDA/10.0.130
    system/CUDA/10.1.105-GCC-8.2.0-2.31.1
    system/CUDA/10.1.105-iccifort-2019.1.144-GCC-8.2.0-2.31.1
    system/CUDA/10.1.105
    system/CUDA/10.1.243
    system/CUDA/10.2.89
    ```
    
## Interactive mode:
To reserve the 1 GPU on single node with 4 CPU cores:
```bash
$ srun -N 1 -c 4 -p gpu --gpus=1 --time=00:30:00 --pty --x11 bash -i
# OR use the 'si-gpu' helper 
$ si-gpu -N 1 -c 4 -G 1 --x11

# Load the module cuda and needed environment 
$ module purge
$ module load swenv/default-env/v1.2-20191021-production         
$ module load system/CUDA/10.1.243 
```

??? info "To check if you really succeed on having GPU:"
    ```bash  
    $ nvidia-smi
    Tue Oct  6 15:15:11 2020       
    +-----------------------------------------------------------------------------+
    | NVIDIA-SMI 440.64.00    Driver Version: 440.64.00    CUDA Version: 10.2     |
    |-------------------------------+----------------------+----------------------+
    | GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
    | Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
    |===============================+======================+======================|
    |   0  Tesla V100-SXM2...  On   | 00000000:1C:00.0 Off |                    0 |
    | N/A   40C    P0    46W / 300W |      0MiB / 16160MiB |      0%      Default |
    +-------------------------------+----------------------+----------------------+
                                                                               
    +-----------------------------------------------------------------------------+
    | Processes:                                                       GPU Memory |
    |  GPU       PID   Type   Process name                             Usage      |
    |=============================================================================|
    |  No running processes found                                                 |
    +-----------------------------------------------------------------------------+
    ```
    
Example
```bash
# Compilation
$ nvcc -arch=compute_70 vector.cu -o vector

# code execution
$ ./vector
```

??? tip "[Compute capability](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html#compute-capabilities)"
    Different Nivida GPUs architecture supports features of techincal specification,
    which can be enbaled by using `-arch=compute_XX`


## Batch job:
Example for batch script:
```bash
#! /bin/bash -l
#SBATCH -J TEST
#SBATCH --ntasks=1
#SBATCH --ntasks-per-core=1
#SBATCH --time=0-00:10:00
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --qos=qos-gpu

echo "== Starting run at $(date)"
echo "== Job ID: ${SLURM_JOBID}"
echo "== Node list: ${SLURM_NODELIST}"
echo "== Submit dir. : ${SLURM_SUBMIT_DIR}"

module purge
module load swenv/default-env/v1.2-20191021-production
module load system/CUDA/10.1.243

srun nvprof ./vector
```

??? tip "Result output:"

    ```bash
    == Starting run at tor jul 30 20:46:57 CEST 2020
    == Job ID: 1940590
    == Node list: iris-169
    == Submit dir. : /mnt/lscratch/users/ekrishnasamy/MOOC/CUDA/Part-1/Vector
    ==341961== NVPROF is profiling process 341961, command: ./vector
    ==341961== Profiling application: ./vector
    ==341961== Profiling result:
    Type  Time(%)      Time     Calls       Avg       Min       Max  Name
    GPU activities:   94.83%  611.62ms         1  611.62ms  611.62ms  611.62ms  vector_add(float*, float*, float*, int)
    out[0] = 3.000000
    PASSED
    ``` 

## Additional information
To know more about CUDA programming, please refer to [Nvidia CUDA](https://docs.nvidia.com/cuda/cuda-c-programming-guide/index.html)
and also [ULHPC summer school](https://hpc.uni.lu/hpc-school/2019/06/index.html).