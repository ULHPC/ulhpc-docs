## ULHPC File system overview

<!--content-start-->

Several _File Systems_ co-exist on the ULHPC facility and are configured for different purposes. Each server and computational resources has access to at least three different file systems with different levels of performance, permanence, and available space as summarized in the following table.

<!--table-start-->

| Directory                                                                                                  | Environment variable                                           | File system                                  | Backup                               |
|------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------|----------------------------------------------|--------------------------------------|
| [`/home/users/<username>`](../filesystems/gpfs.md#global-home-directory-home)                              | [`${HOME}`](../filesystems/gpfs.md#global-home-directory-home) | [GPFS/Spectrumscale](../filesystems/gpfs.md) | no                                   |
| [`/work/projects/<project name>`](../filesystems/gpfs.md#global-project-directory-projecthomeworkprojects) | -                                                              | [GPFS/Spectrumscale](../filesystems/gpfs.md) | yes (partial, `backup` subdirectory) |
| [`/scratch/users/<username>`](../filesystems/lustre.md)                                                    | [`${SCRATCH}`](../filesystems/lustre.md)                       | [Lustre](../filesystems/lustre.md)           | no                                   |
| `/mnt/isilon/projects/<project name>`                                                                      | -                                                              | [OneFS](../filesystems/isilon.md)            | yes (live sync and snapshots)        |

