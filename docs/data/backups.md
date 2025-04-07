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

| Backed up snapshot | Retention |
|--------------------|-----------|
| Daily              | 14 days   |
| Weekly             | 5 months  |
| Monthly            | 12 months |

!!! info "SIU back up policy"

    Snapshots do not protect on themselves against a system failure, they only permit recovering files in case of accidental deletion. To ensure the safe storage, snapshots data is copied to a Disaster Recovery Site (DRS) in a location outside the server room where the primary data storage (Isilon) is located.

<!--backup-isilon-end-->

Users can access some backed up data through the snapshots in Isilon file systems. This can help restoration after incidents such as accidental data deletion. Each project directory, in `/mnt/isilon/projects/` contains a hidden sub-directory `.snapshot`. 

- The `.snapshot` directory is invisible to `ls`, but also to `ls -a`, `find` and similar commands.
- Snapshots can be browsed normally after changing into the snapshot directory (`cd .snapshot`).
- Files cannot be created, deleted, or edited in snapshots; files can *only* be copied *out* of a snapshot.
- Only a few, strategically selected snapshots are exposed to the users. See the [section on backup restoration](#restore) on how to access other snapshots if you need them.

## Data of services

| Name                         | Backup location | Frequency | Retention                                                 |
|------------------------------|-----------------|-----------|-----------------------------------------------------------|
| hpc.uni.lu (pad, privatebin) | CDC, Belval     | Daily     | last 7 daily backups, one per month for the last 6 months |


## Restore

If you require the restoration of lost data in Isilon that cannot be accomplished via the snapshots capability, please create a new request on [Service Now portal](https://hpc.uni.lu/support), with pathnames and timestamps of the missing data. Create a new request for all data stored in the `backup` directory of projects in the clustered file systems.

Such restore requests may take a few days to complete.

## Backup Tools

In practice, the ULHPC backup infrastructure is fully puppetized and make use of several tools facilitating the operations:

- [backupninja](https://0xacab.org/riseuplabs/backupninja), which allows you to coordinate system backup by dropping a few simple configuration files into `/etc/backup.d/`;
- a forked version of [bontmia](https://github.com/hcartiaux/bontmia), which stands for "Backup Over Network To Multiple Incremental Archives";
- [BorgBackup](https://borgbackup.readthedocs.io/en/stable/), a deduplicating backup program supporting compression and authenticated encryption;
- several internal scripts to pilot LVM snapshots/backup/restore operations.
