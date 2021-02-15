All ULHPC login accounts are associated with specific individuals and
must **not** be shared.
In some HPC centers, you may be able to request _Collaboration Accounts_ designed to handle the following use cases:

* __Collaborative Data Management__:
  Large scale experimental and simulation data are typically read or written by multiple collaborators and are kept on disk for long periods.
* __Collaborative Software Management__
* __Collaborative Job Management__

!!! info
    By default, we **DO NOT** provide Collaboration Accounts and encourage the usage of shared research projects `<name>` stored on the [Global project directory](../filesystems/gpfs.md#global-project-directory-projecthomeworkprojects) to enable the group members to manipulate project data with the appropriate use of unix groups and file permissions.

    For dedicated [job billing and accounting](../jobs/billing.md) purposes, you should also request the creation of a [project account](../slurm/accounts.md#default-vs-project-accounts) (this will be done for all accepted funded projects).

    For more details, see [Project Accounts documentation](../accounts/projects.md).

We are aware nevertheless that a problem that often arises is that the files are owned by the collaborator who did the work and if that collaborator changes roles the default unix file permissions usually are such that the
files cannot be managed (deleted) by other members of the collaboration and system administrators must be contacted.
Similarly, for some use cases, Collaboration Accounts would enable members of the team to manipulate jobs submitted by other team members as necessary.
Justified and argued use cases can be submitted to the HPC team to find the appropriate solution by [opening a ticket on the HPC Helpdesk Portal](../support/index.md).
