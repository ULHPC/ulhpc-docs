## ULHPC File system overview

<!--content-start-->

The following table summarizes the mount location, backing up, and environment setup for each one of the network file systems.

<!--table-start-->

| Directory                                                                                                  | Environment variable                                           | File system                                  | Backup                               |
|------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|----------------------------------------------|--------------------------------------|
| [`/home/users/<username>`](../filesystems/gpfs.md#global-home-directory-home)                              | [`${HOME}`](../filesystems/gpfs.md#global-home-directory-home) | [GPFS/Spectrumscale](../filesystems/gpfs.md) | no                                   |
| [`/work/projects/<project name>`](../filesystems/gpfs.md#global-project-directory-projecthomeworkprojects) | -                                                              | [GPFS/Spectrumscale](../filesystems/gpfs.md) | yes (partial, `backup` subdirectory) |
| [`/scratch/users/<username>`](../filesystems/lustre.md)                                                    | [`${SCRATCH}`](../filesystems/lustre.md)                       | [Lustre](../filesystems/lustre.md)           | no                                   |
| `/mnt/isilon/projects/<project name>`                                                                      | -                                                              | [OneFS](../filesystems/isilon.md)            | yes (live sync and snapshots)        |

The  file system mounted on the home directories (`/home/users`) and project directories (`/work/projects`) are both exported by the [GPFS/Spectrumscale](../filesystems/gpfs.md) file system.

- Storage for both directories is redundant, so they are safe against hardware failure.
- Only `/home/users` is mirrored in a SSD cache, so `/home/users` is a significantly faster for random and small file I/O.
