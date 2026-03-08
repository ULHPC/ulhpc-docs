# Backups

<!--backup-intro-start-->

Backups are vital to safeguard important data. Always maintain a well defined backup policy. You can build your backup policy on top of the backup services offered in the UL HPC systems. A high level overview of the backup policies in place for the HPC systems is presented here. If you require specific details, please contact the HPC team directly.

!!! danger "Limitations of backup policies in UL"

    The UL HPC and SIU do not offer cold backups (offline backups). All our backups are maintained in live systems.

    All UL HPC users should back up important files on a regular basis. **Ultimately, it is your responsibility to protect yourself from data loss.**

<!--backup-intro-end-->

## Directories on the UL HPC clusters infrastructure

There are multiple [cluster file systems](/filesystems/#clustered-file-systems) used in UL HPC clusters to support computation jobs. These file systems are accessible through [home](/filesystems/#home-directory), [project](/filesystems/#project-directories), and [scratch](/filesystems/#scratch-directory) directories.

<!--backup-ulhpc-start-->

The cluster file systems are not meant to be used for data storage, so there are minimal back ups created for files in the cluster file systems. The backups are only accessible by UL HPC staff for disaster recovery purposes only. The following table summarizes the backups kept for each file system mount point.

| Directory        | Path             | Backup location | Frequency | Retention                                                                                   |
|------------------|------------------|-----------------|-----------|---------------------------------------------------------------------------------------------|
| home directories | `${HOME}`        | not backed up   | -         |                                                                                             |
| scratch          | `${SCRATCH}`     | not backed up   | -         |                                                                                             |
| projects         | `${PROJECTHOME}` | CDC, Belval     | Weekly    | One backup per week of the backup directory ONLY (`${PROJECTHOME}/<project name>/backup/`). |

!!! tip "Project backups"

    Use the `backup` subdirectory in your project directories to store important configuration files for you projects that are specific to the UL HPC clusters.

!!! info "UL HPC backup policy"

    Data are copied live from the GPFS file system to a backup server (due to limitation regarding snapshots in GPFS). The backup data are copied to a Disaster Recovery Site (DRS) in a location outside the server room where the primary backup server is located.

<!--backup-ulhpc-end-->

## Directories on the SIU Isilon infrastructure

<!--backup-isilon-start-->

Projects stored on the [Isilon system](/filesystems/isilon) are snapshotted regularly. This includes the NFS export of Isilon in HL HPC systems, personal and project directories in Atlas, the SMB export of Isilon, but not the personal directories of the students exported through the Poseidon SMB export of Isilon. The following snapshot schedule and retention strategy are used:

!!! info "SIU back up policy"
    | Backed up snapshot | Retention |
    |--------------------|-----------|
    | Daily              | 14 days   |
    | Weekly             | 5 months  |
    | Monthly            | 12 months |

### Snapshots of directories in Isilon

Users can access some snapshoted data through the snapshots of the Isilon file systems. This can help restore data after incidents such as accidental data deletion. Each project directory, in `/mnt/isilon/projects/` contains a hidden sub-directory called `.snapshot`.

- The `.snapshot` directory is invisible to `ls`, but also to `ls -a`, `find` and similar commands.
- Snapshots can be browsed normally after changing into the snapshot directory (`cd .snapshot`).
- Files cannot be created, deleted, or edited in snapshots; files _can only be copied out_ of a snapshot.
- Only a few, strategically selected snapshots are exposed to the users. See the [section on backup restoration](#restore) on how to access other snapshots if you need them.

### Backup of directories in Isilon

Isilon backups your data automatically, by copying snapshot data to storage in a Disaster Recovery Site (DRS) in a location outside the server room where the primary data storage (Isilon) is located. In case of system failure, the latest snapshot in the DRS storage system will be used to restore your data.

??? info "Backup and snapshot relation"
    Snapshots are not backups as they do not protect against a total system failure, they only permit recovering files in case of accidental deletion. Proper backup storage requires that the data are redundant and highly available with respect to a whole system failure (the whole of Isilon system failing). Snapshots provide a frozen version of the data that is then replicated in the DRS system to guard against whole system failure.

The Isilon system provides backup storage by copying snapshot data to the DRS system. Backup policies impose specific restrictions on the frequency of snapshot, number of copies, and storage types used, like requirements to maintain a copy of your data in an offline system. If the policy of your project imposes any requirements that are stricter than the SIU policy, you will have to provide your own backup solution.

<!--backup-isilon-end-->

## Restore

If you require the restoration of lost data, please create a new request on [Service Now portal](https://hpc.uni.lu/support), with pathnames and timestamps of the missing data.

Such restore requests may take a few days to complete and are not guaranteed.

## Backup Tools

In practice, the ULHPC backup infrastructure is fully puppetized and make use of several tools facilitating the operations:

- [backupninja](https://0xacab.org/riseuplabs/backupninja), which allows you to coordinate system backup by dropping a few simple configuration files into `/etc/backup.d/`;
- a forked version of [bontmia](https://github.com/hcartiaux/bontmia), which stands for "Backup Over Network To Multiple Incremental Archives";
- [BorgBackup](https://borgbackup.readthedocs.io/en/stable/), a deduplicating backup program supporting compression and authenticated encryption;
- several internal scripts to pilot LVM snapshots/backup/restore operations.
