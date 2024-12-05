## Home directory (`${HOME}`)

Home directories provide a convenient means for a user to have access to files such as dotfiles, source files, input files, configuration files regardless of the platform.

Use your home directory to store working data, that are actively accessed by multiple processes in your computations. Home directories are cached, so small files and random I/O is relatively fast but not as fast as local storage. The file system is redundant so it is safe to data and access loss due to hardware failure. _Redundancy does not replace backups, so do not leave your data stored in your home._

Refer to your home directory using the environment variable `${HOME}` whenever possible. The absolute path may change, but the value of `${HOME}` will always be correct.

<!--intro-end-->
