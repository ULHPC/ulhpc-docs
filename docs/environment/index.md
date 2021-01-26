# ULHPC User Environment

Your journey on the ULHPC facility is illustrated in the below figure.

![](../images/ULHPC-simplified-workflow-overview.png)

## Home and Directories Layout

All ULHPC systems use [global home directories](../filesystems/gpfs.md#global-home-directory-home).
You also have access to several other pre-defined directories setup over several different _File Systems_ which co-exist on the ULHPC facility and are configured for different purposes. They are listed below:

{%
   include-markdown "../filesystems/overview.md"
   start="<!--table-start-->"
%}

## Shell and Dotfiles

The default login shell is `bash` -- see `/etc/shells` for supported shells.

!!! warning "ULHPC dotfiles vs. default dotfiles"
    The ULHPC team **DOES NOT** populate shell initialization files (also known as dotfiles) on users' home directories - the default _system_ ones are used in your home -- you can check them in `/etc/skel/.*` on the [access/login servers](../connect/access.md).
    However, you **may want** to install the [`ULHPC/dotfiles`](https://github.com/ULHPC/dotfiles) available as a [Github repository](https://github.com/ULHPC/dotfiles). See [installation notes](https://github.com/ULHPC/dotfiles#installation).
    A working copy of that repository exists in `/etc/dotfiles.d` on the [access/login servers](../connect/access.md). You can thus use it:
    ```bash
    $ /etc/dotfiles.d/install.sh -h
    # Example to install ULHPC GNU screen configuration file
    $ /etc/dotfiles.d/install.sh -d /etc/dotfiles.d/ --screen -n   # Dry-run
    $ /etc/dotfiles.d/install.sh -d /etc/dotfiles.d/ --screen      # real install
    ```

??? info "Changing Default Login Shell (or NOT)"
    If you want to change your your default login shell, you should set that up using the [ULHPC IPA portal](../connect/ipa.md) (change the Login Shell attribute).
    Note **however that we STRONGLY discourage you to do so.** You may hit unexpected issues with system profile scripts expecting `bash` as running shell.

### System Profile

`/etc/profile` contains Linux system wide environment and startup programs.
Specific scripts are set to improve your ULHPC experience, in particular those set in the [`ULHPC/tools`](https://github.com/ULHPC/tools) repository, for instance:

* [/etc/profile.d/slurm-prompt.sh](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm-prompt.sh): provide info of your running Slurm job on your prompt
* [/etc/profile.d/slurm.sh](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh): several helper function to

### Customizing Shell Environment

You can create dotfiles (e.g., `.bashrc`, `.bash_profile`, or
`.profile`, etc) in your `$HOME` directory to put your personal shell
modifications.

??? note "Custom Bash Initialisation Files"
    On ULHPC system `~/.bash_profile` and `~/.profile` are sourced by login
    shells, while `~/.bashrc` is sourced by most of the shell invocations
    including the login shells. In general you can put the environment
    variables, such as `PATH`, which are inheritable to subshells in
    `~/.bash_profile` or `~/.profile` and functions and aliases in the
    `~/.bashrc` file in order to make them available in subshells.
    [`ULHPC/dotfiles` bash
    configuration](https://github.com/ULHPC/dotfiles/blob/master/bash/.bashrc#L469)
    even source the following files for that specific purpose:

    * `~/.bash_private`: custom private functions
    * `~/.bash_aliases`: custom private aliases.

??? info "Understanding Bash Startup Files order"
    See [reference documentation](https://www.gnu.org/software/bash/manual/html_node/Bash-Startup-Files.html).
    That's somehow hard to understand. Some tried to explicit it under the form
    of a "simple" graph -- credits for the one below to [Ian
    Miell](https://zwischenzugs.com/2019/02/27/bash-startup-explained/)
    ([another one](http://www.solipsys.co.uk/new/BashInitialisationFiles.html))

    ![](images/bash_startup.png)

    This explains why normally all [ULHPC launcher
    scripts](https://github.com/ULHPC/tutorials/tree/devel/launchers) start with
    the following [sha-bang](https://tldp.org/LDP/abs/html/sha-bang.html) (`#!`)
    header

    ```bash
    #!/bin/bash -l
    #
    #SBATCH [...]
    [...]
    ```
    That's indeed the only way (_i.e._ using `/bin/bash -l` instead of the
    classical `/bin/bash`) to ensure that `/etc/profile` is sourced natively,
    and thus that all ULHPC environments variables and modules are loaded.
    _If you don't proceed that way_ (i.e. following the classical approach), you
    **MUST** then use the following template you may see from other HPC centers:
    ```bash
    #!/bin/bash
    #
    #SBATCH [...]
    [...]
    # Load ULHPC Profile
    if [ -f  /etc/profile ]; then
       .  /etc/profile
    fi
    ```

Since all ULHPC systems share the [Global HOME](../filesystems/home.md) filesystem,
the same `$HOME` is available regardless of the platform.
To make system specific customizations use the pre-defined environment
`ULHPC_CLUSTER` variable:

!!! example "Example of cluster specific settings"

        ```shell
        case $ULHPC_CLUSTER in
            "iris")
                : # Settings for iris
                export MYVARIABLE="value-for-iris"
                ;;
            "aion")
                : # settings for aion
                export MYVARIABLE="value-for-aion"
                ;;
            *)
                : # default value for
                export MYVARIABLE="default-value"
                ;;
        esac
        ```
