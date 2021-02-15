# Long Jobs

If you are confident that your jobs will last more than 2 days **while efficiently using the allocated resources**, you can use [`--qos long`](long.md) QOS.
```
sbatch -p {batch | gpu | bigmem} --qos long [...]
```

Following EuroHPC/PRACE Recommendations, the `long` QOS allow for an extended Max walltime (`MaxWall`) set to **14 days**.

| __Node Type__ | __Slurm command__                                                           |
|:-------------:|-----------------------------------------------------------------------------|
| regular       | `sbatch [-A <project>] -p batch  --qos long [-C {broadwell,skylake}] [...]` |
| gpu           | `sbatch [-A <project>] -p gpu    --qos long [-C volta[32]] -G 1 [...]`      |
| bigmem        | `sbatch [-A <project>] -p bigmem --qos long [...]`                          |

!!! important
    Be aware however that special restrictions applies for this kind of jobs.

    * There is a limit to the maximum number of concurrent nodes involved in `long` jobs (see `sqos` for details).
    * No more than **4** `long` jobs per User (`MaxJobsPU`) are allowed, using no more than 2 nodes per jobs.
