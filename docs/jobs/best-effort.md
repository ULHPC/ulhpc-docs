# Best-effort Jobs

Best-effort jobs are [preemptible](https://slurm.schedmd.com/preempt.html) jobs that can be interrupted by higher priority jobs. Job preemption is the act of "stopping" one or more "low-priority" jobs to let a "high-priority" job run. Job preemption is implemented as a variation of Slurm's Gang Scheduling logic.

- Preemptible jobs can be scheduled for requeuing upon preemption with the [`--requeue`](https://slurm.schedmd.com/sbatch.html#OPT_requeue) option of `sbatch`.
- When a job is requeued, the batch script is initiated from its beginning.
- The `besteffort` [QoS](/slurm/qos/) is the only preemptible QoS in UL HPC systems.

To submit a job in the `besteffort` [QoS](/slurm/qos/) set the `--qos` option as follows.

```shell
sbatch --partition={batch|gpu|bigmem} --qos=besteffort [...]
```

A few examples for submitting `besteffort` [OoS](/slurm/qos/) are the following in the various compute node types are summarized in the following table.

| Node Type | Slurm command                                                                                                         |
|-----------|-----------------------------------------------------------------------------------------------------------------------|
| regular   | `sbatch [--account=<project>] --partition=batch          --qos=besteffort [--constraints={broadwell,skylake}] [...]`  |
| gpu       | `sbatch [--account=<project>] --partition={gpu,hopper}   --qos=besteffort --gpus=1 [--constraint=volta{16,32}] [...]` |
| bigmem    | `sbatch [--account=<project>] --partition=bigmem         --qos=besteffort [...]`                                      |

!!! question "Why use preemtible jobs?"
    Best-effort (preemptible) jobs allow an efficient usage of the platform resources. Usually when jobs are scheduled, some compute nodes are left unexploited. [Backfilling](https://slurm.schedmd.com/sched_config.html#backfill) can be used to schedule some lower priority jobs in leftover nodes, but these jobs must fill in the "time" gaps left by higher priority jobs. Preemptible jobs relax the time constrains, by allowing the scheduler to schedule them in "time" gaps where they do not fit, knowing that they can be interrupted at any time to schedule a higher priority job.

    As a result of their scheduling flexibility, `besteffort` QoS have less constraints than the other QoS (for instance, you can submit more jobs).

!!! warning "Computing with best-effort jobs"
    Best-effort jobs with the `--requeue` option are launched from the beginning each time they are requeued.

    - The user must ensure that checkpoint-restart or another progress tracking mechanism is used to ensure that best-effort jobs can be stop and resumed without losing any computation progress.
    - A best-effort job with the `--requeue` option is requeued until the job exits on its own (successfully or otherwise).
