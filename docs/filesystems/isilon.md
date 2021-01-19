# Dell EMC Isilon (Archives and cold project data)

OneFS, A global _low_-performance [Dell/EMC Isilon](https://www.dellemc.com/en-us/collaterals/unauth/data-sheets/products/storage/h10717-isilon-onefs-ds.pdf) solution is used to host project data, and serve for backup and archival purposes. You will find it mounted under `/mnt/isilon`.

In 2014, the [IT Department of the University](https://wwwen.uni.lu/universite/presentation/organigrammes/organigramme_rectorat_administration_centrale/service_informatique_de_l_universite), the [UL HPC]
(https://hpc.uni.lu/about/team.html) and the [LCSB](http://wwwen.uni.lu/lcsb/) join their forces (and their funding) to acquire a scalable and modular
 NAS solution able to sustain the need for an internal big data storage, _i.e._ provides space for centralized data and backups of all devices used by the UL staff and all rese
arch-related data, including the one proceed on the [UL HPC](https://hpc.uni.lu) platform.

At the end of a public call for tender released in 2014, the [EMC Isilon](http://www.emc.com/isilon) system was finally selected with an effective deployment in 2015.
It is physically hosted in the new CDC (Centre de Calcul) server room in the [Maison du Savoir](http://www.fonds-belval.lu/index.php?lang=en&page=3&sub=2).
Composed by a large number of disk enclosures featuring the [OneFS](http://www.emc.com/en-us/storage/isilon/onefs-operating-system.htm) File System, it currently offers an **effective** capacity of 3.360 PB.

A secondary Isilon cluster, acquired in 2020 and deployed in 2021 is duplicating this setup in a redundant way.

![](images/isilon.jpg)
