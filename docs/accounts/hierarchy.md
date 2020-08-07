# Slurm Account Hierarchy

The ULHPC resources can be reserved and allocated for the execution of jobs scheduled on the platform thanks to a Resource and Job Management Systems (RJMS) - [Slurm](https://slurm.schedmd.com/documentation.html) in practice.
This tool is configured to collect accounting information for every job and job step executed -- see [SchedMD accounting documentation](https://slurm.schedmd.com/accounting.html).


??? info "ULHPC account (login) vs. Slurm [meta-]account"
    - Your [ULHPC account](index.md) defines the UNIX **user** you can use to connect to the facility and make you known to our systems. They are managed by [IPA](ipa.md) and define your `login`.

    - _Slurm accounts_, further refered to as **meta-account** in the sequel, are more loosely defined in Slurm terminology for accounting purposes, and should be seen as something similar to a UNIX group: it may contain other (set of) slurm account(s), multiple users, or just a single user. **A user may belong to multiple slurm accounts, but must have a DefaultAccount**.

## Meta-account Tree Organization

Accounting records are organized as a hierarchical tree according to 4 layers as depicted in the below figure (click to enlarge):

[![](../images/slurm_account_hierarchy.png)](../images/slurm_account_hierarchy.pdf)

| Level  | Account Type  | Description                                                       | Example                    |
|--------|---------------|-------------------------------------------------------------------|----------------------------|
| __L1__ | meta-account  | Top-level structure / organizations                               | UL, Externals, Projects... |
| __L2__ | meta-account  | Organizational Units, Projects Acronyms                           | FSTM, LCSB, LIST...        |
| __L3__ | meta-acccount | Principal investigators (PIs), courses/lectures                   | `firstname.lastname`       |
| __L4__ | login         | End-users (staff, student) _i.e._, your [ULHPC account](index.md) | `svarrette`                |

??? warning "No association, no job!"
    It is mandatory to have your login registered within at least one _association_ toward a meta-account (PI, project name) to be able to schedule jobs on the

At any moment of time, you can use `acct <login|account>` (defined in [`/etc/profile.d/slurm.sh`](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh)) to get your meta-account information[^1].
You can also see the current association hierarchy for a given meta-account `<account>` via [`sacctmgr`](https://slurm.schedmd.com/sacctmgr.html):

```bash
# get your L3 meta-account association and default account
acct $(whoami)
# get hierarchical association tree for a given account <account>
# /!\ ADAPT <account> accordingly (ex: FSTM)
sacctmgr show association tree where account=<account> format=Account,user%30  withsubaccount
```

## Impact on FairSharing and Job Accounting

Every node in the above-mentioned tree hierarchy is associated with a weight defining its **Raw Share** in the [FairSharing](../jobs/fair-sharing.md) mechanism in place.
Different rules are applied to define these weights/shares depending on the level in the hierarchy:

* __L1__: arbitrary shares to dedicate at least 80% of the platform to serve UL needs and projects
* __L2__: out-degree of the tree nodes
* __L3__: a function reflecting the budget contribution of the PI/project (normalized on a per-month basis) for the year in exercise.

More details are given [on this page](../jobs/fair-sharing.md).


## Default vs. Project accounts

Default account associations are defined as follows:

* For UL staff or external partners: your Line Manager `firstname.lastname` within the institution (Faculty, IC, Company) you belong too.
* For students: the lecture/course they are registered too

In addition, your user account (ULHPC login) may be associated to other meta-accounts such as projects or specific training events.
To establish Job accounting against these extra specific accounts, use: `{sbatch|srun} -A <name>`



[^1]: restrictions applies and do not permit to reveal all information for other accounts than yours.
