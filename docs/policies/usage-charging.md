# ULHPC Usage Charging Policy

ULHPC allocates time on compute nodes and space on its different file systems to support with the research and development performed on its computational resources.

## Service Unit

!!! info "Service Unit (SU)"
    The utilization of the university's computational resources is charged in **Service Unit** (SU)

    * 1 SU _routhly_ correspond to 1 hour on 1 physical processor core on regular computing node
    * Depending on the usage profile, 1 SU is charged _0,03€ per SU (VAT excluded)_
        - this applies in particular to external partners or funded projects, details below

The total number of Service Units a job costs is a function of the number of nodes, the walltime used by the job, and the "charge factor" for the type of resources (amount of cores, memory and GPU) upon which the job was run.
Charge factors are set by ULHPC to accommodate for the relative power of the architecture and the scarcity of the resource.

## Computing Job Charges

In details, a Job is characterized (and thus billed) according to the following elements:

* $T_\text{exec}$: Execution time (in hours) also called _walltime_
* $N_\text{Nodes}$: number of computing nodes, and **per node**:
    * $N_\text{cores}$: number of CPU cores allocated  per node
    * $Mem$: memory size allocated per node, in GB
    * $N_\text{gpus}$: number of GPU allocated per node
* associated weighted factors $\alpha_{cpu},\alpha_{mem},\alpha_{GPU}$  defined as [`TRESBillingWeight`](https://slurm.schedmd.com/tres.html) in Slurm Trackable RESources accounting. They capture the  consumed resources other than just CPUs and are taken into account in fairshare factor. The following weight are formalized in the definition of the charging factor:
    * $\alpha_{cpu}$: normalized relative perf. of CPU processor core (reference: skylake 73,6 GFlops/core)
    * $\alpha_{mem}$: inverse of the average available memory size per core
    * $\alpha_{GPU}$: weight per GPU accelerator


!!! tip "Billing Rate and Service Units per Job"
    For a given job, the _billing rate_ is defined from the configured [`TRESBillingWeight`](https://slurm.schedmd.com/tres.html) as follows:

    $$B_\text{rate} = N_\text{Nodes}\times[\alpha_{cpu}\times N_\text{cores} + \alpha_{mem}\times Mem + \alpha_{gpu}\times N_\text{gpus}]$$

    It follows that the number of service units associated to a given job is given by:

    $$B_\text{rate}\times  T_\text{exec} = N_\text{Nodes}\times[\alpha_{cpu}\times N_\text{cores} + \alpha_{mem}\times Mem + \alpha_{gpu}\times N_\text{gpus}]\times T_\text{exec}$$

You can quickly access the charging and billing rate of a given job from its Job ID `<jobID>` with the [`sbill`](https://github.com/ULHPC/tools/blob/master/slurm/profile.d/slurm.sh#L477) utility:

```bash
$ sbill -h
Usage: sbill -j <jobid>
Display job charging / billing summary

$ sbill -j 2240777
# sacct -X --format=AllocTRES%60,Elapsed -j 2240777
                                                   AllocTRES    Elapsed
       ----------------------------------------------------- ----------
                         billing=448,cpu=224,mem=896G,node=8   11:35:51
       Total usage: 5195.68 SU (indicative price: 155.87€ HT)
```

_Note_: For a running job, you can also check the `TRES=[...],billing=<Brate>` output of `scontrol show job <jobID>`.


### Charge Weight Factors for 2021-2022


| __Cluster__                      | __Node Type__ | __CPU arch__ | __Partition__ | __#Cores/node__ | $\mathbf{\alpha_{cpu}}$ | $\mathbf{\alpha_{mem}}$ | $\mathbf{\alpha_{GPU}}$ |
|----------------------------------|---------------|--------------|---------------|-----------------|-------------------------|-------------------------|-------------------------|
| [Aion](../systems/aion/index.md) | Regular       | `epyc`       | `batch`       | 128             | 0,57                    | $\frac{1}{1.75}$        | 0                       |
| [Iris](../systems/iris/index.md) | Regular       | `broadwell`  | `batch`       | 28              | 1.0*                    | $\frac{1}{4} = 0,25$    | 0                       |
| [Iris](../systems/iris/index.md) | Regular       | `skylake`    | `batch`       | 28              | 1.0                     | $\frac{1}{4} = 0,25$    | 0                       |
| [Iris](../systems/iris/index.md) | GPU           | `skylake`    | `gpu`         | 28              | 1.0                     | $\frac{1}{27}$          | 50                      |
| [Iris](../systems/iris/index.md) | Large-Mem     | `skylake`    | `bigmem`      | 112             | 1.0                     | $\frac{1}{27}$          | 0                       |

In particular, `interactive` jobs are always free-of-charge.

??? example "2 _regular skylake_ nodes on `iris` cluster"
    Continuous use of _2 regular skylake nodes_ (56 cores, 224GB Memory) on `iris` cluster
    Each node features 28 cores, 4 GigaByte RAM per core _i.e._, 112GB per node.
    It follows that for such an allocated job:

    $$B_\text{rate} = 2 \text{ nodes} \times[\alpha_{cpu}\times 28 + \alpha_{mem}\times 4\times 28 + \alpha_{gpu}\times 0] = 2\times[(1.0+\frac{1}{4}\times 4)\times 28] = 112$$

    Such a job running **continuously for 30 days** would then correspond to:

    * a total of $B_\text{rate}\times  T_\text{exec}= 112\times 30\text{ days}\times 24\text{ hours} =112\times 720$ = **80640 SU**.
    * if this job would be billed, it would lead to $80640\text{ SU}\times 0,03€/SU$ = _2419,2€ VAT excluded_

??? example "2 _regular epyc_ nodes on `aion` cluster"
    Continuous use of _2 regular epyc nodes_ (256 cores, 448GB Memory) on `aion` cluster.
    Each node features 128 cores, 1,75 GigaByte RAM per core _i.e._, 224GB per node.
    It follows that for such an allocated job:

    $$B_\text{rate} = 2 \text{ nodes} \times[\alpha_{cpu}\times 128 + \alpha_{mem}\times 1,75\times 128 + \alpha_{gpu}\times 0] = 2\times[(0.57+\frac{1}{1.75}\times 1.75)\times 128]=401.92$$

    Such a job running **continuously for 30 days** would then correspond to:

    * a total of $B_\text{rate}\times  T_\text{exec}= 401.92 \times 30\text{ days}\times 24\text{ hours} =401.92\times 720$ = **289382,4  SU**
    * if this job would be billed, it would lead to $289382,4\text{ SU}\times 0,03€/SU$ = _8681,47€ VAT excluded_

??? example "1 _GPU node_ (and its 4 GPUs) on `iris` cluster"
    Continuous use of _1 GPU nodes_ (28 cores, 4 GPUs, 756GB Memory) on `iris` cluster.
    Each node features 28 cores, 4 GPUs per node,  27 GigaByte RAM per core, 756 GB per node.
    It follows that for such an allocated job:

    $$B_\text{rate} = 1 \text{ node} \times[\alpha_{cpu}\times 28 + \alpha_{mem}\times 27\times 28 + \alpha_{gpu}\times 4] = 1\times[(1.0+\frac{1}{27}\times 27)\times 28 + 50.0\times 4]=256$$

    Such a job running **continuously for 30 days** would then correspond to:

    * a total of $B_\text{rate}\times  T_\text{exec}=  256 \times 30\text{ days}\times 24\text{ hours} =256\times 720$ = **184320 SU**
    * if this job would be billed, it would lead to  $184320 \text{ SU}\times 0,03€/SU$ = _5529,6€ VAT excluded_

??? example "1 _Large-Memory_ node on `iris` cluster"
    Continuous use of _1 Large-Memory nodes_ (112 cores, 3024GB Memory) on `iris` cluster.
    Each node features $4\times 28$=112 cores, 27 GigaByte RAM per core _i.e._, 3024GB per node.
    It follows that for such an allocated job:

    $$B_\text{rate} = 1 \text{ node} \times[\alpha_{cpu}\times 112 + \alpha_{mem}\times 27\times 112 + \alpha_{gpu}\times 0] = 1\times[(1.0+\frac{1}{27}\times 27)\times 112]=224$$

    Such a job running **continuously for 30 days** would then correspond to:

    * a total of $B_\text{rate}\times  T_\text{exec}=  224 \times 30\text{ days}\times 24\text{ hours} =224\times 720$ = **161280 SU**
    * if this job would be billed, it would lead to  $161280 \text{ SU}\times 0,03€/SU$ = _4838,4€ VAT excluded_

### Data Storage Charging

Each user has a personal [quota](../filesystems/quotas.md) in their home directory free of charge.
Each project has a [shared quota](../filesystems/quotas.md) on the [GPFS/SpectrumScale Filesystem](../filesystems/gpfs.md#global-project-directory-projecthomeworkprojects).
A capacity up to 1 TeraByte is created for a given project free of charge.

Capacity extensions are possible and will be charged at the price of **100€ (VAT excluded) per each additional TeraByte per month**

!!! example "6TB Project allocation"
    Example: 5 additional TeraBytes (for a total of 6TB available) for 36 months will be charged

    5TB $\times$ 36 months $\times$ 100€ = _18000€ VAT excluded_.

ULHPC imposes quotas on space utilization as well as inodes (number of files).
For more information about these quotas please see the [file system quotas page](../filesystems/quotas.md).


## Assigning Computing Charges

To charge to a non-default account such as a project or a specific training, use the `-A <projectname> flag in Slurm, either in the Slurm directives preamble of your script, e.g.,

```bash
#SBATCH -A myproject
```

or on the command line when you submit your job, _e.g._, `sbatch -A myproject /path/to/launcher.sh`



## HPC Resource allocation for UL internal R&D and training

ULHPC resources are **free of charge for UL staff for their _internal_ work and training activities**.
Principal Investigators (PI) will nevertheless receive on a regular basis a usage report of their team activities on the UL HPC platform.
The corresponding accumulated price will be provided even if this amount is purely indicative and won't be charged back.

Any other activities will be reviewed with the rectorate and are a priori subjected to be billed.

## HPC Resource Allocations for Research Project

Upon request of the FNR and in collaboration with the rectorate and the accounting department of the University, we have formalized the HPC cost model applicable on the ULHPC Facility.
On July 7, 2020, this policy was approved by the rectorate and was later validated by the FNR.

[:fontawesome-solid-sign-in-alt:  ULHPC Resource Allocations Policy for Research Projects (PDF)](https://hpc.uni.lu/download/documents/Uni.lu-HPC-Resource-allocation-policy_budget-guidelines-v1.0.pdf){: .md-button .md-button--link }

!!! important "Preparing your budget plan to support HPC costs"
    As a consequence, you (project PI) are entitled to plan your computing costs in your project budget plan.
    While the research support department of the University will help you in this process, we consider three
    cases:

    1. You __know__ relatively precisely your computing needs.
    Then use the [above charging guidelines](#charge-weight-factors-for-2021-2022) to estimate from the forseen required resources the billing rates and total walltime the corresponding amount that will be charged.
    2. You are __not able to anticipate the type and amount of resources needed__, but you know ULHPC resources will be required.
    In this case, we suggest you to apply a simple rule based on the total number of funded persons: **account 5529,60€ for every 12 PM of funded personnel** (i.e., 1 month of continuous usage on the most expensive type of resource).
    In particular, account by default:

        - Budget for 1 funded PhD student (36+12PM):  22118,4€ (VAT excluded)
        - Budget for 1 funded PostDoc (24PM):         11059,2€ (VAT excluded)

    3. You don't know and you don't plan to use ULHPC resources. Then you are "safe" but be aware that any outsourced computing expense (whether cloud or HPC) should be budgeted.

Note that even if you plan for large-scale experiments on [PRACE/EuroHPC supercomputers](https://eurohpc-ju.europa.eu/discover-eurohpc) through computing credits granted by [Call for Proposals for Project Access](https://pracecalls.eu/), you should plan for ULHPC costs since you will have to demonstrate the scalability of your code -- the University's facility is ideal for that.

## HPC Service Contract for external and private partners

The University extends access to its HPC resources (i.e., facility and expert HPC consultants) to external and private partners.
While a limited amount of computational resources can be allocated in such cases, this can be done through a dedicated service contract enforcing a **1 year commitment with an initial pre-paid forfait covering a share of the total planned usage, whether used or not**.
Several companies such as [Arcelor Mittal](https://luxembourg.arcelormittal.com/26/87/language/FR) or [Ceratizit](https://www.ceratizit.com/) use or have used the ULHPC facility to serve their internal needs with such service contract agreements.

[:fontawesome-solid-sign-in-alt: Contact us for more details.](mailto:hpc-users@uni.lu){: .md-button .md-button--link } [:fontawesome-solid-sign-in-alt:  ULHPC for External Partners Policy (PDF)](https://hpc.uni.lu/download/documents/Uni.lu-HPC-Resource-allocation-policy_budget-guidelines-v1.0.pdf){: .md-button .md-button--link }


For such pure commercial requests, you may also want to contact [LuxProvide](https://luxprovide.lu/), the national HPC center which also aims at serving the private sector for HPC needs.
