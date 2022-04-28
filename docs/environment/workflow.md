## ULHPC Workflow

<!--intro-start-->

Your typical journey on the ULHPC facility is illustrated in the below figure.

![](../images/ULHPC-simplified-workflow-overview.png)

<!--intro-end-->

??? info "Typical workflow on UL HPC resources"
    You daily interaction with the ULHPC facility includes the following
    actions:

    __Preliminary setup__

    1. Connect to the [access/login servers](../connect/access.md)
        - This can be done either by [`ssh`](../connect/ssh.md)
        (**recommended**) or via the [ULHPC OOD portal](../connect/ood.md)
        - (_advanced users_) at this point, you probably want to create (or
        reattach) to a `screen` or `tmux` session
    2. Synchronize you code and/or [transfer your input
    data](../data/transfer.md) using `rsync/svn/git` typically
        - recall that the [different storage
        filesystems](../filesystems/index.md) are **shared** (via a [high-speed
        interconnect network](../interconnect/ib.md)) among the computational
        resources of the ULHPC facilities. In particular, it is sufficient to
        exchange data with the access servers to make them available on the
        clusters
    3. Reserve a few [interactive resources](../jobs/interactive.md) with `salloc -p interactive [...]`
         - recall that the `module` command (used to load the [ULHPC User
       software](../software/index.md)) is **only** available on the compute
       nodes
         - (_eventually_) [build](../software/build.md) your program, typically using `gcc/icc/mpicc/nvcc..`
         - Test your workflow / HPC analysis on a _small_ size problem (`srun/python/sh...`)
         - Prepare a [launcher script](../slurm/launchers.md) `<launcher>.{sh|py}`

    Then you can proceed with your __Real Experiments__:

    1. Reserve [passive resources](../jobs/submit.md): `sbatch [...] <launcher>`
    2. Grab the results and (eventually) [transfer back your output
       results](../data/transfer.md) using `rsync/svn/git`
