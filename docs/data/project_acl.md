
!!! note "Global Project quotas and backup policies"
    See [quotas](quotas.md) for detailed information about inode,
    space quotas, and file system purge policies.
    Your global projects are daily backuped, according to the policy detailed in the [ULHPC backup policies](../data/backups.md).

<!--start-warning-clusterusers-->

!!! danger "Access rights to project directory: Quota for `clusterusers` group in project directories is 0 !!!"
    When a project `<name>` is created, a group of the same name (`<name>`) is also created and researchers allowed to collaborate on the project are made members of this group,which grant them access to the project directory.

    Be aware that your _default_ group as a user is `clusterusers` which has (_on purpose_) __a quota in project directories set to 0__.
    You thus need to ensure you always **write** data in your project directory using the `<name>` group (instead of yoru default one.).
    This can be achieved by ensuring the [setgid bit](https://en.wikipedia.org/wiki/Setuid) is set on all folders in the project directories: `chmod g+s [...]`

    When using `rsync` to transfer file toward the project directory `/work/projects/<name>` as destination, be aware that rsync will **not** use the correct permissions when copying files into your project directory. As indicated in the [Data transfer](data/transfer.md) section, you also need to:

    * give new files the destination-default permissions with `--no-p` (`--no-perms`), and
    * use the default group `<name>` of the destination dir with `--no-g` (`--no-group`)
    * (eventually) instruct rsync to preserve whatever executable permissions existed on the source file and aren't masked at the destination using `--chmod=ug=rwX`

    Your full `rsync` command becomes (adapt accordingly):

          rsync -avz {--update | --delete} --no-p --no-g [--chmod=ug=rwX] <source> /work/projects/<name>/[...]

<!--end-warning-clusterusers-->
