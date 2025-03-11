# Dell EMC Isilon (Cold project data and Archives)

The university _central data storage services_ uses a [NAS](https://en.wikipedia.org/wiki/Network-attached_storage) system to provide long term storage for user data. The NAS system used is a [Dell/EMC Isilon](https://www.dellemc.com/en-us/collaterals/unauth/data-sheets/products/storage/h10717-isilon-onefs-ds.pdf) (Isilon) server with [OneFS](https://en.wikipedia.org/wiki/OneFS_distributed_file_system), a proprietary and distributed file system and environment, used to store the data. The OneFS file systems is exported by Isilon through the NFS protocol to the HPC platform and other Linux-based services, and through SMB (CIFS) to Windows-based clients. In UL HPC login nodes the script [`smb-storage`](/data/transfer/#mounting-an-smb-share-to-a-login-node) is provided to mount SMB shares.

<!--isilon-start-->

In the UL HPC platform the NFS exported by Isilon is used to host project data when they are not actively used in computations, and for archival purposes. Projects are mounted under `/mnt/isilon/projects`.

-  The file system in Isilon is redundant, regularly snapshot, and backed up, including off site backups. Data is replicated across multiple OneFS instances for high availability with the live sync feature of OneFS. Isilon is thus resilient to hardware failure, protected against catastrophic data loss, and also highly available.

- The NFS share exported from Isilon to the UL HPC platform is not using the Infiniband high performance network and the OneFS file system has lower I/O performance that GPFS and lustre file systems. However, the central data storage has significantly higher capacity.

!!! important "Long term data storage"
    Please move all your data to OneFS directories of the central data storage as soon as your computations finish.

    The central data storage is the intended place for storing data. Clustered file systems using the inifiniband network are meant as working storage only. For this reason, backups in cluster file systems are very limited.

Users have to ask for a project directories in the Isilon mount point (`/mnt/isilon/projects`) separately from the GPFS project directories. However, all users have a personal directory in the university _central data storage_ which they can access through the [ATLAS SMB system](/data/transfer/#transfers-between-long-term-storage-and-the-hpc-facilities). Users may also ask for project directories that are accessible through ATLAS, however these project cannot be mounted on the Isilon NFS share (`/mnt/isilon/projects`).

<!--isilon-end-->

In 2014, the [IT Department of the University](https://wwwen.uni.lu/universite/presentation/organigrammes/organigramme_rectorat_administration_centrale/service_informatique_de_l_universite), the [UL HPC](https://hpc.uni.lu/about/team.html) and the [LCSB](http://wwwen.uni.lu/lcsb/) join their forces (and their funding) to acquire a scalable and modular NAS solution able to sustain the need for an internal big data storage, _i.e._ provides space for centralized data and backups of all devices used by the UL staff and all research-related data, including the one proceed on the [UL HPC](https://hpc.uni.lu) platform.

At the end of a public call for tender released in 2014, the [EMC Isilon](http://www.emc.com/isilon) system was finally selected with an effective deployment in 2015. It is physically hosted in the new CDC (Centre de Calcul) server room in the [Maison du Savoir](http://www.fonds-belval.lu/index.php?lang=en&page=3&sub=2). Composed by a large number of disk enclosures featuring the [OneFS](http://www.emc.com/en-us/storage/isilon/onefs-operating-system.htm) File System, it currently offers an **effective** capacity of 3.360 PB.

A secondary Isilon cluster, acquired in 2020 and deployed in 2021 is duplicating this setup in a redundant way.

![](images/isilon.jpg)
