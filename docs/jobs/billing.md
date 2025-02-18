# Job Accounting and Billing

[:fontawesome-solid-sign-in-alt: Usage Charging Policy](../policies/usage-charging.md){: .md-button .md-button--link }

## Billing rates

{%
   include-markdown "../policies/usage-charging.md"
   start="<!--job-charge-start-->"
   end="<!--job-charge-end-->"
%}

## Trackable RESources (TRES) Billing Weights

The above policy is in practice implemented through the Slurm [Trackable RESources
(TRES)](https://slurm.schedmd.com/tres.html) and remains an important factor for the [Fairsharing score](../slurm/fairsharing.md) calculation.

<!--TRESBillingWeight-start-->

As explained in the [ULHPC Usage Charging
Policy](../policies/usage-charging.md), we set TRES for CPU, GPU, and Memory
usage according to _weights_ defined as follows:

| __Weight__     | __Description__                                                                       |
|----------------|---------------------------------------------------------------------------------------|
| $\alpha_{cpu}$ | Normalized relative performance of CPU processor core (ref.: skylake 73.6 GFlops/core) |
| $\alpha_{mem}$ | Inverse of the average available memory size per core                                 |
| $\alpha_{GPU}$ | Weight per GPU accelerator                                                          |

Each [partition](../slurm/partitions.md) has its own weights
(combined into [`TRESBillingWeight`](https://slurm.schedmd.com/tres.html)) you can check with

```bash
# /!\ ADAPT <partition> accordingly
scontrol show partition <partition>
```

<!--TRESBillingWeight-end-->
