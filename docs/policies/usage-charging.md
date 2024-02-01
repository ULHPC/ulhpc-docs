# ULHPC Usage Charging Policy

!!! danger "The advertised prices are for internal partners only"
    The price list and all other information of this page are meant for internal partners, i.e., not for external companies. 
    If you are not an internal partner, please contact us at hpc-partnership@uni.lu. Alternatively, you can contact [LuxProvide](https://luxprovide.lu/), the national HPC center which aims at serving the private sector for HPC needs.

## How to estimate HPC costs for projects?

You can use the following excel document to estimate the cost of your HPC usage:

[:fontawesome-solid-download: UL HPC Cost Estimates for Project Proposals [xlsx] ](../policies/2022_ULHPC_Usage_Charging.xlsx){: .md-button .md-button--link }

Note that there are two sheets offering two ways to estimate based on your specific situation. Please read the red sections to ensure that you are using the correct estimation sheet.

Note that even if you plan for large-scale experiments on [PRACE/EuroHPC supercomputers](https://eurohpc-ju.europa.eu/discover-eurohpc) through computing credits granted by [Call for Proposals for Project Access](https://pracecalls.eu/), you should plan for ULHPC costs since you will have to demonstrate the scalability of your code -- the University's facility is ideal for that. You can contact hpc-partnership@uni.lu for more details about this.

## HPC price list - 2022-10-01

Note that ULHPC price list has been updated, see below.

### Compute

| __Compute type__ | __Description__              | __€ (excl. VAT) / node-hour__ |
|------------------|------------------------------|-------------------------------|
| CPU - small      | 28 cores, 128 GB RAM         | 0.25€                         |
| CPU - regular    | 128 cores, 256 GB RAM        | 1.25€                         |
| CPU - big mem    | 112 cores, 3 TB RAM          | 6.00€                         |
| GPU              | 4 V100, 28 cores, 768 GB RAM | 5.00€                         |

The prices above correspond to a full-node cost. However, jobs can use a fraction of a node and the price of the job will be computed based on that fraction. Please find below the core-hour / GPU-hour costs and how we compute how much to charge:

| __Compute type__ | __Unit__                     | __€ (excl. VAT)__             | 
|------------------|------------------------------|-------------------------------|
| CPU - small      | Core-hour                    | 0.0089€                       |
| CPU - regular    | Core-hour                    | 0.0097€                       |
| CPU - big mem    | Core-hour                    | 0.0535€                       |
| GPU              | GPU-hour                     | 1.25€                         |

For CPU nodes, the fraction correspond to the number of requested cores, e.g. 64 cores on a CPU - regular node corresponds to 50% of the available cores and thus will be charged 50% of 1.25€. 

Regarding the RAM of a job, if you do not override the default behaviour, you will receive a percentage of the RAM corresponding to the amount of requested cores, e.g, 128G of RAM for the 64 cores example from above (50% of a CPU - regular node). If you override the default behaviour and request more RAM, we will re-compute the equivalent number of cores, e.g. if you request 256G of RAM and 64 cores, we will charge 128 cores.

For GPU nodes, the fraction considers the number of GPUs. There are 4 GPUs, 28 cores and 768G of RAM on one machine. This means that for each GPU, you can have up to 7 cores and 192G of RAM. If you request more than those default, we will re-compute the GPU equivalent, e.g. if you request 1 GPU and 8 cores, we will charge 2 GPUs.


### Storage

| __Storage type__ | __€ (excl. VAT) / GB / Month__ | __Additional information__ |
|------------------|--------------------------------|----------------------------|
| Home             | Free                           | 500 GB                     |
| Project          | 0.02€                          | 1 TB free                  |
| Scratch          | Free                           | 10 TB                      |

Note that for project storage, we charge **the quota and not the used storage**.

## HPC Resource allocation for UL internal R&D and training

<!--resource-allocation-ul-start-->

ULHPC resources are **free of charge for UL staff for their _internal_ work and training activities**.
Principal Investigators (PI) will nevertheless receive on a regular basis a usage report of their team activities on the UL HPC platform.
The corresponding accumulated price will be provided even if this amount is purely indicative and won't be charged back.

Any other activities will be reviewed with the rectorate and are a priori subjected to be billed.

<!--resource-allocation-ul-end-->


## Submit project related jobs 

To allow the ULHPC team to keep track of the jobs related to a project, use the `-A <projectname>` flag in Slurm, either in the Slurm directives preamble of your script, e.g.,

```bash
#SBATCH -A myproject
```

or on the command line when you submit your job, _e.g._, `sbatch -A myproject /path/to/launcher.sh`


