# Backups

!!! danger
	All ULHPC users should back up important files on
    a regular basis.  **Ultimately, it is your responsibility to
    protect yourself from data loss.**

ULHPC has 3 different backup targets, with different rotation policies and physical locations.

The backups are only accessible by HPC staff, for disaster recovery purposes.

More precisions can be requested via a support request.

## User directories on the ULHPC clusters

| Directory        | Path           | Backup location | Frequency | Retention                                                    |
|------------------|----------------|-----------------|-----------|--------------------------------------------------------------|
| home directories | `$HOME`        | CDC, Belval     | Weekly    | last 7 backups, at least one per month for the last 2 months |
| projects         | `$PROJECTWORK` | CDC, Belval     | Weekly    | one backup per week of the backup directory (`$PROJECT/backup/`) |
| scratch          | `$SCRATCH`     | not backed up   |           |                                                              |


## Isilon project directories snapshots

Projects stored on the Isilon filesystem are *snapshotted* weekly, the snapshots are kept for 10 days.

!!! danger
    Snapshots are **not a real backup**. It does not protect you against a system failure, it will only permit to recover some files in case of accidental deletion


Each project directory, in `/mnt/isilon/projects/` contains a hidden sub-directory `.snapshot`:

* `.snapshot` is invisible to `ls`, `ls -a`, `find` and similar
  commands
* can be browsed normally after `cd .snapshot`
* files cannot be created, deleted or edited in snapshots
* files can *only* be copied *out* of a snapshot


## Virtual machines

| Source                 | Backup location | Frequency | Retention                                          |
|------------------------|-----------------|-----------|----------------------------------------------------|
| Gitlab infrastructure  | CS43, Kirchberg | Weekly    | last 5 weekly snapshots                            |
| Iris infrastructure    | CDC, Belval     | Weekly    | last 5 weekly snapshots                            |


## Services

| Name                         | Backup location | Frequency | Retention                                                 |
|------------------------------|-----------------|-----------|-----------------------------------------------------------|
| gitlab.uni.lu                | CDC, Belval     | Daily     | last 7 daily backups, one per month for the last 6 months |
| hpc-nextcloud.uni.lu         | CDC, Belval     | Daily     | last 7 daily backups, one per month for the last 6 months |
| hpc.uni.lu (pad, privatebin) | CDC, Belval     | Daily     | last 7 daily backups, one per month for the last 6 months |


## Restore

If you require a restoration of lost data that cannot be accomplished via the
snapshots capability, please create a new request on [Service Now portal](https://hpc.uni.lu/support),
with pathnames and timestamps of the missing data.

Such restore requests may take a few days to complete.

## Purging

!!! note
    See [Filesystem Quotas and Purging](../filesystems/quotas.md) for detailed information about inode,
    space quotas, and file system purge policies.

!!! warning
	`$SCRATCH` directories are **not** backed up


## Backup Tools

In practice, the ULHPC backup infrastructure is fully puppetized and make use of several tools facilitating the operations:

* [backupninja](https://0xacab.org/riseuplabs/backupninja), which allows you to coordinate system backup by dropping a few simple configuration files into `/etc/backup.d/`
* a forked version of [bontmia](https://github.com/hcartiaux/bontmia), which stands for "Backup Over Network To Multiple Incremental Archives"
* [BorgBackup](https://borgbackup.readthedocs.io/en/stable/), a deduplicating backup program supporting compression and authenticated encryption.
* several internal scripts to pilot LVM snapshots/backup/restore operations
