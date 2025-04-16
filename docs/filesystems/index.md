# Storage overview

The UL HPC clusters provide access to several different _File Systems (FS)_ which are configured for different purposes. There are the file systems _local_ to the compute nodes, and _cluster_ file systems accessible across the network. The available file systems can be seen in the following overview of the UL HPC cluster architecture.

![UL HPC cluster architecture](/images/ULHPC-simplified-workflow-overview.png)

??? info "What is a File System (FS)?"
    A _File System (FS)_ is just the logical manner to _store, organize & access_ data. There are different types of file systems available nowadays:

    - _Local FS_ you find on laptops and servers, such as `NTFS`, `HFS+`, `ext4`, `{x,z,btr}fs`, and other;
    - _Network FS_, such as `NFS`, `CIFS`/`SMB`, `AFP`, allowing to access a remote storage system as a NAS (Network Attached Storage);
    - [_Parallel and Distributed FS_ (_clustered FS_)](https://en.wikipedia.org/wiki/Clustered_file_system), such as `SpectrumScale/GPFS` or `Lustre`; those are file systems used in HPC and HTC (High Throughput Computing) facilities, such that
        - data is spread across multiple storage nodes for redundancy and performance, and
        - global capacity and performance are scalable and increase as additional nodes are added to the storage infrastructure.

In the UL HPC cluster nodes, there are 3 types of file system in use.

- Clustered file systems attached to cluster nodes through the fast [Infiniband network](/interconnect/ib/). These are,
    - a [GPFS](gpfs) file system storing home and project directories, and
    - a [Lustre](lustre) file system for storing scratch data.
- A networked file system attached to cluster nodes through the [Ethernet network](/interconnect/ethernet/). This is
    - an NFS export of an Isilon file system that stores directories.
- File systems local to the compute nodes. These are
    - `etx4` file systems mounted on `/tmp` of cluster nodes.

??? info "File systems not directly visible to users"

    The ULHPC team relies on other file systems within its internal backup infrastructure, such as [`xfs`](https://en.wikipedia.org/wiki/XFS), a high-performant disk file-system deployed on storage/backup servers.

## Storage Systems Overview

The following table summarize the mount location, backing up, and environment setup for each one of the network file systems in the cluster.

<!--file-system-table-start-->

!!! info "Cluster file systems"

    | Directory                                                                              | Environment variable                                                                   | File system                                                | Backup                                    | Interconnect |
    |----------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------|------------------------------------------------------------|-------------------------------------------|--------------|
    | [`/home/users/<username>`](../filesystems/gpfs#home-directory-home)                    | [`${HOME}`](../filesystems/gpfs#home-directory-home)                                   | [GPFS/Spectrumscale](../filesystems/gpfs.md)<sup>[1]</sup> | no                                        | Infiniband   |
    | [`/work/projects/<project name>`](../filesystems/gpfs#project-directories-projecthome) | [`${PROJECTHOME}/<project name>`](../filesystems/gpfs#project-directories-projecthome) | [GPFS/Spectrumscale](../filesystems/gpfs.md)<sup>[1]</sup> | yes (partial, only `backup` subdirectory) | Infiniband   |
    | [`/scratch/users/<username>`](../filesystems/lustre.md)                                | [`${SCRATCH}`](../filesystems/lustre.md)                                               | [Lustre](../filesystems/lustre.md)                         | no                                        | Infiniband   |
    | [`/mnt/isilon/projects/<project name>`](../filesystems/isilon.md)                      | -                                                                                          | [OneFS](../filesystems/isilon.md)                      | yes (and live sync<sup>[2]</sup>)         | Ehternet     |

    1. The  file system mounted on the home directories (`/home/users`) and project directories (`/work/projects`) are both exported by the [GPFS/Spectrumscale](../filesystems/gpfs.md) file system.

        - Storage for both directories is redundant, so they are safe against hardware failure.
        - Only `/home/users` is mirrored in a SSD cache, so `/home/users` is a significantly faster for random and small file I/O.

    2. Live sync replicates data across multiple OneFS instances for high availability.

<!--file-system-table-end-->

A local file system is also accessible through `/tmp`. The following table summarizes the type and capacity of the local storage drives.

!!! info "Local file systems"

    In cluster nodes there is a local file system mounted in `/tmp`. The file systems in the compute nodes are the following:

    | Cluster | Partition | Storage drive interface | Mount directory | File system | Size   |
    |---------|-----------|-------------------------|-----------------|-------------|--------|
    | Aion    | `batch`   | SATA                    | `/tmp`          | ext4        | 367 GB |
    | Iris    | `batch`   | SATA                    | `/tmp`          | ext4        | 73 GB  |
    | Iris    | `gpu`     | NVME                    | `/tmp`          | ext4        | 1.5 TB |
    | Iris    | `bigmem`  | NVME                    | `/tmp`          | ext4        | 1.4 TB |

    - Use the local file system mounted in `/tmp` for small file I/O. Cluster file systems can be slow when handling many small file I/O operations due to botlenecks in the metadata server bandwidth and latency.
    - In compute nodes, the contents of `/tmp` are whipped out after the completion of a job.

### Intended usage of file systems

Each file system in the cluster performs best in a specific set of functions.

- Use the GPFS file system directory mounted in your `${HOME}` for configuration files and files that need to be accessed with low latency and high throughput, for instance for storing environments and container sandboxes.
- Use the GPFS file system directories mounted in `${PROJECTHOME}` to store input and output files for your jobs.
- Use the Lustre file system directory mounted in `${SCRATCH}` to store working files for running jobs that need to be accessed with low latency and high throughput, like checkpoint files. Scratch is meant for temporary storage only; _remove files from scratch as soon as they are not needed for any running jobs_.
- Use project directories in the NFS and SMB exports of Isilon to archive data that need to be stored safely; the OneFS file system of Isilon is backed up regularly.
- Use the local file systems mounted in `/tmp` for small file I/O in running jobs, like compilations. Clustered file systems like GPFS and Lustre do not handle high throughput small file I/O well.

Many file system technologies (e.g. ZFS) can hide a lot of the complexity of using a file system. HPC clusters tend to provide low level access to file system functionality so that users can select the technology that provides the best performance for their workload.

### Clustered file systems

![](../images/plots/plot_piechart_storage_fs.png){: style="width:350px; float: right;"}

Current statistics of the available file systems are depicted on the side figure. The ULHPC facility relies on 2 types of [Distributed/Parallel File Systems](https://en.wikipedia.org/wiki/Clustered_file_system) to deliver high-performant Data storage at a BigData scale:

- [IBM Spectrum Scale](gpfs.md), formerly known as the General Parallel File System ([GPFS](gpfs.md)), a global _high_-performance clustered file system hosting your `${HOME}` and projects data mounted in `${PROJECTHOME}`.
- [Lustre](lustre.md), an open-source, parallel file system dedicated to large, parallel scratch storage mounted in `${SCRATCH}`

#### Home directory

{%
   include-markdown "../filesystems/gpfs.md"
   start="<!--home-mount-start-->"
   end="<!--home-mount-end-->"
%}

#### Project directories

{%
   include-markdown "../filesystems/gpfs.md"
   start="<!--projecthome-mount-start-->"
   end="<!--projecthome-mount-end-->"
%}

#### Scratch directory

{%
   include-markdown "../filesystems/lustre.md"
   start="<!--scratch-mount-start-->"
   end="<!--scratch-mount-end-->"
%}

### Networked file systems

The HPC systems also provide direct access through mount points on cluster nodes to the central data storage of the university. The central data storage uses a [Dell/EMC Isilon](isilon.md) system for the safe archiving of data. Clustered file systems are not meant for the long term storage of data. If you want your data backed up, move your data to the central data storage.

#### Cold project data and archives

{%
  include-markdown "../filesystems/isilon.md"
  start="<!--isilon-start-->"
  end="<!--isilon-end-->"
%}

## Quota

The UL HPC systems provide the `df-ulhpc` command on the cluster login nodes to display the current space and inode (with the option flag `-i`) quota usage. For more details see the documentation section about [quotas](/filesystems/quotas).

{%
   include-markdown "../filesystems/quotas.md"
   start="<!--overview-start-->"
   end="<!--overview-end-->"
%}

## Backups

{%
   include-markdown "../data/backups.md"
   start="<!--backup-intro-start-->"
   end="<!--backup-intro-end-->"
%}

More details and information on how to recover your backed up data can be found in the section of the documentation about [backups](/data/backups/).

### UL HPC clustered file systems

{%
   include-markdown "../data/backups.md"
   start="<!--backup-ulhpc-start-->"
   end="<!--backup-ulhpc-end-->"
%}

### Isilon networked file system

{%
   include-markdown "../data/backups.md"
   start="<!--backup-isilon-start-->"
   end="<!--backup-isilon-end-->"
%}

## Useful resources

- [ULHPC backup policies](../data/backups.md)
- [Quotas](quotas.md)
- ULHPC [GPFS/SpectrumScale](gpfs.md) and [Lustre](lustre.md) filesystems
- UL [Isilon/OneFS](isilon.md) filesystems
