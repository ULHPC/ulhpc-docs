# Best-effort Jobs


| __Node Type__ | __Slurm command__                                                                 |
|:-------------:|-----------------------------------------------------------------------------------|
| regular       | `sbatch [-A <project>] -p batch  --qos besteffort [-C {broadwell,skylake}] [...]` |
| gpu           | `sbatch [-A <project>] -p gpu    --qos besteffort [-C volta[32]] -G 1 [...]`      |
| bigmem        | `sbatch [-A <project>] -p bigmem --qos besteffort [...]`                          |

Best-effort (preemptible) jobs allow an efficient usage of the platform by filling available computing nodes until regular jobs are submitted.

```
sbatch -p {batch | gpu | bigmem} --qos besteffort [...]
```

??? question "What means job preemption?"
    [Job preemption](https://slurm.schedmd.com/preempt.html) is the the act of "stopping" one or more "low-priority" jobs to let a "high-priority" job run. Job preemption is implemented as a variation of Slurm's Gang Scheduling logic.

    When a **non**-best-effort job is allocated resources that are already allocated to one or more best-effort jobs, the preemptable job(s) (thus on QOS `besteffort`) are preempted.
    On ULHPC facilities, the preempted job(s) can be requeued (if possible) or canceling them.
    **For jobs to be requeued, they MUST have the "`--requeue`" sbatch option set.

The `besteffort` QOS have less constraints than the other QOS (for instance, you can submit more jobs etc. )

As a general rule users should ensure that they track successful completion of best-effort jobs (which may be interrupted by other jobs at any time) and use them in combination with mechanisms such as Checkpoint-Restart that allow applications to stop and resume safely.
