Your journey on the ULHPC facility is illustrated in the below figure.

![](/images/ULHPC-simplified-workflow-overview.png)

In particular, once connected, you have access to several different _File Systems (FS)_ which are configured for different purposes.

??? info "What is a File System (FS) ?"
    A _File System (FS)_ is just the logical manner to _store, organize & access_ data.
    There are different types of file systems available nowadays:

    - (local) _Disk FS_ you find on laptops and servers: `FAT32`, `NTFS`, `HFS+`, `ext4`, `{x,z,btr}fs`...
    - _Networked FS_, such as `NFS`, `CIFS`/`SMB`, `AFP`, allowing to access a remote storage system as a NAS (Network Attached Storage)
    - _Parallel and Distributed FS_: such as `SpectrumScale/GPFS` or `Lustre`. Those are typical FileSystems you meet on HPC or HTC (High Throughput Computing) facility as they exhibit several unique capabilities:
        * data is spread across multiple storage nodes for redundancy and performance.
        * the global capacity **AND** the global performances are increased with every systems added to the storage infrastructure.

## Storage Systems Overview

![](../images/plots/plot_piechart_storage_fs_2020.png){: style="width:350px; float: right;"}

Current statistics of the available filesystems are depicted on the side figure.
The ULHPC facility relies on **2** types of [Distributed/Parallel File Systems](https://en.wikipedia.org/wiki/Clustered_file_system) to deliver high-performant Data storage at a BigData scale:

* [IBM Spectrum Scale](gpfs.md), formerly known as the General Parallel File System ([GPFS](gpfs.md)), a global _high_-performance clustered file system hosting your `$HOME` and projects data.
* [Lustre](lustre.md), an open-source, parallel file system dedicated to large, local, parallel **scratch** storage.

In addition, the following file-systems complete the ULHPC storage infrastructure:

* OneFS, A global _low_-performance [Dell/EMC Isilon](isilon.md) solution used to host project data, and serve for backup and archival purposes
* The ULHPC team relies on other filesystems within its internal backup infrastructure, such as [`xfs`](https://en.wikipedia.org/wiki/XFS), a high-performant disk file-system deployed on storage/backup servers.

## Summary

File systems are configured for different purposes.
Each machine has access to at least three different file systems with different levels of performance, permanence and available space.

| Directory                     | Env.       | file system                   | backup | purging |
|-------------------------------|------------|-------------------------------|--------|---------|
| `/home/users/<login>`         | `$HOME`    | [GPFS/Spectrumscale](gpfs.md) | yes    | no      |
| `/scratch/users/<login>`      | `$SCRATCH` | [Lustre](lustre.md)           | no     | yes     |
| `/work/projects/<name>`       | -          | [GPFS/Spectrumscale](gpfs.md) | yes    | no      |
| `/scratch/projects/<name>`    | -          | [Lustre](lustre.md)           | no     | yes     |
| `/mnt/isilon/projects/<name>` | -          | [OneFS](isilon.md)            | yes*   | no      |

* [ULHPC backup policies](../data/backups.md)
* [Quotas and purging policies](quotas.md)
* ULHPC [GPFS/SpectrumScale](gpfs.md) and [Lustre](lustre.md) filesystems
