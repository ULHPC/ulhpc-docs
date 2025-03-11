{%
   include-markdown "../filesystems/gpfs.md"
   start="<!--projecthome-mount-start-->"
   end="<!--projecthome-mount-end-->"
%}

!!! info "Research Project Allocations, Accounting and Reporting"
    The [Research Support](https://wwwen.uni.lu/university/about_the_university/organisation_charts/organisation_chart_rectorate_central_administration/research_support_department) and [Accounting](https://wwwen.uni.lu/universite/presentation/organigrammes/organigramme_rectorat_administration_centrale/service_des_finances_et_de_la_comptabilite) Departments of the University keep track of the list of research projects funded within the University.
    Starting 2021, a new procedure has been put in place to provide a detailed reporting of the HPC usage for such projects.
    As part of this process, the following actions are taken by the ULHPC team:

    1. a dedicated [project account](../slurm/accounts.md) `<name>` (normally the acronym of the project) is created for accounting purpose at the Slurm level (L3 account - see [Account Hierarchy](../slurm/accounts.md));
    2. a dedicated project directory with the same name (`<name>`) is created, allowing to share data within a group of project researchers, under `$PROJECTHOME/<name>`, _i.e._, `/work/projects/<name>`

    You are then **entitled to submit jobs associated to the project using `-A <name>`** such that the HPC usage is reported accurately.
    The ULHPC team will provide to the project PI (Principal Investigator) and the [Research Support](https://wwwen.uni.lu/university/about_the_university/organisation_charts/organisation_chart_rectorate_central_administration/research_support_department) department a regular report detailing the corresponding HPC usage.
    In all cases, job [billing](../jobs/billing.md) under the conditions defined in the [Job Accounting and Billing](../jobs/billing.md) section may apply.

## New project directory

You can request a new project directory under [ServiceNow](https://hpc.uni.lu/support/) (HPC &rarr; Storage & projects &rarr; Request for a new project).

## Quotas and Backup Policies

See [quotas](../filesystems/quotas.md) for detailed information about inode, space quotas, and file system purge policies.
Your projects backup directories are backed up weekly, according to the policy detailed in the [ULHPC backup policies](backups.md).

{%
   include-markdown "project_acl.md"
   start="<!--start-warning-clusterusers-->"
   end="<!--end-warning-clusterusers-->"
%}

## Project directory modification

You can request changes for your project directory (quotas extension, add/remove a group member) under [ServiceNow](https://hpc.uni.lu/support/):

* HPC &rarr; Storage & projects &rarr; Extend quota/Request information
* HPC &rarr; User access & accounts &rarr; Add/Remove user within project
