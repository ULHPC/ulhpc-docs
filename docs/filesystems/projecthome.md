## Project directories `(${PROJECTHOME})`

Project directories are intended for sharing data within a group of researchers, and are stored under the path `/work/projects/<project name>`. Project directories are also accessible from every node in the cluster.

Use project directories to store input and output data for your jobs. Data can be accessed by multiple processes in your computation. Project directories are not cached so small file I/O performance is lower that the home directory. The file system is redundant so it is safe to data and access loss due to hardware failure. _Redundancy does not replace backups, so do not leave your data stored in your project directories._

The parent directory of all project directories (`/work/projects`) can be referenced using the environment variable `${PROJECTHOME}`. Use `${PROJECTHOME}` whenever possible as it is guaranteed to point to the parent directory of all project directories.

<!--intro-end-->
