# Affinity and pinning of processes and threads

HPC systems consist of multiple components that provide access to various resources. A process or thread running in some core of the system rarely has the same quality of access to all the resources. Take for instance a single CPU node of Iris.

!!! tip "Topology of an Iris CPU node"

    <figure markdown="span">
        ![Iris CPU node topology](images/iris-cpu-node-topology.svg){width="600" style="display: block; margin: 0 auto"}
    </figure>

    An Iris CPU node; the node contains 2 CPU sockets, each socket contains a single NUMA[^43] node, each NUMA node consists of a group of 14 cores sharing a single physical L3 cache, and each core provides a single PU[^53].

A typical HPC cluster node is composed of computing cores that are integrated in an recursive manner in more complex structures to implement the functionality of the node. In Iris CPU nodes for instance,

- compute nodes contain 2 sockets,
- each socket contains a single NUMA[^43],
- each NUMA node consists of a group of 14 cores sharing a single physical L3 cache, and
- each core provides a single PU (processor unit)[^53][^56].

[^43]: NUMA: Non-Uniform Memory Access
[^53]: PU: Processor Unit
[^56]: Simultaneous Multi Threading (SMT), also known as Hyper-Threading for Intel CPUs, is disabled in our cluster nodes because it impacts negatively numerical calculations that comprise the vast majority of our workloads.

The CPU is thus organized in a number of levels with actual threads running on processor units, and processes consist of one or more threads. Communication between threads and thus processes, involves sending information from one thread to another. Depending on how many levels of the node architecture hierarchy the message has to pass the slower the communication will be. Also, threads and thus processes that are close in the architectural hierarchy tend to share memory. If you want more memory per thread you may have to spread your threads across processor units that are distant with respect to communication.

Typically the libraries used in HPC applications provide a high degree of control of process and thread placement. In order to extract the best performance from the HPC system you often need to specify the placement of threads and processes.

## Process and thread placement

A call to `sbatch` or `salloc` in clusters with the Slurm scheduler allocates the resources for a job. To pin processes of your job to specific cores within each node you need to set binding option in each step of your job with `srun` or in raw calls to `mpirun`.

### Binding processes

Process (tasks) are bound to cores with the `--cpu-bind=[verbose],<bind type>` option flag of `srun`. The bind option assigns a process to fixed group of _processor units_ for the duration of a job step. Some common options for `<bind type>` are

- `threads`: binds processes to threads,
- `cores`: binds processes to cores,
- `sockets`: binds processes to sockets,
- `map_cpu:<list>`: binds processes to processor unit ranks given in a comma separated `<list>`, and
- `mask_cpu:<list>`: binds processes to groups of processing units defined by _masks_ upon ranks given in a comma separated `<list>`.

You can optionally add the `verbose` option in debugging jobs to print process bindings before the job step runs.

Like with other resources, Slurm is using the [control group](https://www.kernel.org/doc/html/v5.4/admin-guide/cgroup-v1/cgroups.html) feature of Linux to allocate processor units to processes. The base option that controls the allocation of cores is the `mask_cpu`. The other allocation options are converted to mask according to groupings of cores with similar access to resources by the [hardware locality](https://www.open-mpi.org/projects/hwloc/) tool.

#### Mask binding

The basic biding option is the mask option, `mask_cpu:<list>`, all other options are converted to masks according to the site configuration of Slurm.

- The `<mask>` is a bit field over the processor unit ranks (as reported by hardware locality) that marks with 1 the processor units that are available to a process running within a job step.
- The `<list> == <mask>[,<mask>]` option of the binding directive is a comma separated list of masks, each consecutive process of the `srun` command uses the corresponding mask.
- The list is reused if the available masks are exhausted.
- Processes are allowed to move freely within the allocated processor units.

??? info "Hexadecimal notation for masks"

    Masks are written in hexadecimal notation. For instance, assume an allocation on some machine with 2 sockets, 16 cores per socket, and one hardware thread per core. Such an allocation contains 32 processor units (cores). Then, the mask
    ```
    mask_cpu:0xff0000,0xff000000
    ```	
    maps 4 processes to to the following bit fields
    
    | Process number | Processor unit availability               |
    | :------------: | :---------------------------------------- |
    | `0`            | `0000 0000 1111 1111 0000 0000 0000 0000` |
    | `1`            | `1111 1111 0000 0000 0000 0000 0000 0000` |
    | `2`            | `0000 0000 1111 1111 0000 0000 0000 0000` |
    | `3`            | `1111 1111 0000 0000 0000 0000 0000 0000` |

    that in turn constrain

    - task 0 and 2 to run on processor units (hardware threads) 16 to 23 of the node, and
    - task 1 and 3 to run on processor units (hardware threads) 24 to 31 of the node.

    For convenience, you can add leading zeros to a mask so that all masks are of the same length, so, `0x00ff0000 = 0xff0000`.

As an example consider an I/O throughput test for Aion local storage. In Aion there are 8 NUMA nodes per compute node, 4 CCXs per NUMA node, and 4 cores sharing a single L3 cache per CCX. Every digit in the hexadecimal mask controls the availability of a single CCX. To launch an I/O stress test in 4 parallel processes, with

- processes 0 and 2 pinned on CCX 0 of virtual socket 0, and
- processes 1 and 3 pinned on CCX 0 of virtual socket 1

use the following command.

```bash
salloc --nodes=1 --exclusive --partition=batch --qos=normal --time=4:00:00
srun --nodes=1 --ntasks-per-node=4 --cpu-bind=verbose,mask_cpu:0xf,0xf0000 stress --hdd 1 --timeout 240
```

??? note "Context switching within binding regions"

    The HDD stress test processes are I/O heavy and are often interrupted by thread and process context switching. You can login to the running job from another terminal using the `sjoin` alias available in UL HPC systems, and with `htop` you may see the load moving among the allocated cores.

#### Map binding

The map binding binds processes to specific processor units (PUs). The `<list>==<PU rank>[,<PU rank>]` option of the binding directive is a list of processing unit ranks, as reported by hardware locality.

- Processes launched within a job step use the processor unit with corresponding rank.
- Ranks may appear more that once if processing units are shared between processes.
- The list is reused if the available ranks are exhausted.

!!! important "Limitations of map binding"
    Note that with the map binding each process is assigned a single processor unit. If your process needs more that one processor unit, as is the case with multithreaded processes, using another binging option like mask.

As an example consider an I/O throughput test for Aion local storage. In Aion there are 8 NUMA nodes per compute node, with 16 cores per NUMA node. Every digit in the hexadecimal mask controls the availability of a single CCX. To launch an I/O stress test in 4 parallel processes, with

- processes 0 and 1 pinned on cores 0 and 2 of virtual socket 0, and
- processes 2 and 3 pinned on cores 16 and 18 of virtual socket 1

use the following command.

```bash
salloc --nodes=1 --exclusive --partition=batch --qos=normal --time=4:00:00
srun --nodes=1 --ntasks-per-node=4 --cpu-bind=verbose,map_cpu:0,2,16,18 stress --hdd 1 --timeout 240
```

#### Automatically generated masks binding 

The Slurm scheduler provides options to generate bindings automatically. Many systems as MUMPS rely on simple allocations of one MPI process per NUMA node, and OpenMP thread parallelism within NUMA nodes. Automatically generated masks can describe such simple binding efficiently and the resulting description is most often portable between systems.

When using automatic binging users may want to inspect the resulting binding mask. The binding is implemented using [control groups](https://slurm.schedmd.com/cpu_management.html#Step4), so the cores allocated for the process can be inspected with

- the `vorbose` option of binding,
- the `taskset` command, or
- directly reading the `Cpus_allowed_list` in `/proc/self/status`.

As an example consider binding 2 process per node for 2 nodes with the various available options. The `taskset` command is used to report the core bindings, and the verbose option is enabled to print the same information in a format closer to the internal system representation. Start by creating an allocation with exclusive access to 2 nodes:

```bash
salloc --exclusive --nodes=2 --ntasks-per-node=2 --time=1:00:00
```

=== "Threads"

    Simultaneous multi-threading is disabled in our systems, so the `threads` option is not relevant. The _core_ and _processor unit_ (threads) object types of hardware locality coincide.

=== "Cores"

    In this example the processes are pinned to cores of the CPUs.

    - Allow processes to share sockets.
      ```
      $ srun --nodes=2 --ntasks-per-node=2 --cpu-bind=verbose,cores bash -c 'echo -n "task ${SLURM_PROCID} (node ${SLURM_NODEID}): "; taskset --cpu-list --pid ${BASHPID}' | sort
      cpu-bind=MASK - aion-0014, task  0  0 [3431378]: mask 0x1 set
      cpu-bind=MASK - aion-0014, task  1  1 [3431379]: mask 0x2 set
      cpu-bind=MASK - aion-0220, task  2  0 [2549677]: mask 0x1 set
      cpu-bind=MASK - aion-0220, task  3  1 [2549678]: mask 0x2 set
      task 0 (node 0): pid 3431378's current affinity list: 0
      task 1 (node 0): pid 3431379's current affinity list: 1
      task 2 (node 1): pid 2549677's current affinity list: 0
      task 3 (node 1): pid 2549678's current affinity list: 1
      ```

    - Processes pinned with one process per socket.
      ```
      $ srun --nodes=2 --ntasks-per-node=2 --ntasks-per-socket=1 --cpu-bind=verbose,cores bash -c 'echo -n "task ${SLURM_PROCID} (node ${SLURM_NODEID}): "; taskset --cpu-list --pid ${BASHPID}' | sort
      cpu-bind=MASK - aion-0220, task  2  0 [2549899]: mask 0x1 set
      cpu-bind=MASK - aion-0014, task  0  0 [3431621]: mask 0x1 set
      cpu-bind=MASK - aion-0220, task  3  1 [2549900]: mask 0x10000 set
      cpu-bind=MASK - aion-0014, task  1  1 [3431622]: mask 0x10000 set
      task 0 (node 0): pid 3431621's current affinity list: 0
      task 1 (node 0): pid 3431622's current affinity list: 16
      task 2 (node 1): pid 2549899's current affinity list: 0
      task 3 (node 1): pid 2549900's current affinity list: 16
      ```

=== "Sockets"

    In this example the processes are pinned to sockets of the processesing nodes.

    - Allow processes to share sockets (one processor unit per process by default).
      ```
      $ srun --nodes=2 --ntasks-per-node=2 --cpu-bind=verbose,sockets bash -c 'echo -n "task ${SLURM_PROCID} (node ${SLURM_NODEID}): "; taskset --cpu-list --pid ${BASHPID}' | sort
      cpu-bind=MASK - aion-0014, task  0  0 [3431515]: mask 0xffff set
      cpu-bind=MASK - aion-0220, task  2  0 [2549712]: mask 0xffff set
      cpu-bind=MASK - aion-0014, task  1  1 [3431516]: mask 0xffff set
      cpu-bind=MASK - aion-0220, task  3  1 [2549713]: mask 0xffff set
      task 0 (node 0): pid 3431515's current affinity list: 0-15
      task 1 (node 0): pid 3431516's current affinity list: 0-15
      task 2 (node 1): pid 2549712's current affinity list: 0-15
      task 3 (node 1): pid 2549713's current affinity list: 0-15
      ```

    - Processes pinned with one process per socket.
      ```
      $ srun --nodes=2 --ntasks-per-node=2 --ntasks-per-socket=1 --cpu-bind=verbose,sockets bash -c 'echo -n "task ${SLURM_PROCID} (node ${SLURM_NODEID}): "; taskset --cpu-list --pid ${BASHPID}' | sort
      cpu-bind=MASK - aion-0220, task  2  0 [2550128]: mask 0xffff set
      cpu-bind=MASK - aion-0014, task  0  0 [3431908]: mask 0xffff set
      cpu-bind=MASK - aion-0220, task  3  1 [2550129]: mask 0xffff0000 set
      cpu-bind=MASK - aion-0014, task  1  1 [3431909]: mask 0xffff0000 set
      task 0 (node 0): pid 3431908's current affinity list: 0-15
      task 1 (node 0): pid 3431909's current affinity list: 16-31
      task 2 (node 1): pid 2550128's current affinity list: 0-15
      task 3 (node 1): pid 2550129's current affinity list: 16-31
      ```

=== "Custom binding"

    With custom bindings we specify exactly where processes are bound.

    - Pin (single threaded) processes to sockets.
      ```
      $ srun --cpu-bind=verbose,mask_cpu:0xffff,0xffff0000 bash -c 'echo -n "task ${SLURM_PROCID} (node ${SLURM_NODEID})"; taskset --cpu-list --pid ${BASHPID}' | sort
      cpu-bind=MASK - aion-0001, task  0  0 [3535103]: mask 0xffff set
      cpu-bind=MASK - aion-0339, task  2  0 [3595625]: mask 0xffff set
      cpu-bind=MASK - aion-0001, task  1  1 [3535104]: mask 0xffff0000 set
      cpu-bind=MASK - aion-0339, task  3  1 [3595626]: mask 0xffff0000 set
      task 0 (node 0)pid 3535103's current affinity list: 0-15
      task 1 (node 0)pid 3535104's current affinity list: 16-31
      task 2 (node 1)pid 3595625's current affinity list: 0-15
      task 3 (node 1)pid 3595626's current affinity list: 16-31
      ```

    - Pin processes to cores.
      ```
      $ srun --cpu-bind=verbose,mask_cpu:0x1,0x10000 bash -c 'echo -n "task ${SLURM_PROCID} (node ${SLURM_NODEID})"; taskset --cpu-list --pid ${BASHPID}' | sort
      cpu-bind=MASK - aion-0220, task  2  0 [2553408]: mask 0x1 set
      cpu-bind=MASK - aion-0014, task  0  0 [3435289]: mask 0x1 set
      cpu-bind=MASK - aion-0220, task  3  1 [2553409]: mask 0x10000 set
      cpu-bind=MASK - aion-0014, task  1  1 [3435290]: mask 0x10000 set
      task 0 (node 0)pid 3435289's current affinity list: 0
      task 1 (node 0)pid 3435290's current affinity list: 16
      task 2 (node 1)pid 2553408's current affinity list: 0
      task 3 (node 1)pid 2553409's current affinity list: 16
      ```

    Printing the binding information however, demonstrates how processes are spread across nodes. By default, the tasks are distributed in _blocks_, where first the available slots in the first node of the allocation are filled, before moving to the next.

---

An exhaustive [list of reporting features for binding configurations](https://slurm.schedmd.com/cpu_management.html#Section2) can be found in the administrator's guide of Slurm.

??? info "_Resources_"

1. [Configuration options managing the allocation of CPU resources](https://slurm.schedmd.com/cpu_management.html)
2. [Configuration of the control group plugin of Slurm (`cgroup.conf`)](https://slurm.schedmd.com/cgroup.conf.html)

## Examining the architecture of compute nodes

You can extract detailed information for our clusters using the [Portable Hardware Locality (hwloc)](https://www.open-mpi.org/projects/hwloc/) package. The hardware locality modules are provided in UL HPC clusters by the `system/hwloc` [modules](/environment/modules). Let's examine the output of hardware locality in an Iris CPU node and how it is interpreted.

Running the hardware locality is as simple as loading the module and calling the hardware locality program `hwloc-ls`.

=== "Iris CPU nodes"

    1. Allocate a full node in Iris.
       ```bash
       salloc --partition=batch --qos=normal --nodes=1 --ntasks-per-node=1 --cpus-per-task=28
       ```
    2. Load the hardware locality module.
       ```bash
       module load system/hwloc
       ```
    3. Run the hardware locality program `hwloc-ls`.
       ```
       hwloc-ls
       ```

    ??? tip "The output of `hwloc-ls`"
        ```
        $ hwloc-ls
        Machine (126GB total)
          Package L#0
            NUMANode L#0 (P#0 63GB)
            L3 L#0 (35MB)
              L2 L#0 (256KB) + L1d L#0 (32KB) + L1i L#0 (32KB) + Core L#0 + PU L#0 (P#0)
              L2 L#1 (256KB) + L1d L#1 (32KB) + L1i L#1 (32KB) + Core L#1 + PU L#1 (P#2)
              L2 L#2 (256KB) + L1d L#2 (32KB) + L1i L#2 (32KB) + Core L#2 + PU L#2 (P#4)
              L2 L#3 (256KB) + L1d L#3 (32KB) + L1i L#3 (32KB) + Core L#3 + PU L#3 (P#6)
              L2 L#4 (256KB) + L1d L#4 (32KB) + L1i L#4 (32KB) + Core L#4 + PU L#4 (P#8)
              L2 L#5 (256KB) + L1d L#5 (32KB) + L1i L#5 (32KB) + Core L#5 + PU L#5 (P#10)
              L2 L#6 (256KB) + L1d L#6 (32KB) + L1i L#6 (32KB) + Core L#6 + PU L#6 (P#12)
              L2 L#7 (256KB) + L1d L#7 (32KB) + L1i L#7 (32KB) + Core L#7 + PU L#7 (P#14)
              L2 L#8 (256KB) + L1d L#8 (32KB) + L1i L#8 (32KB) + Core L#8 + PU L#8 (P#16)
              L2 L#9 (256KB) + L1d L#9 (32KB) + L1i L#9 (32KB) + Core L#9 + PU L#9 (P#18)
              L2 L#10 (256KB) + L1d L#10 (32KB) + L1i L#10 (32KB) + Core L#10 + PU L#10 (P#20)
              L2 L#11 (256KB) + L1d L#11 (32KB) + L1i L#11 (32KB) + Core L#11 + PU L#11 (P#22)
              L2 L#12 (256KB) + L1d L#12 (32KB) + L1i L#12 (32KB) + Core L#12 + PU L#12 (P#24)
              L2 L#13 (256KB) + L1d L#13 (32KB) + L1i L#13 (32KB) + Core L#13 + PU L#13 (P#26)
            HostBridge
              PCIBridge
                PCI 01:00.0 (InfiniBand)
                  Net "ib0"
                  OpenFabrics "mlx5_0"
              PCIBridge
                PCIBridge
                  PCIBridge
                    PCIBridge
                      PCI 08:00.0 (VGA)
              PCI 00:1f.2 (SATA)
                Block(Disk) "sda"
          Package L#1
            NUMANode L#1 (P#1 63GB)
            L3 L#1 (35MB)
              L2 L#14 (256KB) + L1d L#14 (32KB) + L1i L#14 (32KB) + Core L#14 + PU L#14 (P#1)
              L2 L#15 (256KB) + L1d L#15 (32KB) + L1i L#15 (32KB) + Core L#15 + PU L#15 (P#3)
              L2 L#16 (256KB) + L1d L#16 (32KB) + L1i L#16 (32KB) + Core L#16 + PU L#16 (P#5)
              L2 L#17 (256KB) + L1d L#17 (32KB) + L1i L#17 (32KB) + Core L#17 + PU L#17 (P#7)
              L2 L#18 (256KB) + L1d L#18 (32KB) + L1i L#18 (32KB) + Core L#18 + PU L#18 (P#9)
              L2 L#19 (256KB) + L1d L#19 (32KB) + L1i L#19 (32KB) + Core L#19 + PU L#19 (P#11)
              L2 L#20 (256KB) + L1d L#20 (32KB) + L1i L#20 (32KB) + Core L#20 + PU L#20 (P#13)
              L2 L#21 (256KB) + L1d L#21 (32KB) + L1i L#21 (32KB) + Core L#21 + PU L#21 (P#15)
              L2 L#22 (256KB) + L1d L#22 (32KB) + L1i L#22 (32KB) + Core L#22 + PU L#22 (P#17)
              L2 L#23 (256KB) + L1d L#23 (32KB) + L1i L#23 (32KB) + Core L#23 + PU L#23 (P#19)
              L2 L#24 (256KB) + L1d L#24 (32KB) + L1i L#24 (32KB) + Core L#24 + PU L#24 (P#21)
              L2 L#25 (256KB) + L1d L#25 (32KB) + L1i L#25 (32KB) + Core L#25 + PU L#25 (P#23)
              L2 L#26 (256KB) + L1d L#26 (32KB) + L1i L#26 (32KB) + Core L#26 + PU L#26 (P#25)
              L2 L#27 (256KB) + L1d L#27 (32KB) + L1i L#27 (32KB) + Core L#27 + PU L#27 (P#27)
            HostBridge
              PCIBridge
                PCI 81:00.0 (Ethernet)
                  Net "eno1"
                PCI 81:00.1 (Ethernet)
                  Net "eno2"
        ```

    From the output you can see the following in an Iris CPU node.

    - There are 2 sockets in a node (`Package`).
    - There is a single NUMA node with `63GB` and a single L3 cache per socket.
    - There are 12 cores per L3 cache group.
    - There is a single processor unit (`PU`), also known as hardware thread, per core.
    - The storage (`sda`) and the fast interconnect adaptor (`mlx5_0`) are attached to socket 0 (`Package L#0`).

=== "Iris GPU nodes"

    1. Allocate a full node in Iris.
       ```bash
       salloc --partition=gpu --qos=normal --nodes=1 --ntasks-per-node=1 --cpus-per-task=28 --gpus-per-task=4
       ```
    2. Load the hardware locality module.
       ```bash
       module load system/hwloc
       ```
    3. Run the hardware locality program `hwloc-ls`.
       ```
       hwloc-ls
       ```

    ??? tip "The output of `hwloc-ls`"
        ```
        Machine (755GB total)
          Package L#0
            NUMANode L#0 (P#0 377GB)
            L3 L#0 (19MB)
              L2 L#0 (1024KB) + L1d L#0 (32KB) + L1i L#0 (32KB) + Core L#0 + PU L#0 (P#0)
              L2 L#1 (1024KB) + L1d L#1 (32KB) + L1i L#1 (32KB) + Core L#1 + PU L#1 (P#2)
              L2 L#2 (1024KB) + L1d L#2 (32KB) + L1i L#2 (32KB) + Core L#2 + PU L#2 (P#4)
              L2 L#3 (1024KB) + L1d L#3 (32KB) + L1i L#3 (32KB) + Core L#3 + PU L#3 (P#6)
              L2 L#4 (1024KB) + L1d L#4 (32KB) + L1i L#4 (32KB) + Core L#4 + PU L#4 (P#8)
              L2 L#5 (1024KB) + L1d L#5 (32KB) + L1i L#5 (32KB) + Core L#5 + PU L#5 (P#10)
              L2 L#6 (1024KB) + L1d L#6 (32KB) + L1i L#6 (32KB) + Core L#6 + PU L#6 (P#12)
              L2 L#7 (1024KB) + L1d L#7 (32KB) + L1i L#7 (32KB) + Core L#7 + PU L#7 (P#14)
              L2 L#8 (1024KB) + L1d L#8 (32KB) + L1i L#8 (32KB) + Core L#8 + PU L#8 (P#16)
              L2 L#9 (1024KB) + L1d L#9 (32KB) + L1i L#9 (32KB) + Core L#9 + PU L#9 (P#18)
              L2 L#10 (1024KB) + L1d L#10 (32KB) + L1i L#10 (32KB) + Core L#10 + PU L#10 (P#20)
              L2 L#11 (1024KB) + L1d L#11 (32KB) + L1i L#11 (32KB) + Core L#11 + PU L#11 (P#22)
              L2 L#12 (1024KB) + L1d L#12 (32KB) + L1i L#12 (32KB) + Core L#12 + PU L#12 (P#24)
              L2 L#13 (1024KB) + L1d L#13 (32KB) + L1i L#13 (32KB) + Core L#13 + PU L#13 (P#26)
            HostBridge
              PCI 00:11.5 (SATA)
              PCIBridge
                PCI 01:00.0 (Ethernet)
                  Net "eno3"
                PCI 01:00.1 (Ethernet)
                  Net "eno4"
              PCIBridge
                PCIBridge
                  PCI 03:00.0 (VGA)
              PCIBridge
                PCI 04:00.0 (SATA)
                  Block(Disk) "sda"
              PCIBridge
                PCI 05:00.0 (Ethernet)
                  Net "eno1"
                PCI 05:00.1 (Ethernet)
                  Net "eno2"
            HostBridge
              PCIBridge
                PCIBridge
                  PCIBridge
                    PCI 1a:00.0 (3D)
                  PCIBridge
                    PCI 1c:00.0 (3D)
                  PCIBridge
                    PCI 1d:00.0 (3D)
                  PCIBridge
                    PCI 1e:00.0 (3D)
            HostBridge
              PCIBridge
                PCI 5e:00.0 (InfiniBand)
                  Net "ib0"
                  OpenFabrics "mlx5_0"
                PCI 5e:00.1 (InfiniBand)
                  Net "ib1"
                  OpenFabrics "mlx5_1"
          Package L#1
            NUMANode L#1 (P#1 378GB)
            L3 L#1 (19MB)
              L2 L#14 (1024KB) + L1d L#14 (32KB) + L1i L#14 (32KB) + Core L#14 + PU L#14 (P#1)
              L2 L#15 (1024KB) + L1d L#15 (32KB) + L1i L#15 (32KB) + Core L#15 + PU L#15 (P#3)
              L2 L#16 (1024KB) + L1d L#16 (32KB) + L1i L#16 (32KB) + Core L#16 + PU L#16 (P#5)
              L2 L#17 (1024KB) + L1d L#17 (32KB) + L1i L#17 (32KB) + Core L#17 + PU L#17 (P#7)
              L2 L#18 (1024KB) + L1d L#18 (32KB) + L1i L#18 (32KB) + Core L#18 + PU L#18 (P#9)
              L2 L#19 (1024KB) + L1d L#19 (32KB) + L1i L#19 (32KB) + Core L#19 + PU L#19 (P#11)
              L2 L#20 (1024KB) + L1d L#20 (32KB) + L1i L#20 (32KB) + Core L#20 + PU L#20 (P#13)
              L2 L#21 (1024KB) + L1d L#21 (32KB) + L1i L#21 (32KB) + Core L#21 + PU L#21 (P#15)
              L2 L#22 (1024KB) + L1d L#22 (32KB) + L1i L#22 (32KB) + Core L#22 + PU L#22 (P#17)
              L2 L#23 (1024KB) + L1d L#23 (32KB) + L1i L#23 (32KB) + Core L#23 + PU L#23 (P#19)
              L2 L#24 (1024KB) + L1d L#24 (32KB) + L1i L#24 (32KB) + Core L#24 + PU L#24 (P#21)
              L2 L#25 (1024KB) + L1d L#25 (32KB) + L1i L#25 (32KB) + Core L#25 + PU L#25 (P#23)
              L2 L#26 (1024KB) + L1d L#26 (32KB) + L1i L#26 (32KB) + Core L#26 + PU L#26 (P#25)
              L2 L#27 (1024KB) + L1d L#27 (32KB) + L1i L#27 (32KB) + Core L#27 + PU L#27 (P#27)
            HostBridge
              PCIBridge
                PCI d8:00.0 (NVMExp)
                  Block(Disk) "nvme0n1"
        ```

    From the output you can see the following in an Iris CPU node.

    - There are 2 sockets in a node (`Package`).
    - There is a single NUMA node with `378GB` and a single L3 cache per socket.
    - There are 12 cores per L3 cache group.
    - There is a single processor unit (`PU`), also known as hardware thread, per core.
    - There are 4 GPUs attached to socket 0 (`Package L#0`) through PCIe (`PCIBridge`).
    - The fast interconnect adaptor (`mlx5_0`) is also attached to socket 0.
    - The storage (`nvme0n1`) is attached to socket 1.

=== "Iris Bigmem nodes"

    1. Allocate a full node in Iris.
       ```bash
       salloc --partition=bigmem --qos=normal --nodes=1 --ntasks-per-node=1 --cpus-per-task=112
       ```
    2. Load the hardware locality module.
       ```bash
       module load system/hwloc
       ```
    3. Run the hardware locality program `hwloc-ls`.
       ```
       hwloc-ls
       ```

    ??? tip "The output of `hwloc-ls`"
        ```
        Machine (3022GB total)
          Package L#0
            NUMANode L#0 (P#0 754GB)
            L3 L#0 (39MB)
              L2 L#0 (1024KB) + L1d L#0 (32KB) + L1i L#0 (32KB) + Core L#0 + PU L#0 (P#0)
              L2 L#1 (1024KB) + L1d L#1 (32KB) + L1i L#1 (32KB) + Core L#1 + PU L#1 (P#4)
              L2 L#2 (1024KB) + L1d L#2 (32KB) + L1i L#2 (32KB) + Core L#2 + PU L#2 (P#8)
              L2 L#3 (1024KB) + L1d L#3 (32KB) + L1i L#3 (32KB) + Core L#3 + PU L#3 (P#12)
              L2 L#4 (1024KB) + L1d L#4 (32KB) + L1i L#4 (32KB) + Core L#4 + PU L#4 (P#16)
              L2 L#5 (1024KB) + L1d L#5 (32KB) + L1i L#5 (32KB) + Core L#5 + PU L#5 (P#20)
              L2 L#6 (1024KB) + L1d L#6 (32KB) + L1i L#6 (32KB) + Core L#6 + PU L#6 (P#24)
              L2 L#7 (1024KB) + L1d L#7 (32KB) + L1i L#7 (32KB) + Core L#7 + PU L#7 (P#28)
              L2 L#8 (1024KB) + L1d L#8 (32KB) + L1i L#8 (32KB) + Core L#8 + PU L#8 (P#32)
              L2 L#9 (1024KB) + L1d L#9 (32KB) + L1i L#9 (32KB) + Core L#9 + PU L#9 (P#36)
              L2 L#10 (1024KB) + L1d L#10 (32KB) + L1i L#10 (32KB) + Core L#10 + PU L#10 (P#40)
              L2 L#11 (1024KB) + L1d L#11 (32KB) + L1i L#11 (32KB) + Core L#11 + PU L#11 (P#44)
              L2 L#12 (1024KB) + L1d L#12 (32KB) + L1i L#12 (32KB) + Core L#12 + PU L#12 (P#48)
              L2 L#13 (1024KB) + L1d L#13 (32KB) + L1i L#13 (32KB) + Core L#13 + PU L#13 (P#52)
              L2 L#14 (1024KB) + L1d L#14 (32KB) + L1i L#14 (32KB) + Core L#14 + PU L#14 (P#56)
              L2 L#15 (1024KB) + L1d L#15 (32KB) + L1i L#15 (32KB) + Core L#15 + PU L#15 (P#60)
              L2 L#16 (1024KB) + L1d L#16 (32KB) + L1i L#16 (32KB) + Core L#16 + PU L#16 (P#64)
              L2 L#17 (1024KB) + L1d L#17 (32KB) + L1i L#17 (32KB) + Core L#17 + PU L#17 (P#68)
              L2 L#18 (1024KB) + L1d L#18 (32KB) + L1i L#18 (32KB) + Core L#18 + PU L#18 (P#72)
              L2 L#19 (1024KB) + L1d L#19 (32KB) + L1i L#19 (32KB) + Core L#19 + PU L#19 (P#76)
              L2 L#20 (1024KB) + L1d L#20 (32KB) + L1i L#20 (32KB) + Core L#20 + PU L#20 (P#80)
              L2 L#21 (1024KB) + L1d L#21 (32KB) + L1i L#21 (32KB) + Core L#21 + PU L#21 (P#84)
              L2 L#22 (1024KB) + L1d L#22 (32KB) + L1i L#22 (32KB) + Core L#22 + PU L#22 (P#88)
              L2 L#23 (1024KB) + L1d L#23 (32KB) + L1i L#23 (32KB) + Core L#23 + PU L#23 (P#92)
              L2 L#24 (1024KB) + L1d L#24 (32KB) + L1i L#24 (32KB) + Core L#24 + PU L#24 (P#96)
              L2 L#25 (1024KB) + L1d L#25 (32KB) + L1i L#25 (32KB) + Core L#25 + PU L#25 (P#100)
              L2 L#26 (1024KB) + L1d L#26 (32KB) + L1i L#26 (32KB) + Core L#26 + PU L#26 (P#104)
              L2 L#27 (1024KB) + L1d L#27 (32KB) + L1i L#27 (32KB) + Core L#27 + PU L#27 (P#108)
            HostBridge
              PCI 00:11.5 (SATA)
              PCI 00:17.0 (SATA)
              PCIBridge
                PCI 01:00.0 (Ethernet)
                  Net "eth0"
                PCI 01:00.1 (Ethernet)
                  Net "eth2"
              PCIBridge
                PCIBridge
                  PCI 03:00.0 (VGA)
            HostBridge
              PCIBridge
                PCI 17:00.0 (Ethernet)
                  Net "eth1"
                PCI 17:00.1 (Ethernet)
                  Net "eth3"
            HostBridge
              PCIBridge
                PCI 33:00.0 (InfiniBand)
                  Net "ib0"
                  OpenFabrics "mlx5_0"
                PCI 33:00.1 (InfiniBand)
                  Net "ib1"
                  OpenFabrics "mlx5_1"
          Package L#1
            NUMANode L#1 (P#1 756GB)
            L3 L#1 (39MB)
              L2 L#28 (1024KB) + L1d L#28 (32KB) + L1i L#28 (32KB) + Core L#28 + PU L#28 (P#1)
              L2 L#29 (1024KB) + L1d L#29 (32KB) + L1i L#29 (32KB) + Core L#29 + PU L#29 (P#5)
              L2 L#30 (1024KB) + L1d L#30 (32KB) + L1i L#30 (32KB) + Core L#30 + PU L#30 (P#9)
              L2 L#31 (1024KB) + L1d L#31 (32KB) + L1i L#31 (32KB) + Core L#31 + PU L#31 (P#13)
              L2 L#32 (1024KB) + L1d L#32 (32KB) + L1i L#32 (32KB) + Core L#32 + PU L#32 (P#17)
              L2 L#33 (1024KB) + L1d L#33 (32KB) + L1i L#33 (32KB) + Core L#33 + PU L#33 (P#21)
              L2 L#34 (1024KB) + L1d L#34 (32KB) + L1i L#34 (32KB) + Core L#34 + PU L#34 (P#25)
              L2 L#35 (1024KB) + L1d L#35 (32KB) + L1i L#35 (32KB) + Core L#35 + PU L#35 (P#29)
              L2 L#36 (1024KB) + L1d L#36 (32KB) + L1i L#36 (32KB) + Core L#36 + PU L#36 (P#33)
              L2 L#37 (1024KB) + L1d L#37 (32KB) + L1i L#37 (32KB) + Core L#37 + PU L#37 (P#37)
              L2 L#38 (1024KB) + L1d L#38 (32KB) + L1i L#38 (32KB) + Core L#38 + PU L#38 (P#41)
              L2 L#39 (1024KB) + L1d L#39 (32KB) + L1i L#39 (32KB) + Core L#39 + PU L#39 (P#45)
              L2 L#40 (1024KB) + L1d L#40 (32KB) + L1i L#40 (32KB) + Core L#40 + PU L#40 (P#49)
              L2 L#41 (1024KB) + L1d L#41 (32KB) + L1i L#41 (32KB) + Core L#41 + PU L#41 (P#53)
              L2 L#42 (1024KB) + L1d L#42 (32KB) + L1i L#42 (32KB) + Core L#42 + PU L#42 (P#57)
              L2 L#43 (1024KB) + L1d L#43 (32KB) + L1i L#43 (32KB) + Core L#43 + PU L#43 (P#61)
              L2 L#44 (1024KB) + L1d L#44 (32KB) + L1i L#44 (32KB) + Core L#44 + PU L#44 (P#65)
              L2 L#45 (1024KB) + L1d L#45 (32KB) + L1i L#45 (32KB) + Core L#45 + PU L#45 (P#69)
              L2 L#46 (1024KB) + L1d L#46 (32KB) + L1i L#46 (32KB) + Core L#46 + PU L#46 (P#73)
              L2 L#47 (1024KB) + L1d L#47 (32KB) + L1i L#47 (32KB) + Core L#47 + PU L#47 (P#77)
              L2 L#48 (1024KB) + L1d L#48 (32KB) + L1i L#48 (32KB) + Core L#48 + PU L#48 (P#81)
              L2 L#49 (1024KB) + L1d L#49 (32KB) + L1i L#49 (32KB) + Core L#49 + PU L#49 (P#85)
              L2 L#50 (1024KB) + L1d L#50 (32KB) + L1i L#50 (32KB) + Core L#50 + PU L#50 (P#89)
              L2 L#51 (1024KB) + L1d L#51 (32KB) + L1i L#51 (32KB) + Core L#51 + PU L#51 (P#93)
              L2 L#52 (1024KB) + L1d L#52 (32KB) + L1i L#52 (32KB) + Core L#52 + PU L#52 (P#97)
              L2 L#53 (1024KB) + L1d L#53 (32KB) + L1i L#53 (32KB) + Core L#53 + PU L#53 (P#101)
              L2 L#54 (1024KB) + L1d L#54 (32KB) + L1i L#54 (32KB) + Core L#54 + PU L#54 (P#105)
              L2 L#55 (1024KB) + L1d L#55 (32KB) + L1i L#55 (32KB) + Core L#55 + PU L#55 (P#109)
            HostBridge
              PCIBridge
                PCI 48:00.0 (NVMExp)
                  Block(Disk) "nvme0n1"
          Package L#2
            NUMANode L#2 (P#2 756GB)
            L3 L#2 (39MB)
              L2 L#56 (1024KB) + L1d L#56 (32KB) + L1i L#56 (32KB) + Core L#56 + PU L#56 (P#2)
              L2 L#57 (1024KB) + L1d L#57 (32KB) + L1i L#57 (32KB) + Core L#57 + PU L#57 (P#6)
              L2 L#58 (1024KB) + L1d L#58 (32KB) + L1i L#58 (32KB) + Core L#58 + PU L#58 (P#10)
              L2 L#59 (1024KB) + L1d L#59 (32KB) + L1i L#59 (32KB) + Core L#59 + PU L#59 (P#14)
              L2 L#60 (1024KB) + L1d L#60 (32KB) + L1i L#60 (32KB) + Core L#60 + PU L#60 (P#18)
              L2 L#61 (1024KB) + L1d L#61 (32KB) + L1i L#61 (32KB) + Core L#61 + PU L#61 (P#22)
              L2 L#62 (1024KB) + L1d L#62 (32KB) + L1i L#62 (32KB) + Core L#62 + PU L#62 (P#26)
              L2 L#63 (1024KB) + L1d L#63 (32KB) + L1i L#63 (32KB) + Core L#63 + PU L#63 (P#30)
              L2 L#64 (1024KB) + L1d L#64 (32KB) + L1i L#64 (32KB) + Core L#64 + PU L#64 (P#34)
              L2 L#65 (1024KB) + L1d L#65 (32KB) + L1i L#65 (32KB) + Core L#65 + PU L#65 (P#38)
              L2 L#66 (1024KB) + L1d L#66 (32KB) + L1i L#66 (32KB) + Core L#66 + PU L#66 (P#42)
              L2 L#67 (1024KB) + L1d L#67 (32KB) + L1i L#67 (32KB) + Core L#67 + PU L#67 (P#46)
              L2 L#68 (1024KB) + L1d L#68 (32KB) + L1i L#68 (32KB) + Core L#68 + PU L#68 (P#50)
              L2 L#69 (1024KB) + L1d L#69 (32KB) + L1i L#69 (32KB) + Core L#69 + PU L#69 (P#54)
              L2 L#70 (1024KB) + L1d L#70 (32KB) + L1i L#70 (32KB) + Core L#70 + PU L#70 (P#58)
              L2 L#71 (1024KB) + L1d L#71 (32KB) + L1i L#71 (32KB) + Core L#71 + PU L#71 (P#62)
              L2 L#72 (1024KB) + L1d L#72 (32KB) + L1i L#72 (32KB) + Core L#72 + PU L#72 (P#66)
              L2 L#73 (1024KB) + L1d L#73 (32KB) + L1i L#73 (32KB) + Core L#73 + PU L#73 (P#70)
              L2 L#74 (1024KB) + L1d L#74 (32KB) + L1i L#74 (32KB) + Core L#74 + PU L#74 (P#74)
              L2 L#75 (1024KB) + L1d L#75 (32KB) + L1i L#75 (32KB) + Core L#75 + PU L#75 (P#78)
              L2 L#76 (1024KB) + L1d L#76 (32KB) + L1i L#76 (32KB) + Core L#76 + PU L#76 (P#82)
              L2 L#77 (1024KB) + L1d L#77 (32KB) + L1i L#77 (32KB) + Core L#77 + PU L#77 (P#86)
              L2 L#78 (1024KB) + L1d L#78 (32KB) + L1i L#78 (32KB) + Core L#78 + PU L#78 (P#90)
              L2 L#79 (1024KB) + L1d L#79 (32KB) + L1i L#79 (32KB) + Core L#79 + PU L#79 (P#94)
              L2 L#80 (1024KB) + L1d L#80 (32KB) + L1i L#80 (32KB) + Core L#80 + PU L#80 (P#98)
              L2 L#81 (1024KB) + L1d L#81 (32KB) + L1i L#81 (32KB) + Core L#81 + PU L#81 (P#102)
              L2 L#82 (1024KB) + L1d L#82 (32KB) + L1i L#82 (32KB) + Core L#82 + PU L#82 (P#106)
              L2 L#83 (1024KB) + L1d L#83 (32KB) + L1i L#83 (32KB) + Core L#83 + PU L#83 (P#110)
          Package L#3
            NUMANode L#3 (P#3 756GB)
            L3 L#3 (39MB)
              L2 L#84 (1024KB) + L1d L#84 (32KB) + L1i L#84 (32KB) + Core L#84 + PU L#84 (P#3)
              L2 L#85 (1024KB) + L1d L#85 (32KB) + L1i L#85 (32KB) + Core L#85 + PU L#85 (P#7)
              L2 L#86 (1024KB) + L1d L#86 (32KB) + L1i L#86 (32KB) + Core L#86 + PU L#86 (P#11)
              L2 L#87 (1024KB) + L1d L#87 (32KB) + L1i L#87 (32KB) + Core L#87 + PU L#87 (P#15)
              L2 L#88 (1024KB) + L1d L#88 (32KB) + L1i L#88 (32KB) + Core L#88 + PU L#88 (P#19)
              L2 L#89 (1024KB) + L1d L#89 (32KB) + L1i L#89 (32KB) + Core L#89 + PU L#89 (P#23)
              L2 L#90 (1024KB) + L1d L#90 (32KB) + L1i L#90 (32KB) + Core L#90 + PU L#90 (P#27)
              L2 L#91 (1024KB) + L1d L#91 (32KB) + L1i L#91 (32KB) + Core L#91 + PU L#91 (P#31)
              L2 L#92 (1024KB) + L1d L#92 (32KB) + L1i L#92 (32KB) + Core L#92 + PU L#92 (P#35)
              L2 L#93 (1024KB) + L1d L#93 (32KB) + L1i L#93 (32KB) + Core L#93 + PU L#93 (P#39)
              L2 L#94 (1024KB) + L1d L#94 (32KB) + L1i L#94 (32KB) + Core L#94 + PU L#94 (P#43)
              L2 L#95 (1024KB) + L1d L#95 (32KB) + L1i L#95 (32KB) + Core L#95 + PU L#95 (P#47)
              L2 L#96 (1024KB) + L1d L#96 (32KB) + L1i L#96 (32KB) + Core L#96 + PU L#96 (P#51)
              L2 L#97 (1024KB) + L1d L#97 (32KB) + L1i L#97 (32KB) + Core L#97 + PU L#97 (P#55)
              L2 L#98 (1024KB) + L1d L#98 (32KB) + L1i L#98 (32KB) + Core L#98 + PU L#98 (P#59)
              L2 L#99 (1024KB) + L1d L#99 (32KB) + L1i L#99 (32KB) + Core L#99 + PU L#99 (P#63)
              L2 L#100 (1024KB) + L1d L#100 (32KB) + L1i L#100 (32KB) + Core L#100 + PU L#100 (P#67)
              L2 L#101 (1024KB) + L1d L#101 (32KB) + L1i L#101 (32KB) + Core L#101 + PU L#101 (P#71)
              L2 L#102 (1024KB) + L1d L#102 (32KB) + L1i L#102 (32KB) + Core L#102 + PU L#102 (P#75)
              L2 L#103 (1024KB) + L1d L#103 (32KB) + L1i L#103 (32KB) + Core L#103 + PU L#103 (P#79)
              L2 L#104 (1024KB) + L1d L#104 (32KB) + L1i L#104 (32KB) + Core L#104 + PU L#104 (P#83)
              L2 L#105 (1024KB) + L1d L#105 (32KB) + L1i L#105 (32KB) + Core L#105 + PU L#105 (P#87)
              L2 L#106 (1024KB) + L1d L#106 (32KB) + L1i L#106 (32KB) + Core L#106 + PU L#106 (P#91)
              L2 L#107 (1024KB) + L1d L#107 (32KB) + L1i L#107 (32KB) + Core L#107 + PU L#107 (P#95)
              L2 L#108 (1024KB) + L1d L#108 (32KB) + L1i L#108 (32KB) + Core L#108 + PU L#108 (P#99)
              L2 L#109 (1024KB) + L1d L#109 (32KB) + L1i L#109 (32KB) + Core L#109 + PU L#109 (P#103)
              L2 L#110 (1024KB) + L1d L#110 (32KB) + L1i L#110 (32KB) + Core L#110 + PU L#110 (P#107)
              L2 L#111 (1024KB) + L1d L#111 (32KB) + L1i L#111 (32KB) + Core L#111 + PU L#111 (P#111)
        ```

    From the output you can see the following in an Iris CPU node.

    - There are 4 sockets in a node (`Package`).
    - There is a single NUMA node with `754GB` and a single L3 cache per socket.
    - There are 12 cores per L3 cache group.
    - There is a single processor unit (`PU`), also known as hardware thread, per core.
    - There are 2 fast interconnect adaptors (`mlx5_0` and `mlx5_1`) attached to socket 0 (`Package L#0`).
    - The storage (`nvme0n1`) is attached to socket 1.


=== "Aion CPU nodes"

    1. Allocate a full node in Aion.
       ```bash
       salloc --partition=batch --qos=normal --nodes=1 --ntasks-per-node=1 --cpus-per-task=128
       ```
    2. Load the hardware locality module.
       ```bash
       module load system/hwloc
       ```
    3. Run the hardware locality program `hwloc-ls`.
       ```
       hwloc-ls
       ```

    ??? tip "The output of `hwloc-ls`"
        ```
        $ hwloc-ls
        Machine (251GB total)
          Package L#0
            Group0 L#0
              NUMANode L#0 (P#0 31GB)
              L3 L#0 (16MB)
                L2 L#0 (512KB) + L1d L#0 (32KB) + L1i L#0 (32KB) + Core L#0 + PU L#0 (P#0)
                L2 L#1 (512KB) + L1d L#1 (32KB) + L1i L#1 (32KB) + Core L#1 + PU L#1 (P#1)
                L2 L#2 (512KB) + L1d L#2 (32KB) + L1i L#2 (32KB) + Core L#2 + PU L#2 (P#2)
                L2 L#3 (512KB) + L1d L#3 (32KB) + L1i L#3 (32KB) + Core L#3 + PU L#3 (P#3)
              L3 L#1 (16MB)
                L2 L#4 (512KB) + L1d L#4 (32KB) + L1i L#4 (32KB) + Core L#4 + PU L#4 (P#4)
                L2 L#5 (512KB) + L1d L#5 (32KB) + L1i L#5 (32KB) + Core L#5 + PU L#5 (P#5)
                L2 L#6 (512KB) + L1d L#6 (32KB) + L1i L#6 (32KB) + Core L#6 + PU L#6 (P#6)
                L2 L#7 (512KB) + L1d L#7 (32KB) + L1i L#7 (32KB) + Core L#7 + PU L#7 (P#7)
              L3 L#2 (16MB)
                L2 L#8 (512KB) + L1d L#8 (32KB) + L1i L#8 (32KB) + Core L#8 + PU L#8 (P#8)
                L2 L#9 (512KB) + L1d L#9 (32KB) + L1i L#9 (32KB) + Core L#9 + PU L#9 (P#9)
                L2 L#10 (512KB) + L1d L#10 (32KB) + L1i L#10 (32KB) + Core L#10 + PU L#10 (P#10)
                L2 L#11 (512KB) + L1d L#11 (32KB) + L1i L#11 (32KB) + Core L#11 + PU L#11 (P#11)
              L3 L#3 (16MB)
                L2 L#12 (512KB) + L1d L#12 (32KB) + L1i L#12 (32KB) + Core L#12 + PU L#12 (P#12)
                L2 L#13 (512KB) + L1d L#13 (32KB) + L1i L#13 (32KB) + Core L#13 + PU L#13 (P#13)
                L2 L#14 (512KB) + L1d L#14 (32KB) + L1i L#14 (32KB) + Core L#14 + PU L#14 (P#14)
                L2 L#15 (512KB) + L1d L#15 (32KB) + L1i L#15 (32KB) + Core L#15 + PU L#15 (P#15)
              HostBridge
                PCIBridge
                  PCI 61:00.0 (InfiniBand)
                    Net "ib0"
                    OpenFabrics "mlx5_0"
                PCIBridge
                  PCIBridge
                    PCI 63:00.0 (VGA)
            Group0 L#1
              NUMANode L#1 (P#1 31GB)
              L3 L#4 (16MB)
                L2 L#16 (512KB) + L1d L#16 (32KB) + L1i L#16 (32KB) + Core L#16 + PU L#16 (P#16)
                L2 L#17 (512KB) + L1d L#17 (32KB) + L1i L#17 (32KB) + Core L#17 + PU L#17 (P#17)
                L2 L#18 (512KB) + L1d L#18 (32KB) + L1i L#18 (32KB) + Core L#18 + PU L#18 (P#18)
                L2 L#19 (512KB) + L1d L#19 (32KB) + L1i L#19 (32KB) + Core L#19 + PU L#19 (P#19)
              L3 L#5 (16MB)
                L2 L#20 (512KB) + L1d L#20 (32KB) + L1i L#20 (32KB) + Core L#20 + PU L#20 (P#20)
                L2 L#21 (512KB) + L1d L#21 (32KB) + L1i L#21 (32KB) + Core L#21 + PU L#21 (P#21)
                L2 L#22 (512KB) + L1d L#22 (32KB) + L1i L#22 (32KB) + Core L#22 + PU L#22 (P#22)
                L2 L#23 (512KB) + L1d L#23 (32KB) + L1i L#23 (32KB) + Core L#23 + PU L#23 (P#23)
              L3 L#6 (16MB)
                L2 L#24 (512KB) + L1d L#24 (32KB) + L1i L#24 (32KB) + Core L#24 + PU L#24 (P#24)
                L2 L#25 (512KB) + L1d L#25 (32KB) + L1i L#25 (32KB) + Core L#25 + PU L#25 (P#25)
                L2 L#26 (512KB) + L1d L#26 (32KB) + L1i L#26 (32KB) + Core L#26 + PU L#26 (P#26)
                L2 L#27 (512KB) + L1d L#27 (32KB) + L1i L#27 (32KB) + Core L#27 + PU L#27 (P#27)
              L3 L#7 (16MB)
                L2 L#28 (512KB) + L1d L#28 (32KB) + L1i L#28 (32KB) + Core L#28 + PU L#28 (P#28)
                L2 L#29 (512KB) + L1d L#29 (32KB) + L1i L#29 (32KB) + Core L#29 + PU L#29 (P#29)
                L2 L#30 (512KB) + L1d L#30 (32KB) + L1i L#30 (32KB) + Core L#30 + PU L#30 (P#30)
                L2 L#31 (512KB) + L1d L#31 (32KB) + L1i L#31 (32KB) + Core L#31 + PU L#31 (P#31)
            Group0 L#2
              NUMANode L#2 (P#2 31GB)
              L3 L#8 (16MB)
                L2 L#32 (512KB) + L1d L#32 (32KB) + L1i L#32 (32KB) + Core L#32 + PU L#32 (P#32)
                L2 L#33 (512KB) + L1d L#33 (32KB) + L1i L#33 (32KB) + Core L#33 + PU L#33 (P#33)
                L2 L#34 (512KB) + L1d L#34 (32KB) + L1i L#34 (32KB) + Core L#34 + PU L#34 (P#34)
                L2 L#35 (512KB) + L1d L#35 (32KB) + L1i L#35 (32KB) + Core L#35 + PU L#35 (P#35)
              L3 L#9 (16MB)
                L2 L#36 (512KB) + L1d L#36 (32KB) + L1i L#36 (32KB) + Core L#36 + PU L#36 (P#36)
                L2 L#37 (512KB) + L1d L#37 (32KB) + L1i L#37 (32KB) + Core L#37 + PU L#37 (P#37)
                L2 L#38 (512KB) + L1d L#38 (32KB) + L1i L#38 (32KB) + Core L#38 + PU L#38 (P#38)
                L2 L#39 (512KB) + L1d L#39 (32KB) + L1i L#39 (32KB) + Core L#39 + PU L#39 (P#39)
              L3 L#10 (16MB)
                L2 L#40 (512KB) + L1d L#40 (32KB) + L1i L#40 (32KB) + Core L#40 + PU L#40 (P#40)
                L2 L#41 (512KB) + L1d L#41 (32KB) + L1i L#41 (32KB) + Core L#41 + PU L#41 (P#41)
                L2 L#42 (512KB) + L1d L#42 (32KB) + L1i L#42 (32KB) + Core L#42 + PU L#42 (P#42)
                L2 L#43 (512KB) + L1d L#43 (32KB) + L1i L#43 (32KB) + Core L#43 + PU L#43 (P#43)
              L3 L#11 (16MB)
                L2 L#44 (512KB) + L1d L#44 (32KB) + L1i L#44 (32KB) + Core L#44 + PU L#44 (P#44)
                L2 L#45 (512KB) + L1d L#45 (32KB) + L1i L#45 (32KB) + Core L#45 + PU L#45 (P#45)
                L2 L#46 (512KB) + L1d L#46 (32KB) + L1i L#46 (32KB) + Core L#46 + PU L#46 (P#46)
                L2 L#47 (512KB) + L1d L#47 (32KB) + L1i L#47 (32KB) + Core L#47 + PU L#47 (P#47)
            Group0 L#3
              NUMANode L#3 (P#3 31GB)
              L3 L#12 (16MB)
                L2 L#48 (512KB) + L1d L#48 (32KB) + L1i L#48 (32KB) + Core L#48 + PU L#48 (P#48)
                L2 L#49 (512KB) + L1d L#49 (32KB) + L1i L#49 (32KB) + Core L#49 + PU L#49 (P#49)
                L2 L#50 (512KB) + L1d L#50 (32KB) + L1i L#50 (32KB) + Core L#50 + PU L#50 (P#50)
                L2 L#51 (512KB) + L1d L#51 (32KB) + L1i L#51 (32KB) + Core L#51 + PU L#51 (P#51)
              L3 L#13 (16MB)
                L2 L#52 (512KB) + L1d L#52 (32KB) + L1i L#52 (32KB) + Core L#52 + PU L#52 (P#52)
                L2 L#53 (512KB) + L1d L#53 (32KB) + L1i L#53 (32KB) + Core L#53 + PU L#53 (P#53)
                L2 L#54 (512KB) + L1d L#54 (32KB) + L1i L#54 (32KB) + Core L#54 + PU L#54 (P#54)
                L2 L#55 (512KB) + L1d L#55 (32KB) + L1i L#55 (32KB) + Core L#55 + PU L#55 (P#55)
              L3 L#14 (16MB)
                L2 L#56 (512KB) + L1d L#56 (32KB) + L1i L#56 (32KB) + Core L#56 + PU L#56 (P#56)
                L2 L#57 (512KB) + L1d L#57 (32KB) + L1i L#57 (32KB) + Core L#57 + PU L#57 (P#57)
                L2 L#58 (512KB) + L1d L#58 (32KB) + L1i L#58 (32KB) + Core L#58 + PU L#58 (P#58)
                L2 L#59 (512KB) + L1d L#59 (32KB) + L1i L#59 (32KB) + Core L#59 + PU L#59 (P#59)
              L3 L#15 (16MB)
                L2 L#60 (512KB) + L1d L#60 (32KB) + L1i L#60 (32KB) + Core L#60 + PU L#60 (P#60)
                L2 L#61 (512KB) + L1d L#61 (32KB) + L1i L#61 (32KB) + Core L#61 + PU L#61 (P#61)
                L2 L#62 (512KB) + L1d L#62 (32KB) + L1i L#62 (32KB) + Core L#62 + PU L#62 (P#62)
                L2 L#63 (512KB) + L1d L#63 (32KB) + L1i L#63 (32KB) + Core L#63 + PU L#63 (P#63)
          Package L#1
            Group0 L#4
              NUMANode L#4 (P#4 31GB)
              L3 L#16 (16MB)
                L2 L#64 (512KB) + L1d L#64 (32KB) + L1i L#64 (32KB) + Core L#64 + PU L#64 (P#64)
                L2 L#65 (512KB) + L1d L#65 (32KB) + L1i L#65 (32KB) + Core L#65 + PU L#65 (P#65)
                L2 L#66 (512KB) + L1d L#66 (32KB) + L1i L#66 (32KB) + Core L#66 + PU L#66 (P#66)
                L2 L#67 (512KB) + L1d L#67 (32KB) + L1i L#67 (32KB) + Core L#67 + PU L#67 (P#67)
              L3 L#17 (16MB)
                L2 L#68 (512KB) + L1d L#68 (32KB) + L1i L#68 (32KB) + Core L#68 + PU L#68 (P#68)
                L2 L#69 (512KB) + L1d L#69 (32KB) + L1i L#69 (32KB) + Core L#69 + PU L#69 (P#69)
                L2 L#70 (512KB) + L1d L#70 (32KB) + L1i L#70 (32KB) + Core L#70 + PU L#70 (P#70)
                L2 L#71 (512KB) + L1d L#71 (32KB) + L1i L#71 (32KB) + Core L#71 + PU L#71 (P#71)
              L3 L#18 (16MB)
                L2 L#72 (512KB) + L1d L#72 (32KB) + L1i L#72 (32KB) + Core L#72 + PU L#72 (P#72)
                L2 L#73 (512KB) + L1d L#73 (32KB) + L1i L#73 (32KB) + Core L#73 + PU L#73 (P#73)
                L2 L#74 (512KB) + L1d L#74 (32KB) + L1i L#74 (32KB) + Core L#74 + PU L#74 (P#74)
                L2 L#75 (512KB) + L1d L#75 (32KB) + L1i L#75 (32KB) + Core L#75 + PU L#75 (P#75)
              L3 L#19 (16MB)
                L2 L#76 (512KB) + L1d L#76 (32KB) + L1i L#76 (32KB) + Core L#76 + PU L#76 (P#76)
                L2 L#77 (512KB) + L1d L#77 (32KB) + L1i L#77 (32KB) + Core L#77 + PU L#77 (P#77)
                L2 L#78 (512KB) + L1d L#78 (32KB) + L1i L#78 (32KB) + Core L#78 + PU L#78 (P#78)
                L2 L#79 (512KB) + L1d L#79 (32KB) + L1i L#79 (32KB) + Core L#79 + PU L#79 (P#79)
              HostBridge
                PCIBridge
                  PCI e1:00.0 (Ethernet)
                    Net "enp225s0f0"
                  PCI e1:00.1 (Ethernet)
                    Net "enp225s0f1"
            Group0 L#5
              NUMANode L#5 (P#5 31GB)
              L3 L#20 (16MB)
                L2 L#80 (512KB) + L1d L#80 (32KB) + L1i L#80 (32KB) + Core L#80 + PU L#80 (P#80)
                L2 L#81 (512KB) + L1d L#81 (32KB) + L1i L#81 (32KB) + Core L#81 + PU L#81 (P#81)
                L2 L#82 (512KB) + L1d L#82 (32KB) + L1i L#82 (32KB) + Core L#82 + PU L#82 (P#82)
                L2 L#83 (512KB) + L1d L#83 (32KB) + L1i L#83 (32KB) + Core L#83 + PU L#83 (P#83)
              L3 L#21 (16MB)
                L2 L#84 (512KB) + L1d L#84 (32KB) + L1i L#84 (32KB) + Core L#84 + PU L#84 (P#84)
                L2 L#85 (512KB) + L1d L#85 (32KB) + L1i L#85 (32KB) + Core L#85 + PU L#85 (P#85)
                L2 L#86 (512KB) + L1d L#86 (32KB) + L1i L#86 (32KB) + Core L#86 + PU L#86 (P#86)
                L2 L#87 (512KB) + L1d L#87 (32KB) + L1i L#87 (32KB) + Core L#87 + PU L#87 (P#87)
              L3 L#22 (16MB)
                L2 L#88 (512KB) + L1d L#88 (32KB) + L1i L#88 (32KB) + Core L#88 + PU L#88 (P#88)
                L2 L#89 (512KB) + L1d L#89 (32KB) + L1i L#89 (32KB) + Core L#89 + PU L#89 (P#89)
                L2 L#90 (512KB) + L1d L#90 (32KB) + L1i L#90 (32KB) + Core L#90 + PU L#90 (P#90)
                L2 L#91 (512KB) + L1d L#91 (32KB) + L1i L#91 (32KB) + Core L#91 + PU L#91 (P#91)
              L3 L#23 (16MB)
                L2 L#92 (512KB) + L1d L#92 (32KB) + L1i L#92 (32KB) + Core L#92 + PU L#92 (P#92)
                L2 L#93 (512KB) + L1d L#93 (32KB) + L1i L#93 (32KB) + Core L#93 + PU L#93 (P#93)
                L2 L#94 (512KB) + L1d L#94 (32KB) + L1i L#94 (32KB) + Core L#94 + PU L#94 (P#94)
                L2 L#95 (512KB) + L1d L#95 (32KB) + L1i L#95 (32KB) + Core L#95 + PU L#95 (P#95)
              HostBridge
                PCIBridge
                  PCI c3:00.0 (SATA)
                    Block(Disk) "sda"
            Group0 L#6
              NUMANode L#6 (P#6 31GB)
              L3 L#24 (16MB)
                L2 L#96 (512KB) + L1d L#96 (32KB) + L1i L#96 (32KB) + Core L#96 + PU L#96 (P#96)
                L2 L#97 (512KB) + L1d L#97 (32KB) + L1i L#97 (32KB) + Core L#97 + PU L#97 (P#97)
                L2 L#98 (512KB) + L1d L#98 (32KB) + L1i L#98 (32KB) + Core L#98 + PU L#98 (P#98)
                L2 L#99 (512KB) + L1d L#99 (32KB) + L1i L#99 (32KB) + Core L#99 + PU L#99 (P#99)
              L3 L#25 (16MB)
                L2 L#100 (512KB) + L1d L#100 (32KB) + L1i L#100 (32KB) + Core L#100 + PU L#100 (P#100)
                L2 L#101 (512KB) + L1d L#101 (32KB) + L1i L#101 (32KB) + Core L#101 + PU L#101 (P#101)
                L2 L#102 (512KB) + L1d L#102 (32KB) + L1i L#102 (32KB) + Core L#102 + PU L#102 (P#102)
                L2 L#103 (512KB) + L1d L#103 (32KB) + L1i L#103 (32KB) + Core L#103 + PU L#103 (P#103)
              L3 L#26 (16MB)
                L2 L#104 (512KB) + L1d L#104 (32KB) + L1i L#104 (32KB) + Core L#104 + PU L#104 (P#104)
                L2 L#105 (512KB) + L1d L#105 (32KB) + L1i L#105 (32KB) + Core L#105 + PU L#105 (P#105)
                L2 L#106 (512KB) + L1d L#106 (32KB) + L1i L#106 (32KB) + Core L#106 + PU L#106 (P#106)
                L2 L#107 (512KB) + L1d L#107 (32KB) + L1i L#107 (32KB) + Core L#107 + PU L#107 (P#107)
              L3 L#27 (16MB)
                L2 L#108 (512KB) + L1d L#108 (32KB) + L1i L#108 (32KB) + Core L#108 + PU L#108 (P#108)
                L2 L#109 (512KB) + L1d L#109 (32KB) + L1i L#109 (32KB) + Core L#109 + PU L#109 (P#109)
                L2 L#110 (512KB) + L1d L#110 (32KB) + L1i L#110 (32KB) + Core L#110 + PU L#110 (P#110)
                L2 L#111 (512KB) + L1d L#111 (32KB) + L1i L#111 (32KB) + Core L#111 + PU L#111 (P#111)
            Group0 L#7
              NUMANode L#7 (P#7 31GB)
              L3 L#28 (16MB)
                L2 L#112 (512KB) + L1d L#112 (32KB) + L1i L#112 (32KB) + Core L#112 + PU L#112 (P#112)
                L2 L#113 (512KB) + L1d L#113 (32KB) + L1i L#113 (32KB) + Core L#113 + PU L#113 (P#113)
                L2 L#114 (512KB) + L1d L#114 (32KB) + L1i L#114 (32KB) + Core L#114 + PU L#114 (P#114)
                L2 L#115 (512KB) + L1d L#115 (32KB) + L1i L#115 (32KB) + Core L#115 + PU L#115 (P#115)
              L3 L#29 (16MB)
                L2 L#116 (512KB) + L1d L#116 (32KB) + L1i L#116 (32KB) + Core L#116 + PU L#116 (P#116)
                L2 L#117 (512KB) + L1d L#117 (32KB) + L1i L#117 (32KB) + Core L#117 + PU L#117 (P#117)
                L2 L#118 (512KB) + L1d L#118 (32KB) + L1i L#118 (32KB) + Core L#118 + PU L#118 (P#118)
                L2 L#119 (512KB) + L1d L#119 (32KB) + L1i L#119 (32KB) + Core L#119 + PU L#119 (P#119)
              L3 L#30 (16MB)
                L2 L#120 (512KB) + L1d L#120 (32KB) + L1i L#120 (32KB) + Core L#120 + PU L#120 (P#120)
                L2 L#121 (512KB) + L1d L#121 (32KB) + L1i L#121 (32KB) + Core L#121 + PU L#121 (P#121)
                L2 L#122 (512KB) + L1d L#122 (32KB) + L1i L#122 (32KB) + Core L#122 + PU L#122 (P#122)
                L2 L#123 (512KB) + L1d L#123 (32KB) + L1i L#123 (32KB) + Core L#123 + PU L#123 (P#123)
              L3 L#31 (16MB)
                L2 L#124 (512KB) + L1d L#124 (32KB) + L1i L#124 (32KB) + Core L#124 + PU L#124 (P#124)
                L2 L#125 (512KB) + L1d L#125 (32KB) + L1i L#125 (32KB) + Core L#125 + PU L#125 (P#125)
                L2 L#126 (512KB) + L1d L#126 (32KB) + L1i L#126 (32KB) + Core L#126 + PU L#126 (P#126)
                L2 L#127 (512KB) + L1d L#127 (32KB) + L1i L#127 (32KB) + Core L#127 + PU L#127 (P#127)
        ```

    From the output you can see the following in an Aion node.

    - There are 2 physical sockets in a node (`Package`).
    - There are 8 virtual sockets (`Group0`) in a node, 4 per physical socket.
    - There is a single NUMA node with `32GB` per virtual socket.
    - There are 4 physical L3 caches per NUMA node.
    - There are 4 cores per L3 cache group.
    - There is a single processor unit (`PU`), also known as hardware thread, per core.
    - The fast interconnect adaptor (`mlx5_0`) is attached to virtual socket 0 (`Group0 L#0`).
    - The local storage (`sda`) is attache to virtual socket 5 (`Group0 L#5`).

---

### Hardware locality and cluster allocations

The hardware locality program is aware of the allocation in the cluster. If you request only part of a node, then hardware locality will only display the allocated resources in the node where it is running. For instance allocate a single node in Iris with 2 tasks.
```bash
salloc --partition=batch --qos=normal --nodes=1 --ntasks-per-node=2 --cpus-per-task=14
```
This allocation command allocates a full socket per job by default. Then load the hardware locality module in the allocation for the job.
```bash
module load system/hwloc
```

You can now launch hardware locality in a single task of the allocation.
```bash
srun --ntasks=1 hwloc-ls
```

??? tip "Output of hardware locality for a single task"

    ```
    $ srun --ntasks=1 hwloc-ls
    Machine (126GB total)
      Package L#0
        NUMANode L#0 (P#0 63GB)
        L3 L#0 (35MB)
          L2 L#0 (256KB) + L1d L#0 (32KB) + L1i L#0 (32KB) + Core L#0 + PU L#0 (P#0)
          L2 L#1 (256KB) + L1d L#1 (32KB) + L1i L#1 (32KB) + Core L#1 + PU L#1 (P#2)
          L2 L#2 (256KB) + L1d L#2 (32KB) + L1i L#2 (32KB) + Core L#2 + PU L#2 (P#4)
          L2 L#3 (256KB) + L1d L#3 (32KB) + L1i L#3 (32KB) + Core L#3 + PU L#3 (P#6)
          L2 L#4 (256KB) + L1d L#4 (32KB) + L1i L#4 (32KB) + Core L#4 + PU L#4 (P#8)
          L2 L#5 (256KB) + L1d L#5 (32KB) + L1i L#5 (32KB) + Core L#5 + PU L#5 (P#10)
          L2 L#6 (256KB) + L1d L#6 (32KB) + L1i L#6 (32KB) + Core L#6 + PU L#6 (P#12)
          L2 L#7 (256KB) + L1d L#7 (32KB) + L1i L#7 (32KB) + Core L#7 + PU L#7 (P#14)
          L2 L#8 (256KB) + L1d L#8 (32KB) + L1i L#8 (32KB) + Core L#8 + PU L#8 (P#16)
          L2 L#9 (256KB) + L1d L#9 (32KB) + L1i L#9 (32KB) + Core L#9 + PU L#9 (P#18)
          L2 L#10 (256KB) + L1d L#10 (32KB) + L1i L#10 (32KB) + Core L#10 + PU L#10 (P#20)
          L2 L#11 (256KB) + L1d L#11 (32KB) + L1i L#11 (32KB) + Core L#11 + PU L#11 (P#22)
          L2 L#12 (256KB) + L1d L#12 (32KB) + L1i L#12 (32KB) + Core L#12 + PU L#12 (P#24)
          L2 L#13 (256KB) + L1d L#13 (32KB) + L1i L#13 (32KB) + Core L#13 + PU L#13 (P#26)
        HostBridge
          PCIBridge
            PCI 01:00.0 (InfiniBand)
              Net "ib0"
              OpenFabrics "mlx5_0"
          PCIBridge
            PCIBridge
              PCIBridge
                PCIBridge
                  PCI 08:00.0 (VGA)
          PCI 00:1f.2 (SATA)
            Block(Disk) "sda"
      Package L#1
        NUMANode L#1 (P#1 63GB)
        HostBridge
          PCIBridge
            PCI 81:00.0 (Ethernet)
              Net "eno1"
            PCI 81:00.1 (Ethernet)
              Net "eno2"
    ```

In the output of hardware locality only the cores of the running task are available.

### Object types and relative communication latency

The architectural data extracted by hardware locality are not very useful without any information on how to pin software threads in the processes units of the compute nodes. Fortunately, hardware locality also provides a distance matrix for the communication latency between processor units. Communication latency is reported at the lowest relevant level of an object type hierarchy.

The object types are reported in the verbose output of hardware locality.

```bash
hwloc-ls --verbose
```

In hardware locality interface, _object types_ are an abstraction of the architectural units of organization of the CPU. The finest object type is always the processor unit (`PU`), also known as hardware thread. Each level in the hierarchy consists of objects of the previous level.

!!! info "Object types"

    | Depth | Object     | Description |
    |:-----:|:-----------|:------------|
    | 0     | `Machine`  | The compute node. |
    | 1     | `Package`  | The physical socket. |
    | 2     | `Group0`   | A group of cores (level 0); usually this is an architectural artifact like CCX complexes in Zen architectures. |
    | 3     | `L3Cache`  | The L3 cache. |
    | 4     | `L2Cache`  | The L2 cache. |
    | 5     | `L1dCache` | The L1 data cache. |
    | 6     | `L1iCache` | The L1 instruction cache. |
    | 7     | `Core`     | The physical CPU core. |
    | 8     | `PU`       | The processor unit; corresponds to hardware threads. |

There are also _special object types_ that correspond to groups of processor units with uniform access to some resource such as memory channels or peripheral devices such as storage or network cards. For instance NUMA nodes are groups of cores that have access to the same memory channels in Zen2 architecture, and `PCIDev` is a peripheral PCIe device such as a GPU or network card.

!!! info "Special object types"

    | Depth | Object      | Description |
    |:-----:|:------------|:------------|
    | -3    | `NUMANode`  | A group of cores with access to the same memory channels |
    | -4    | `PCIBridge` | A group of cores that have direct access to a PICe connection. |
    | -5    | `PCIDev`    | A generic PCIe device, such as interconnect cards; connects to a `PCIBridge`. |

Hardware locality provides an estimate of the relative latency between processor units. For the reporting purposes, processor units are group to the highest level in the object type hierarchy were communication latency is still uniform within the group; cores are usually grouped into NUMA nodes. To output latency information use the `--distances` option flag.

```bash
hwloc-ls --distances
```

This option produces a matrix of distances between an object type of the architecture. The unit of the reported values is arbitrary, the important quantity is the ratio between the various values.

??? info "Distance matrix for Aion compute nodes"

    ```
    $ hwloc-ls --distances
    Relative latency matrix (name NUMALatency kind 5) between 8 NUMANodes (depth -3) by logical indexes:
     index     0     1     2     3     4     5     6     7
         0    10    12    12    12    32    32    32    32
         1    12    10    12    12    32    32    32    32
         2    12    12    10    12    32    32    32    32
         3    12    12    12    10    32    32    32    32
         4    32    32    32    32    10    12    12    12
         5    32    32    32    32    12    10    12    12
         6    32    32    32    32    12    12    10    12
         7    32    32    32    32    12    12    12    10
    ```

??? info "Distance matrix for Iris CPU and GPU compute nodes"

    ```
    $ hwloc-ls --distances
    Relative latency matrix (name NUMALatency kind 5) between 2 NUMANodes (depth -3) by logical indexes:
     index     0     1
         0    10    21
         1    21    10
    ```

??? info "Distance matrix for Iris Bigmem compute nodes"

    ```
    $ hwloc-ls --distances
    Relative latency matrix (name NUMALatency kind 5) between 4 NUMANodes (depth -3) by logical indexes:
     index     0     1     2     3
         0    10    21    21    21
         1    21    10    21    21
         2    21    21    10    21
         3    21    21    21    10
    ```

<!--
![Iris CPU node topology](images/iris-cpu-node-topology.svg){width="600" style="display: block; margin: 0 auto"}
![Iris CPU node topology](images/iris-cpu-node-topology.svg){: style="width:325px;"}
-->

## _Resources_

1. [Distribution and binding options - LUMI](https://docs.lumi-supercomputer.eu/runjobs/scheduled-jobs/distribution-binding/)
2. [Process and Thread Distribution and Binding - MUNI trainings](https://lumi-supercomputer.github.io/LUMI-training-materials/2day-20240502/07_Binding/)
3. [Hardware Locality (hwloc) documentation](https://hwloc.readthedocs.io/en/stable/)
