# Projects Accounts

## Shared project in the Global project directory.

We can setup for you a dedicated project directory on the [GPFS/SpectrumScale Filesystem](../filesystems/gpfs.md#global-project-directory-projecthomeworkprojects) for sharing research data with other colleagues.

Whether to _create_ a new project directory or to add/remove members to the group set to access the project data, use the [Service Now HPC Support Portal](https://hpc.uni.lu/support).

[:fontawesome-solid-hand-holding-medical: Service Now HPC Support Portal](https://hpc.uni.lu/support){: .md-button .md-button--link }

## Data Storage Charging

{%
   include-markdown "../policies/usage-charging.md"
   start="<!--data-charging-start-->"
   end="<!--data-charging-end-->"
%}

## Slurm Project Account

As explained in the [Slurm Account Hierarchy](../slurm/accounts.md), projects account can be created at the L3 level of the association tree.

To quickly list a given project accounts and the users attached to it, you can use the [`sassoc` helper function](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh):

```bash
# /!\ ADAPT project acronym/name <name>accordingly
sassoc project_<name>
```

Alternatively, you can rely on [`sacctmgr`](https://slurm.schedmd.com/sacctmgr.html), typically coupled with the `withassoc` attribute:

```bash
# /!\ ADAPT project acronym/name <name>accordingly
sacctmgr show account where name=project_<name> format="account%20,user%20,Share,QOS%50" withassoc
```

As per [HPC Resource Allocations for Research Project](../policies/usage-charging.md#hpc-resource-allocations-for-research-project), creation of such project accounts is **mandatory for funded research projects**, since [usage charging](../policies/usage-charging.md) may occur when a detailed reporting will be provided for auditing purposes.

With the help of the University Research Support department, we will create automatically project accounts from the list of accepted project which acknowledge the need of computing resources.
Feel free nevertheless to use the [Service Now HPC Support Portal](https://hpc.uni.lu/support) to request the _creation_ of a new project account or to add/remove members to the group - this might be **pertinent for internal research projects or specific collaboration with external partners requiring a separate usage monitoring**.

!!! important
    Project account is a natural way to access the higher priority [QOS](../slurm/qos.md) not granted by default to your personal account on the ULHPC. For instance, the [`high` QOS](../slurm/qos.md) is automatically granted as soon as a contribution to the HPC budget line is performed by the project.
