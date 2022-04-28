### Understanding Lustre I/O

When a client (a compute node from your job) needs to create or access a file, the client queries the metadata server (MDS) and the metadata target (MDT) for the layout and location of the file's stripes. Once the file is opened and the client obtains the striping information, the MDS is no longer involved in the file I/O process. The client interacts directly with the object storage servers (OSSes) and OSTs to perform I/O operations such as locking, disk allocation, storage, and retrieval.

If multiple clients try to read and write the same part of a file at the same time, the Lustre distributed lock manager enforces coherency, so that all clients see consistent results.

### Discover MDTs and OSTs

ULHPC's Lustre file systems look and act like a single logical storage, but a large files on Lustre can be divided into multiple chunks (**stripes**) and stored across over OSTs.
This technique is called [**file striping**](https://en.wikipedia.org/wiki/Data_striping).
The stripes are distributed among the OSTs in a round-robin fashion to ensure load balancing.
It is thus important to know the number of OST on your running system.

As mentioned in the [Lustre implementation section](lustre.md#storage-system-implementation), the ULHPC Lustre infrastructure is composed of 2 MDS servers (2 MDT), 2 OSS servers and **16 OSTs**.
You can list the MDTs and OSTs with the command `lfs df`:

```bash
$ cds      # OR: cd $SCRATCH
$ lfs df -h
UUID                       bytes        Used   Available Use% Mounted on
lscratch-MDT0000_UUID        3.2T       15.4G        3.1T   1% /mnt/lscratch[MDT:0]
lscratch-MDT0001_UUID        3.2T        3.8G        3.2T   1% /mnt/lscratch[MDT:1]
lscratch-OST0000_UUID       57.4T       16.7T       40.2T  30% /mnt/lscratch[OST:0]
lscratch-OST0001_UUID       57.4T       18.8T       38.0T  34% /mnt/lscratch[OST:1]
lscratch-OST0002_UUID       57.4T       17.6T       39.3T  31% /mnt/lscratch[OST:2]
lscratch-OST0003_UUID       57.4T       16.6T       40.3T  30% /mnt/lscratch[OST:3]
lscratch-OST0004_UUID       57.4T       16.5T       40.3T  30% /mnt/lscratch[OST:4]
lscratch-OST0005_UUID       57.4T       16.5T       40.3T  30% /mnt/lscratch[OST:5]
lscratch-OST0006_UUID       57.4T       16.3T       40.6T  29% /mnt/lscratch[OST:6]
lscratch-OST0007_UUID       57.4T       17.0T       39.9T  30% /mnt/lscratch[OST:7]
lscratch-OST0008_UUID       57.4T       16.8T       40.0T  30% /mnt/lscratch[OST:8]
lscratch-OST0009_UUID       57.4T       13.2T       43.6T  24% /mnt/lscratch[OST:9]
lscratch-OST000a_UUID       57.4T       13.2T       43.7T  24% /mnt/lscratch[OST:10]
lscratch-OST000b_UUID       57.4T       13.3T       43.6T  24% /mnt/lscratch[OST:11]
lscratch-OST000c_UUID       57.4T       14.0T       42.8T  25% /mnt/lscratch[OST:12]
lscratch-OST000d_UUID       57.4T       13.9T       43.0T  25% /mnt/lscratch[OST:13]
lscratch-OST000e_UUID       57.4T       14.4T       42.5T  26% /mnt/lscratch[OST:14]
lscratch-OST000f_UUID       57.4T       12.9T       43.9T  23% /mnt/lscratch[OST:15]

filesystem_summary:       919.0T      247.8T      662.0T  28% /mnt/lscratch
```


### File striping

**[File striping](https://en.wikipedia.org/wiki/Data_striping)** permits to increase the throughput of operations by taking advantage of several OSSs and OSTs, by allowing one or more clients to read/write different parts of the same file in parallel. On the other hand, striping small files can decrease the performance.

File striping allows file sizes larger than a single OST, large files **MUST** be striped over several OSTs in order to avoid filling a single OST and harming the performance for all users.
There is default stripe configuration for ULHPC Lustre filesystems (see below).
However, users can set the following stripe parameters for their own directories or files to get optimum I/O performance.
You can tune file striping using 3 properties:

| Property          | Effect                                                           | Default            | Accepted values                     | Advised values |
|-------------------|------------------------------------------------------------------|--------------------|-------------------------------------|----------------|
| **stripe_size**   | Size of the file stripes in bytes                                | **1048576** (1m)   | > 0                                 | > 0            |
| **stripe_count**  | Number of OST to stripe across                                   | **1**              | **-1** (use all the OSTs), **1-16** | -1             |
| **stripe_offset** | Index of the OST where the first stripe of files will be written | **-1** (automatic) | **-1**, **0-15**                    | -1             |

_Note_: With regards `stripe_offset` (the index of the OST where the first stripe is to be placed); the default is -1 which results in random selection and **using a non-default value is NOT recommended**.

!!! note
    Setting stripe size and stripe count correctly for your needs may significantly affect the I/O performance.

* Use the `lfs getstripe` command for getting the stripe parameters.
* Use `lfs setstripe` for setting the stripe parameters to get optimal I/O performance. The correct stripe setting depends on your needs and file access patterns.
    - Newly created files and directories will inherit these parameters from their parent directory. However, the parameters cannot be changed on an existing file.


```console
$ lfs getstripe dir|filename
$ lfs setstripe -s <stripe_size> -c <stripe_count> -o <stripe_offset> dir|filename
    usage: lfs setstripe -d <directory>   (to delete default striping from an existing directory)
    usage: lfs setstripe [--stripe-count|-c <stripe_count>]
                         [--stripe-index|-i <start_ost_idx>]
                         [--stripe-size|-S <stripe_size>]  <directory|filename>
```

Example:

```console
$ lfs getstripe $SCRATCH
/scratch/users/<login>/
stripe_count:   1 stripe_size:    1048576 stripe_offset:  -1
[...]
$ lfs setstripe -c -1 $SCRATCH
$ lfs getstripe $SCRATCH
/scratch/users/<login>/
stripe_count:  -1 stripe_size:   1048576 pattern:       raid0 stripe_offset: -1
```

In this example, we view the current stripe setting of the `$SCRATCH` directory. The stripe count is changed to all OSTs and verified.
All files written to this directory will be striped over the maximum number of OSTs (16).
Use `lfs check osts` to see the number and status of active OSTs for each filesystem on the cluster. Learn more by reading the man page:

```console
$ lfs check osts
$ man lfs
```

### File stripping Examples

* Set the striping parameters for a directory containing only small files (< 20MB)

```console
$ cd $SCRATCH
$ mkdir test_small_files
$ lfs getstripe test_small_files
test_small_files
stripe_count:   1 stripe_size:    1048576 stripe_offset:  -1 pool:
$ lfs setstripe --stripe-size 1M --stripe-count 1 test_small_files
$ lfs getstripe test_small_files
test_small_files
stripe_count:   1 stripe_size:    1048576 stripe_offset:  -1
```

* Set the striping parameters for a directory containing only large files between 100MB and 1GB

```console
$ mkdir test_large_files
$ lfs setstripe --stripe-size 2M --stripe-count 2 test_large_files
$ lfs getstripe test_large_files
test_large_files
stripe_count:   2 stripe_size:    2097152 stripe_offset:  -1
```

* Set the striping parameters for a directory containing files larger than 1GB

```console
$ mkdir test_larger_files
$ lfs setstripe --stripe-size 4M --stripe-count 6 test_larger_files
$ lfs getstripe test_larger_files
test_larger_files
stripe_count:   6 stripe_size:    4194304 stripe_offset:  -1
```

!!! Hint "Big Data files management on Lustre"
    Using a large stripe size can improve performance when accessing very large files

Large stripe size allows each client to have exclusive access to its own part of a file. However, it can be counterproductive in some cases if it does not match your I/O pattern. The choice of stripe size has no effect on a single-stripe file.


Note that these are simple examples, the optimal settings defer depending on the application (concurrent threads accessing the same file, size of each write operation, etc).

## Lustre Best practices

!!! hint "Parallel I/O on the same file"
    Increase the `stripe_count` for parallel I/O to the same file.

When multiple processes are writing blocks of data to the same file in parallel, the I/O performance for large files will improve when the `stripe_count` is set to a larger value. The stripe count sets the number of OSTs to which the file will be written. By default, the stripe count is set to 1. While this default setting provides for efficient access of metadata (for example to support the `ls -l` command), large files should use stripe counts of greater than 1. This will increase the aggregate I/O bandwidth by using multiple OSTs in parallel instead of just one. A rule of thumb is to use a stripe count approximately equal to the number of gigabytes in the file.

Another good practice is to make the stripe count be an integral factor of the number of processes performing the write in parallel, so that you achieve load balance among the OSTs. For example, set the stripe count to 16 instead of 15 when you have 64 processes performing the writes.
For more details, you can read the following external resources:

* [Reference Documentation:  Managing File Layout (Striping) and Free Space](https://doc.lustre.org/lustre_manual.xhtml#managingstripingfreespace)
* [Lustre Wiki](https://wiki.lustre.org/Main_Page)
* [Lustre Best Practices - Nasa HECC](http://www.nas.nasa.gov/hecc/support/kb/lustre-best-practices_226.html)
* [I/O and Lustre Usage - NISC](https://www.nics.tennessee.edu/computing-resources/file-systems/io-lustre-tips)
