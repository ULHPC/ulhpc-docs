
!!! note "Global Project quotas and backup policies"
    See [quotas](../filesystems/quotas.md) for detailed information about inode,
    space quotas, and file system purge policies.
    Your projects backup directories are backuped weekly, according to the policy detailed in the [ULHPC backup policies](../data/backups.md).

<!--start-warning-clusterusers-->

!!! danger "Access rights to project directory: Quota for `clusterusers` group in project directories is 0 !!!"
    When a project `<name>` is created, a group of the same name (`<name>`) is also created and researchers allowed to collaborate on the project are made members of this group,which grant them access to the project directory.

    Be aware that your _default_ group as a user is `clusterusers` which has (_on purpose_) __a quota in project directories set to 0__.
    You thus need to ensure you always **write** data in your project directory using the `<name>` group (instead of yoru default one.).
    This can be achieved by ensuring the [setgid bit](https://en.wikipedia.org/wiki/Setuid) is set on all folders in the project directories: `chmod g+s [...]`

    When using `rsync` to transfer file toward the project directory `/work/projects/<name>` as destination, be aware that rsync will **not** use the correct permissions when copying files into your project directory. As indicated in the [Data transfer](../data/transfer.md) section, you also need to:

    * give new files the destination-default permissions with `--no-p` (`--no-perms`), and
    * use the default group `<name>` of the destination dir with `--no-g` (`--no-group`)
    * (eventually) instruct rsync to preserve whatever executable permissions existed on the source file and aren't masked at the destination using `--chmod=ug=rwX`

    Your full `rsync` command becomes (adapt accordingly):

          rsync -avz {--update | --delete} --no-p --no-g [--chmod=ug=rwX] <source> /work/projects/<name>/[...]

For the same reason detailed above, in case you are using a build command or
more generally any command meant to _write_ data in your project directory
`/work/projects/<name>`, you want to use the
[`sg`](https://linux.die.net/man/1/sg) as follows:

```bash
# /!\ ADAPT <name> accordingly
sg <name> -c "<command> [...]"
```

This is particularly important if you are [building dedicated software with
Easybuild](../environment/easybuild.md) for members of the project - you typically want to do it as follows:

```bash
# /!\ ADAPT <name> accordingly
sg <name> -c "eb [...] -r --rebuild -D"   # Dry-run - enforce using the '<name>' group
sg <name> -c "eb [...] -r --rebuild"      # Dry-run - enforce using the '<name>' group
```



<!--end-warning-clusterusers-->
