# Iris Compute Nodes

Iris is a cluster of x86-64 Intel-based compute nodes.
More precisely, Iris consists of 196 computational nodes named `iris-[001-196]` and features 3 types of computing resources:

* 168 "_regular_" nodes, Dual Intel Xeon [Broadwell](https://en.wikipedia.org/wiki/Broadwell_(microarchitecture)) or [Skylake](https://en.wikipedia.org/wiki/Skylake_(microarchitecture)) CPU (28 cores), 128 GB of RAM
* 24 "_gpu_" nodes, Dual Intel Xeon [Skylake](https://en.wikipedia.org/wiki/Skylake_(microarchitecture)) CPU (28 cores), 4 [Nvidia Tesla V100](https://www.nvidia.com/en-us/data-center/v100/) SXM2 GPU accelerators (16 or 32 GB), 768 GB RAM
* 4 "_bigmem_" nodes:  Quad-Intel Xeon [Skylake](https://en.wikipedia.org/wiki/Skylake_(microarchitecture)) CPU (112 cores), 3072 GB RAM

| Hostname        (#Nodes) | Node type                           | Processor                                                         | RAM     |
|--------------------------|-------------------------------------|-------------------------------------------------------------------|---------|
| `iris-[001-108]` (108)   | Regular <small>Broadwell</small>    | 2 Xeon E5-2680v4 @ 2.4GHz [14c/120W]                              | 128 GB  |
| `iris-[109-168]` (60)    | Regular <small>Skylake</small>      | 2 Xeon Gold 6132 @ 2.6GHz [14c/140W]                              | 128 GB  |
| `iris-[169-186]` (18)    | Multi-GPU<br/><small>Skylake</small> | 2 Xeon Gold 6132 @ 2.6GHz [14c/140W] <br/> 4x Tesla V100 SXM2 16G | 768 GB  |
| `iris-[191-196]` (6)     | Multi-GPU<br/><small>Skylake</small> | 2 Xeon Gold 6132 @ 2.6GHz [14c/140W] <br/> 4x Tesla V100 SXM2 32G | 768 GB  |
| `iris-[187-190]` (4)     | Large Memory<br/><small>Skylake</small> | 4 Xeon Platinum 8180M @ 2.5GHz [28c/205W]                         | 3072 GB |


## Processors Performance

Each Iris node rely on an Intel x86_64 processor architecture with the following performance:

| Processor Model                                                                                                                                                                                        | #core | TDP(*) | CPU Freq.<br/>(<small>AVX-512 T.Freq.</small>) | $R_\text{peak}$<br/><small>[TFlops]</small> | $R_\text{max}$<br/><small>[TFlops]</small> |
|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------|--------|------------------------------------------------|---------------------------------------------|--------------------------------------------|
| [Xeon E5-2680v4](https://ark.intel.com/content/www/us/en/ark/products/92986/intel-xeon-processor-e5-2620-v4-20m-cache-2-10-ghz.html?wapkw=intel%20xeon%20e5-2620%20v4) <br/><small>(Broadwell)</small> |    14 | 120W   | 2.4GHz <br/>(<small>n/a)                       | 0.538 TF                                    | 0.46 TF                                    |
| [Xeon Gold 6132](https://ark.intel.com/content/www/us/en/ark/products/123541/intel-xeon-gold-6132-processor-19-25m-cache-2-60-ghz.html?wapkw=Xeon%20Gold%206132)       <br/><small>(Skylake)</small>   |    14 | 140W   | 2.6GHz <br/>(<small>2.3GHz</small>)            | 1.03 TF                                     | 0.88 TF                                    |
| [Xeon Platinum 8180M](https://ark.intel.com/content/www/us/en/ark/products/120498/intel-xeon-platinum-8180m-processor-38-5m-cache-2-50-ghz.html)                       <br/><small>(Skylake)</small>   |    28 | 205W   | 2.5GHz <br/>(<small>2.3GHz</small>)            | 2.06 TF                                     | 1.75 TF                                    |

<small>(*) The _Thermal Design Power_ (TDP) represents the average power, in watts, the processor dissipates when operating at Base Frequency with all cores active under an Intel-defined, high-complexity workload.</small>

??? info "Theoretical $R_\text{peak}$ vs. Maximum $R_\text{max}$ Performance for Intel Broadwell/Skylake"
    The reported $R_\text{peak}$ performance is computed as follows for the above processors:

    - The **Broadwell** processors carry on **16 Double Precision (DP) ops/cycle** and support AVX2/FMA3.
    - The selected **Skylake _Gold_** processors have two AVX512 units, thus they are capable of performing 32 DP ops/cycle YET only upon AVX-512 Turbo Frequency (_i.e._, the maximum all-core frequency in turbo mode) in place of the base non-AVX core frequency. The reported values are extracted from the [Reference Intel Specification documentation](https://www.intel.com/content/dam/www/public/us/en/documents/specification-updates/xeon-scalable-spec-update.pdf).

    Then $R_\text{peak} = ops/cycle \times Freq. \times \#Cores$ with the appropriate frequency (2.3 GHz instead of 2.6 for our Skylake processors).

    With regards the _estimation_ of the Maximum Performance $R_\text{max}$, an efficiency factor of 85% is applied.
    It is computed from the expected performance runs during the [HPL](http://www.netlib.org/benchmark/hpl/index.html) benchmark workload as follows:


## Regular Dual-CPU Nodes without Accelerators

These nodes are packaged within Dell PowerEdge C6300 chassis, each hosting 4 PowerEdge C6320 blade servers.

![](images/iris-compute_front.jpg)

### Broadwell Compute Nodes

Iris comprises 108 Dell C6320 "regular" compute nodes `iris-001-108` relying on [Broadwell](https://en.wikipedia.org/wiki/Broadwell_(microarchitecture)) Xeon processor generation, totalling 3024 computing cores.




nodes `iris-001-108`

* Each node are configured as follows:
    - 2 Intel Xeon E5-2680v4 @ 2.4GHz [14c/120W]

(2 Xeon E5-2680v4 @ 2.4GHz, [14c/120W]) and featuring 128GB RAM per node


    or AMD high-core density CPUs, for example (see Table 2): ◦ Intel Xeon Gold Cascade Lake 6248 processors (20c@2.5GHz) ◦ AMD EPYC Rome Processor (64c@2.2GHz)
• RAM: 384GB or 512GB DDR4 with ECC (Error Correcting Codes), i.e., using the best configuration enabling all DRAM channels available on the selected processor family (6 on the targeted Intel processor, 8 on the targeted AMD processors) with 32 GB DDR4 RAM DIMMs.
• IB HDR Connect-X6 Dual Port mezzanine card (or equivalent Intel Omni-Path mezzanine card) depending on selected interconnect technology.
• 1 NVMe drive at 1.6 TB.



- Theoretical Peak Performance $$



(3024 based on Intel Xeon "[Broadwell](https://en.wikipedia.org/wiki/Broadwell_(microarchitecture))" processors, 2800 based on Intel Xeon "[Broadwell](https://en.wikipedia.org/wiki/Skylake_(microarchitecture))" processors).
