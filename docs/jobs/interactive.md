# Interactive Jobs

The `interactive` (_floating_) [partition](../slurm/partitions.md) (exclusively associated to the [`debug` QOS](../slurm/qos.md)) is **to be used for code development, testing, and debugging**.

!!! important
    **Production runs are not permitted in interactive jobs**. User accounts are subject to suspension if they are determined to be using the `interactive` partition and the `debug` QOS for production computing. In particular, interactive job "chaining" is not allowed. Chaining is defined as using a batch script to submit another batch script.

You can access the different node classes available using the `-C <class>` flag (see also [List of Slurm features on ULHPC nodes](../slurm/index.md#hw-characteristics-and-slurm-features-of-ulhpc-nodes)), or (__better__) through the [custom helper functions](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh) defined for each category of nodes, _i.e._ `si`, `si-gpu` or `si-bigmem`:

=== "Regular Dual-CPU node"
    !!! example ""
        ```bash
        ### Quick interative job for the default time
        $ si
        # salloc -p interactive --qos debug -C batch

        ### Explicitly ask for a skylake node
        $ si -Cskylake
        # salloc -p interactive --qos debug -C batch -Cskylake

        ### Use 1 full node for 28 tasks
        $ si --ntasks-per-node=28
        # salloc -p interactive --qos debug -C batch --ntasks-per-node=28

        ### interactive job for 2 hours
        $ si -t2:00:00
        # salloc -p interactive --qos debug -C batch -t2:00:00

        ### interactive job on 2 nodes, 1 multithreaded tasks per node
        $ si -N2 --ntasks-per-node=1 -c4
        # salloc -p interactive --qos debug -C batch -N2 --ntasks-per-node=1 -c4
        ```

=== "GPU node"
    !!! example ""
        ```bash
        ### Quick interative job for the default time
        $ si-gpu
        # /!\ WARNING: append -G 1 to really reserve a GPU
        # salloc -p interactive --qos debug -C gpu -G 1

        ### (Better) Allocate 1/4 of available CPU cores per GPU to manage
        $ si-gpu -G1 -c7
        $ si-gpu -G2 -c14
        $ si-gpu -G4 -c28
        ```

=== "Large-Memory node"
    !!! example ""
        ```bash
        ### Quick interative job for the default time
        $ si-bigmem
        # salloc -p interactive --qos debug -C bigmem

        ### interactive job with 1 multithreaded task per socket available (4 in total)
        $ si-bigmem --ntasks-per-node=4 --ntasks-per-socket=1 -c28
        # salloc -p interactive --qos debug -C bigmem --ntasks-per-node=4 --ntasks-per-socket=1 -c4

        ### interactive job for 1 task but 512G of memory
        $ si-bigmem --mem=512G
        # salloc -p interactive --qos debug -C bigmem --mem=512G
        ```

If you prefer to rely on the regular [`srun`](https://slurm.schedmd.com/srun.html), the below table proposes the equivalent commands run by the helper scripts `si*`:

| Node Type | UL HPC helper function         | Slurm command                                                                                                                                                                                                                               |
|:----------|:------------------------------:|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| regular   | `si [...]`                     | `salloc --partition=interactive --qos=debug --constraint=batch [...]`<br/>`salloc --partition=interactive --qos=debug --constraint=batch,broadwell [...]`<br/>`salloc --partition=interactive --qos=debug --constraint=batch,skylake [...]` |
| gpu       | `si-gpu [...]`                 | `salloc --partition=interactive --qos=debug --constraint=gpu,[volta[32]] --gpus=1 [...]`                                                                                                                                                    |
| bigmem    | `si-bigmem [...]`              | `salloc --partition=interactive --qos=debug --constraint=bigmem [...]`                                                                                                                                                                      |


!!! important "Impact of Interactive jobs implementation over a _floating_ partition"
    We have recently changed the way interactive jobs are served. Since the [`interactive` partition](../slurm/partitions.md) is no longer dedicated but _floating_ above the other partitions, there is **NO** guarantee to have an interactive job running if the surrounding partition (`batch`, `gpu` or `bigmem`) is full.

    **However**, the [backfill scheduling](priority.md#backfill-scheduling) in place together with the partition [priority](priority.md) set ensure that interactive jobs will be first served upon resource release.
