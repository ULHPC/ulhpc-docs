# Quotas and Purging

## Overview

| Directory    | Default space quota | Default inode quota | Purge time |
| ---------------------- | ------------------- | ------------------- | ---------- |
| `$HOME`                | 500 GB              | 1 M                 | -          |
| `$SCRATCH`             | 10 TB               | 1 M                 | 60 days    |
| `/work/projects/...`   | 16 MB               | 0                   | -          |
| `/mnt/isilon/projects/...` | 1.14 PB globally | -                   | -          |

## Quotas

!!! warning
	When a quota is reached writes to that directory will fail.

!!! note
	On Isilon everyone shares one global quota. Unfortunately it is not possible to see the quota status on the cluster.

### Current usage

We provide the `df-ulhpc` command on the cluster login nodes, which displays current usage, soft quota, hard quota and grace period. Any directories that have exceeded the quota will be highlighted in red.

Once you reach the soft quota you can still write data until the grace period expires (7 days) or you reach the hard quota. After you reach the end of the grace period or the hard quota, you have to reduce your usage to below the soft quota to be able to write data again.

Check current space quota status:

```
df-ulhpc
```

Check current inode quota status:

```
df-ulhpc -i
```

Check free space on all file systems:

```
df -h
```

Check free space on current file system:

```
df -h .
```

### Increases

If you or your project needs additional space or inodes for your scratch or project directory you may request it via [ServiceNow](https://hpc.uni.lu/support/) (HPC &rarr; Storage & projects &rarr; Extend quota).

Quotas on the home directory cannot be increased.

### Troubleshooting

The quotas on project directories are based on the group. Be aware that the quota for the default user group `clusterusers` is 0. If you get a quota error, but `df-ulhpc` and `df-ulhpc -i` confirm that the quota is not expired, you are most likely trying to write a file with the group `clusterusers` instead of the project group.

To avoid this issue, check out the `newgrp` command or set the `s` mode bit ("set group ID") on the directory with `chmod g+s <directory>`. The `s` bit means that any file or folder created below will inherit the group.

To transfer data with `rsync` into a project directory, please check the [data transfer documentation](/data/transfer/#transfer-from-your-local-machine-to-a-project-directory-on-the-remote-cluster).

## Purging
Files in the scratch (`$SCRATCH`, `/mnt/lscratch`) directories are purged. This means **files that have not been read** (i.e. atime has not been updated) **within the last 60 days are automatically removed every month**.

Files in `/tmp` on the compute nodes are **removed** at the end of the job.
