## ULHPC File Systems Overview

<!--content-start-->

Several _File Systems_ co-exist on the ULHPC facility and are configured for different purposes.
Each servers and computational resources has access to at least three different file systems with different levels of performance, permanence and available space summarized below

<!--table-start-->

| Directory                                                                                            | Env.                                                         | file system                                  | backup                               |
|------------------------------------------------------------------------------------------------------|--------------------------------------------------------------|----------------------------------------------|--------------------------------------|
| [`/home/users/<login>`](../filesystems/gpfs.md#global-home-directory-home)                           | [`$HOME`](../filesystems/gpfs.md#global-home-directory-home) | [GPFS/Spectrumscale](../filesystems/gpfs.md) | no                                   |
| [`/work/projects/`](../filesystems/gpfs.md#global-project-directory-projecthomeworkprojects)`<name>` | -                                                            | [GPFS/Spectrumscale](../filesystems/gpfs.md) | yes (partial, `backup` subdirectory) |
| [`/scratch/users/<login>`](../filesystems/lustre.md)                                                 | [`$SCRATCH`](../filesystems/lustre.md)                       | [Lustre](../filesystems/lustre.md)           | no                                   |
| `/mnt/isilon/projects/<name>`                                                                        | -                                                            | [OneFS](../filesystems/isilon.md)            | yes (live sync and snapshots)        |
