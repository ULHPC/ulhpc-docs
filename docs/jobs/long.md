# Long Jobs

If you are confident that your jobs will last more than 2 days **while efficiently using the allocated resources**, you can use a long [QoS](/slurm/qos/).

```shell
sbatch --partition={batch|gpu|bigmem} --qos=<cluster>-<partition>-long [...]
```

Following EuroHPC/PRACE Recommendations, the `long` QOS allow for an extended Max walltime (`MaxWall`) set to **14 days**.

| Node Type     | Cluster | Partition | Slurm command                                                                                                       |
|---------------|---------|-----------|---------------------------------------------------------------------------------------------------------------------|
| regular       | aion    | batch     | `sbatch [--account=<project>] --partition=batch  --qos=aion-batch-long  [...]`                                      |
| regular       | iris    | batch     | `sbatch [--account=<project>] --partition=batch  --qos=iris-batch-long  [--constraint={broadwell,skylake}] [...]`   |
| gpu (v100)    | iris    | gpu       | `sbatch [--account=<project>] --partition=gpu    --qos=iris-gpu-long    --gpus=1 [--constraint=volta{16,32}] [...]` |
| gpu (h100)    | iris    | hopper    | `sbatch [--account=<project>] --partition=hopper --qos=iris-hopper-long --gpus=1 [...]`                             |
| bigmem        | iris    | bigmem    | `sbatch [--account=<project>] --partition=bigmem --qos=iris-bigmem-long [...]`                                      |

!!! important
    Be aware however that special [restrictions](/slurm/qos/#available-qoss) apply to long jobs. In sort, the constraints are the following.

    - There is a per partition limit to the maximum number of concurrent nodes involved in long jobs (call the alias `sqos` defined in UL HPC systems for details).
    - In `batch` partitions no more than **8** long jobs per User (`MaxJobsPU`) are allowed, using no more than **16** nodes per jobs.
    - In `gpu` partition no more than **4** long jobs per User (`MaxJobsPU`) are allowed, using no more than **2** nodes per jobs.
    - In `bigmem` partition no more than **4** long jobs per User (`MaxJobsPU`) are allowed, using no more than **2** nodes per jobs.
