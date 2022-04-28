# Fairsharing and Job Accounting

* __Resources__:
    - [Slurm Priority, Fairshare and Fair Tree (PDF)](https://slurm.schedmd.com/SLUG19/Priority_and_Fair_Trees.pdf)
    - [SchedMD Slurm documentation: Multifactor Priority Plugin](https://slurm.schedmd.com/priority_multifactor.html)
    - [Fair tree](https://slurm.schedmd.com/fair_tree.html) algorithm, [FAS RC docs](https://docs.rc.fas.harvard.edu/kb/fairshare/), Official [`sshare`](https://slurm.schedmd.com/sshare.html) documentation


**Fairshare** allows past resource utilization information to be taken into
account into job feasibility and priority decisions to ensure a _fair_
allocation of the computational resources between the all ULHPC users.
A difference with a _equal_ scheduling is illustrated in the side picture (_[source](http://www.fairsharemovement.com/en/fair-vs-equal)_).

![](images/equal_vs_fair_share.jpg){: style="width:400px; float: right;"}

Essentially fairshare is a way of ensuring that users get their appropriate
portion of a system. Sadly this term is also used confusingly for different
parts of fairshare listed below, so for the sake of clarity, the following terms
will be used:

* __[Raw] Share__: portion of the system users have been granted
* __[Raw] Usage__: amount of the system users have actually used so far
    - The _fairshare score_ is the value the system calculates based on the usage
   _and_ the share (see below)
*  __Priority__: the priority that users are assigned based off of their fairshare score.

!!! info "Demystifying Fairshare"
    While fairshare may seem complex and confusing, it is actually quite logical
    once you think about it.
    The scheduler needs some way to adjudicate who gets what resources when
    different groups on the cluster have been granted different resources and shares
    for various reasons (see [Account Hierarchy](accounts.md)).

    In order to serve the great variety of groups and needs on the cluster, a
    method of fairly adjudicating job priority is required.
    **This is the goal of Fairshare**.
    Fairshare allows those users who have **not fully used** their resource
    grant to **get higher priority** for their jobs on the cluster, while making
    sure that those groups that have used _more_ than their resource grant
    do not overuse the cluster.

    **The ULHPC supercomputers are a limited shared resource, and Fairshare
    ensures everyone gets a fair opportunity to use it regardless of
    how big or small the group is**.


## FairTree Algorithm

There exists several [fairsharing
algorithms](https://slurm.schedmd.com/priority_multifactor.html#fairshare)
implemented in Slurm:

* [Classic Fairshare](https://slurm.schedmd.com/classic_fair_share.html)
* [Depth-Oblivious Fair-share](https://slurm.schedmd.com/priority_multifactor3.html)
* __[Fair Tree](https://slurm.schedmd.com/fair_tree.html)__ (now implemented on
  ULHPC since Oct 2020)


!!! question "What is Fair Tree?"
    The [Fair Tree](https://slurm.schedmd.com/fair_tree.html) algorithm
    prioritizes users such that if accounts A and B are siblings and A has a
    higher fairshare factor than B, then all children of A will have higher
    fairshare factors than all children of B.

    This is done through a [rooted plane tree
    (PDF)](http://www.math.ucsd.edu/~ebender/CombText/ch-9.pdf), also known as a
    rooted ordered tree, which is logically created then sorted by fairshare
    with the highest fairshare values on the left.
    The tree is then visited in a _depth-first traversal_ way.
    Users are ranked in pre-order as they are found. The ranking is used to
    create the final fairshare factor for the user.
    [Fair Tree Traversal
    Illustrated](https://docs.google.com/uc?id=0B8dVHMccGpAJLWFfdjlNMnFoZk0&export=download) -
    [initial post](http://tech.ryancox.net/2014/08/fair-tree-slurm-fairshare-algorithm.html)

    Some of the benefits include:

    * All users from a higher priority account receive a higher fair share
    factor than all users from a lower priority account.
    * Users are sorted and ranked to prevent errors due to precision loss.
    Ties are allowed.
    * Account coordinators cannot accidentally harm the priority of their users
    relative to users in other accounts.
    * Users are extremely unlikely to have exactly the same fairshare factor as
    another user due to loss of precision in calculations.
    * New jobs are immediately assigned a priority.

    [:fontawesome-solid-sign-in-alt: Overview of Fair Tree for End Users](https://slurm.schedmd.com/fair_tree.html#enduser){: .md-button .md-button--link }
    [:fontawesome-solid-sign-in-alt: Level Fairshare Calculation](https://slurm.schedmd.com/fair_tree.html#fairshare){: .md-button .md-button--link }



## Shares

On ULHPC facilities, each user is associated by default to a meta-account reflecting its
direct Line Manager  within the institution (Faculty, IC, Company) you belong
too -- see [ULHPC Account Hierarchy](accounts.md).
You may have other account associations (typically toward projects accounts, granting
access to different QOS for instance), and each accounts have Shares granted to
them. **These Shares determine how much of the cluster that group/account has
been granted**.
Users when they run are charged back for their runs against the account used
upon job submission -- you can use `sbatch|srun|... -A <account> [...]` to
change that account.

[:fontawesome-solid-sign-in-alt: ULHPC Usage Charging
Policy](../policies/usage-charging.md){: .md-button .md-button--link }

{%
   include-markdown "accounts.md"
   start="<!--share-rule-per-level-start-->"
   end="<!--share-rule-per-level-end-->"
%}




## Fair Share Factor

The _Fairshare score_ is the value Slurm calculates based off of user's
usage reflecting the difference between the portion of the computing resource
that has been promised (share) and the amount of resources that has been
consumed.
It thus influences the order in which a user's queued jobs are scheduled to run based on the portion of the computing resources they have been allocated and the resources their jobs have already consumed.

In practice, Slurm's fair-share factor is a floating point number between 0.0 and 1.0 that reflects the shares of a computing resource that a user has been allocated and the amount of computing resources the user's jobs have consumed.

* The higher the value, the higher is the placement in the queue of jobs waiting to be scheduled.
* Reciprocally, the more resources the users is consuming, the lower the fair share factor will be which will result in lower priorities.

### `ulhpcshare` helper

!!! important "Listing the ULHPC shares: `ulhpcshare` helper"
    [`sshare`](https://slurm.schedmd.com/sshare.html) can be used to view the fair share factors and corresponding promised and actual usage for all users.
    **However**, you are encouraged to use the `ulhpcshare` helper function:
    ```bash
    # your current shares and fair-share factors among your associations
    ulhpcshare
    # as above, but for user '<login>'
    ulhpcshare -u <login>
    # as above, but for account '<account>'
    ulhpcshare -A <account>
    ```
    The column that contains the actual factor is called "FairShare".

### Official `sshare` utility

`ulhpcshare` is a wrapper around the official [`sshare`](https://slurm.schedmd.com/sshare.html) utility.
You can quickly see your score with
```console
$ sshare  [-A <account>] [-l] [--format=Account,User,RawShares,NormShares,EffectvUsage,LevelFS,FairShare]
```
It will show the Level Fairshare value as `Level FS`.
The field shows the value for each association, thus allowing users to see the results of the fairshare calculation at each level.

_Note_: Unlike the Effective Usage, the Norm Usage is **not** used by Fair Tree but is still displayed in this case.

### Slurm Parameter Definitions

In this part some of the set slurm parameters are explained which are used to set up the Fair Tree Fairshare Algorithm. For a more detailed explanation please consult the [official documentation](https://slurm.schedmd.com/)

* `PriorityCalcPeriod=HH:MM::SS`: frequency in minutes that job half-life decay and Fair Tree calculations are performed.
* `PriorityDecayHalfLife=[number of days]-[number of hours]`: the time, of which the resource consumption is taken into account for the Fairshare Algorithm, can be set by this.
* `PriorityMaxAge=[number of days]-[number of hours]`: the maximal queueing time which counts for the priority calculation. Note that queueing times above are possible but do not contribute to the priority factor.

A quick way to check the currently running configuration is:

```bash
scontrol show config | grep -i priority
```


## Trackable RESources (TRES) Billing Weights

Slurm saves accounting data for every job or job step that the user submits.
On ULHPC facilities, Slurm [Trackable RESources
(TRES)](https://slurm.schedmd.com/tres.html) is enabled to allow for
the scheduler to charge back users for how much they have used of different
features (i.e. not only CPU) on the cluster -- see [Job Accounting and Billing](../jobs/billing.md).
This is important as the usage of the cluster factors into the Fairshare
calculation.

{%
   include-markdown "../jobs/billing.md"
   start="<!--TRESBillingWeight-start-->"
   end="<!--TRESBillingWeight-end-->"
%}

{%
   include-markdown "../policies/usage-charging.md"
   start="<!--TRESBillingWeight-table-start-->"
   end="<!--TRESBillingWeight-table-end-->"
%}

## FAQ

### Q: My user fairshare is low, what can I do?

We have introduced an efficiency score evaluated on a regular basis (by default,
every year) to measure how efficient you use the computational resources of the
University according to several measures for completed jobs:

* How efficient you were to estimate the walltime of your jobs (Average Walltime
Accuracy)
* How CPU/Memory efficient were your completed jobs (see `seff`)

Without entering into the details, we combine these metrics to compute an unique
score value $S_\text{efficiency}$ and you obtain a grade: **A** (very good), **B**,
**C**, or **D** (very bad) which can increase your user share.

### Q: My account fairshare is low, what can I do?

There are several things that can be done when your fairshare is low:

1. __Do not run jobs__: Fairshare recovers via two routes.
    - The first is via your group not running any jobs and letting others use the
    resource.  That allows your fractional usage to decrease which in turn
    increases your fairshare score.
    - The second is via the half-life we apply to fairshare which ages out old
      usage over time.
     Both of these method require not action but inaction on the part of your
     group.
     Thus to recover your fairshare simply stop running jobs until your fairshare
     reaches the level you desire.
     Be warned this could take several weeks to accomplish depending on your
     current usage.
2. __Be patient__, as a corollary to the previous point. **Even if your
   fairshare is low, your job gains priority by sitting the queue** (see [Job Priority](../jobs/priority.md))
   The longer it sits the higher priority it gains.  So even if you have very
   low fairshare your jobs will eventually run, it just may take several days to
   accomplish.
3. __Leverage Backfill__: Slurm runs in two scheduling loops.
    - The first loop is the _main_ loop which simply looks at the top of the
      priority chain for the partition and tries to schedule that job.  It will
      schedule jobs until it hits a job it cannot schedule and then it restarts
      the loop.
    - The second loop is the _backfill_ loop. This loop looks through jobs
      further down in the queue and asks can I schedule this job now and not
      interfere with the start time of the top priority job.  Think of it as the
      scheduler playing giant game of three dimensional tetris, where the
      dimensions are number of cores, amount of memory, and amount of time.  If
      your job will fit in the gaps that the scheduler has it will put your job
      in that spot even if it is low priority.  This requires you to be very
      accurate in specifying the core, memory, and time usage (**typically below
      ) of your job.
      **The better constrained your job is the more likely the scheduler is to
      fit you in to these gaps**.
      The `seff` utility is a great way of figuring out your job performance.
4. __Plan__: Better planning and knowledge of your historic usage can help you
   better budget your time on the cluster. **Our clusters are not infinite
   resources**.  You have been allocated a slice of the cluster, thus it is best
   to budget your usage so that you can run high priority jobs when you need to.
5. __HPC Budget contribution__: If your group has persistent high demand that cannot be met
   with your current allocation, serious consideration should be given to
   contributing to the ULHPC budget line.
     - This _should_ be done for funded research projects - see
       [HPC Resource Allocations for Research Project](../policies/usage-charging.md#hpc-resource-allocations-for-research-project)
     - This _can_ be done by each individual PI, Dean or IC director
    In all cases, any contribution on year `Y` grants additional shares for the
    group starting year `Y+1`. We apply a consistent (complex) function taking
    into account depreciation of the investment. Contact us (by [mail](mailto:hpc-team 'at'
    uni.lu) or by a [ticket](https://hpc.uni.lu/support) for more details.
