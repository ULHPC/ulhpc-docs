## Global Scratch directory `$SCRATCH`

The _scratch_ area is a [Lustre](http://lustre.org/)-based file system designed for high performance temporary storage of large files.

It is thus intended to support large I/O for jobs that are being actively computed on the ULHPC systems.
We recommend that you run your jobs, especially data intensive ones, from the ULHPC scratch file system.

Refer to your scratch directory using the environment variable `$SCRATCH` whenever possible (which expands to `/scratch/users/$(whoami)`).
The scratch file system is shared via the Infiniband network of the ULHPC facility and is available from all nodes while being tuned for high performance.

<!--intro-end-->
