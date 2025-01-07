## Scratch directory `(${SCRATCH})`

The _scratch_ area is a [Lustre](http://lustre.org/)-based file system designed for high performance temporary storage of large files.

The scratch is used to write large files in a continuous manner. The term originates from [scratch data tapes](https://en.wikipedia.org/wiki/Scratch_tape). People uses scratch tapes to write and read data that did not fit into the main memory, and since it was a tape, it could only perform continuous I/O. The term scratch is a bit abused in modern times as most storage systems nowadays support random access. In the case of the UL HPC scratch however, we use the term literally. Our file system in scratch has a very bad performance in small file and random reads and writes.

_If you cannot guarantee that your computations will read and write the data in a continuous manner and in large files then do not use the scratch._

The scratch is intended to support large file continuous I/O for jobs that are being actively computed on the UL HPC systems. If you are sure about the data access pattern of your job, the we recommend that you run the I/O of your jobs, especially data intensive ones, from the UL HPC scratch file system.

The file system is redundant so it is safe to data and access loss due to hardware failure. _Redundancy does not replace backups, so do not leave your data stored in your scratch directory._

Refer to your scratch directory using the environment variable `${SCRATCH}` whenever possible (which expands to `/scratch/users/$(whoami)`). The scratch file system is shared via the Infiniband network of the ULHPC facility and is available from all nodes while being tuned for high performance.

<!--intro-end-->
