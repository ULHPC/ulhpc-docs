# Backups

!!! danger
	All ULHPC users should back up important files on
    a regular basis.  **Ultimately, it is your responsibility to
    protect yourself from data loss.**

The backups are only accessible by HPC staff, for disaster recovery purposes only.

More precisions can be requested via a support request.

## Directories on the ULHPC clusters infrastructure

For computation purposes, ULHPC users can use multiple storages: home, scratch and projects. Note however that the HPC Platform does not have the infrastructure to backup all of them, see details below.

| Directory        | Path           | Backup location | Frequency | Retention                                                    |
|------------------|----------------|-----------------|-----------|--------------------------------------------------------------|
| home directories | `$HOME`        | not backed up     |     |
| scratch          | `$SCRATCH`     | not backed up   |           |                                                              |
| projects         | `$PROJECTWORK` | CDC, Belval     | Weekly    | one backup per week of the backup directory ONLY (`$PROJECT/backup/`) |


## Directories on the SIU Isilon infrastructure

Projects stored on the Isilon filesystem are *snapshotted* weekly, the snapshots are kept for 10 days.

!!! danger
    Snapshots are **not a real backup**. It does not protect you against a system failure, it will only permit to recover some files in case of accidental deletion

Each project directory, in `/mnt/isilon/projects/` contains a hidden sub-directory `.snapshot`:

* `.snapshot` is invisible to `ls`, `ls -a`, `find` and similar
  commands
* can be browsed normally after `cd .snapshot`
* files cannot be created, deleted or edited in snapshots
* files can *only* be copied *out* of a snapshot


## Services

| Name                         | Backup location | Frequency | Retention                                                 |
|------------------------------|-----------------|-----------|-----------------------------------------------------------|
| hpc.uni.lu (pad, privatebin) | CDC, Belval     | Daily     | last 7 daily backups, one per month for the last 6 months |


## Restore

If you require a restoration of lost data that cannot be accomplished via the
snapshots capability, please create a new request on [Service Now portal](https://hpc.uni.lu/support),
with pathnames and timestamps of the missing data.

Such restore requests may take a few days to complete.

## Backup Tools

In practice, the ULHPC backup infrastructure is fully puppetized and make use of several tools facilitating the operations:

* [backupninja](https://0xacab.org/riseuplabs/backupninja), which allows you to coordinate system backup by dropping a few simple configuration files into `/etc/backup.d/`
* a forked version of [bontmia](https://github.com/hcartiaux/bontmia), which stands for "Backup Over Network To Multiple Incremental Archives"
* [BorgBackup](https://borgbackup.readthedocs.io/en/stable/), a deduplicating backup program supporting compression and authenticated encryption.
* several internal scripts to pilot LVM snapshots/backup/restore operations
