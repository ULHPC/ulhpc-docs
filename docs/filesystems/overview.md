## ULHPC File system overview

<!--content-start-->

The following table summarizes the mount location, backing up, and environment setup for each one of the network file systems.

<!--table-start-->

!!! info "Cluster file systems"

    | Directory                                                                                                  | Environment variable                                           | File system                                      | Backup                                    |
    |------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|--------------------------------------------------|-------------------------------------------|
    | [`/home/users/<username>`](../filesystems/gpfs.md#global-home-directory-home)                              | [`${HOME}`](../filesystems/gpfs.md#global-home-directory-home) | [GPFS/Spectrumscale](../filesystems/gpfs.md) [1] | no                                        |
    | [`/work/projects/<project name>`](../filesystems/gpfs.md#global-project-directory-projecthomeworkprojects) | -                                                              | [GPFS/Spectrumscale](../filesystems/gpfs.md) [1] | yes (partial, only `backup` subdirectory) |
    | [`/scratch/users/<username>`](../filesystems/lustre.md)                                                    | [`${SCRATCH}`](../filesystems/lustre.md)                       | [Lustre](../filesystems/lustre.md)               | no                                        |
    | `/mnt/isilon/projects/<project name>`                                                                      | -                                                              | [OneFS](../filesystems/isilon.md)                | yes (and live sync [2])                   |
    
    1. The  file system mounted on the home directories (`/home/users`) and project directories (`/work/projects`) are both exported by the [GPFS/Spectrumscale](../filesystems/gpfs.md) file system.
    
        - Storage for both directories is redundant, so they are safe against hardware failure.
        - Only `/home/users` is mirrored in a SSD cache, so `/home/users` is a significantly faster for random and small file I/O.
    
    2. Live sync replicates data across multiple OneFS instances for high availability.
