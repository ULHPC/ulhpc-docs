# ULHPC User Environment

{%
   include-markdown "workflow.md"
   start="<!--intro-start-->"
%}

For more information:

* [Getting Started](../getting-started.md)
* [Connecting to ULHPC supercomputers](../getting-started.md#connecting-to-ulhpc-supercomputers)
* [ULHPC Storage Systems Overview](../filesystems/index.md)
<!-- * [ULHPC User Software](../software/index.md) -->

!!! warning "'-bash: `module`: command not found' on access/login servers"
    Recall that by default, the `module` command is (_on purpose_) **NOT** available on the [access/login servers](../connect/access.md).
    You HAVE to be on a computing node (within a [slurm job](../slurm/index.md))

## Home and Directories Layout

All UL HPC systems use [global home directories](../filesystems/gpfs.md#global-home-directory-home). You also have access with environment variables to several other pre-defined directories setup over several different _File Systems_ which co-exist on the UL HPC facility and are configured for different purposes. They are listed below:

{%
   include-markdown "../filesystems/index.md"
   start="<!--file-system-table-start-->"
   end="<!--file-system-table-end-->"
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

Since all ULHPC systems share the [Global HOME](../data/layout#home-directory-home) filesystem,
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

[![Rocky Linux](https://upload.wikimedia.org/wikipedia/commons/thumb/9/9c/Rocky_Linux_wordmark.svg/2560px-Rocky_Linux_wordmark.svg.png){: style="width:150px; float: right;"}](https://rockylinux.org/)

## Operating Systems :fontawesome-brands-linux:

[![RedHat](https://www.redhat.com/cms/managed-files/Logo-redhat-color-375.png){: style="width:150px; float: right;"}](https://www.redhat.com/en/technologies/linux-platforms/enterprise-linux)

The ULHPC facility runs [RedHat-based Linux Distributions](https://en.wikipedia.org/wiki/Red_Hat_Enterprise_Linux_derivatives), in particular:

* the [Iris cluster](../systems/iris/index.md) and the [Aion cluster](../systems/aion/index.md) run [RedHat (RHEL)](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/8/) Linux operating system, **version 8** on the access and compute nodes. Servers (not accessible to users) run Rocky Linux 8, which is RHEL compatible, when appropriate.
![](https://www.debian.org/logos/openlogo-100.png){: style="width:75px; float: right;"}
*  Experimental [Grid5000](https://www.grid5000.fr/w/Luxembourg:Hardware) clusters run [Debian](https://www.debian.org/) Linux, version 11

Thus, you are more than encouraged to become familiar - if not yet - with [Linux commands](http://linuxcommand.org/). We can recommend the following sites and resources:

* [Software Carpentry: The Unix Shell](https://swcarpentry.github.io/shell-novice/)
* [Unix/Linux Command Reference](https://files.fosswire.com/2007/08/fwunixref.pdf)


## Discovering, visualizing and reserving UL HPC resources

See [ULHPC Tutorial / Getting Started](https://ulhpc-tutorials.readthedocs.io/en/latest/beginners/#discovering-visualizing-and-reserving-ul-hpc-resources)

## ULHPC User Software Environment

{%
   include-markdown "modules.md"
   start="<!--intro-start-->"
   end="<!--intro-end-->"
%}
{%
   include-markdown "easybuild.md"
   start="<!--intro-start-->"
   end="<!--intro-end-->"
%}

[:fontawesome-solid-sign-in-alt: ULHPC Environment modules](modules.md){: .md-button .md-button--link }
[:fontawesome-solid-sign-in-alt: Using Easybuild on ULHPC Clusters](../environment/easybuild.md){: .md-button .md-button--link }

## Self management of work environments in UL HPC with Conda

{%
   include-markdown "conda.md"
   start="<!--intro-start-->"
   end="<!--intro-end-->"
%}

[:fontawesome-solid-sign-in-alt: Management of work environments with Conda](conda.md){: .md-button .md-button--link }
