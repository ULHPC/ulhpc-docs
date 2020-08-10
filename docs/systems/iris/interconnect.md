# Fast Local Interconnect Network

The Fast _local_ interconnect network implemented within Iris relies on the [Mellanox](https://www.mellanox.com/) **[Infiniband (IB) EDR](https://en.wikipedia.org/wiki/InfiniBand)[^1]** technology.
For more details, see [Introduction to
High-Speed InfiniBand Interconnect](https://www.hpcadvisorycouncil.com/pdf/Intro_to_InfiniBand.pdf).

[^1]: Enhanced Data Rate (EDR) – 100 Gb/s throughput with a very low latency, typically below 0,6$\mu$s.

One of the most significant differentiators between HPC systems and lesser performing systems is, apart from the interconnect technology deployed, the supporting topology. There are several topologies commonly used in large-scale HPC deployments ([Fat-Tree](https://clusterdesign.org/fat-trees/), [3D-Torus](https://clusterdesign.org/torus/), Dragonfly+ etc.).

![](https://clusterdesign.org/wp-content/uploads/2012/02/fat_tree_varying_ports.png){: style="width:200px;float: right;"}
Iris (like [Aion](../aion/index.md)) is part of an _Island_ which employs a "[Fat-Tree](https://clusterdesign.org/fat-trees/)" Topology[^2] which remains the widely used topology in HPC clusters due to its versatility, high bisection bandwidth and well understood routing.
Iris 2-Level Fat-Tree is composed of:

* 6x L2 Spine IB (SIB) EDR [Mellanox SB7800](https://www.mellanox.com/products/infiniband-switches/SB7800) switches (36 ports)
* 12x L1 Leaf IB (LIB) EDR  [Mellanox SB7800](https://www.mellanox.com/products/infiniband-switches/SB7800) switches (36 ports)

The Iris Island is connected through its L2 SIB switches to the Aion Island through 48 EDR links.

[^2]: with blocking factor 1:1.5.


For more details:
[:fontawesome-solid-sign-in-alt: ULHPC Fast IB Interconnect](../../interconnect/ib.md){: .md-button .md-button--link }
