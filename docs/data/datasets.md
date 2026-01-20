# Datasets management

The ULHPC team provides central storage for various public and freely usable datasets and databases in the shared directory `/work/project/bigdata_sets/`.
This directory is read-only for all users of the HPC platform. The advantage of this central location is twofold:

- **Prevents data duplication**: It avoids many users downloading the same dataset to their own directories.
- **Performance**: `/work/project/bigdata_sets/` is hosted on our fast storage tier.
- **Scientific reproducibility**: It ensures that different users can use the same version of the dataset.

Users who use public data for their calculations should always check first if it's already available in `/work/project/bigdata_sets/`.


## Requesting a New Dataset

You can request to host a new dataset in this dedicated space on [service.uni.lu](https://service.uni.lu/sp?id=sc_cat_item&sys_id=9f9acb4887b2c210aa6d65740cbb355c&table=sc_cat_item&searchTerm=dataset) (Section Research > HPC > Storage & projects > Request a dataset upload). 

Note that some datasets may not be shareable publicly in this directory due to licensing or distribution constraints.

## Data Manipulation

Some datasets contain millions of small files. Manipulating this amount of small files is a **worst-case scenario** for performance on any parallel filesystem. Additionally, it may not be feasible to manipulate such a volume of files in user directories due to inode quotas.

Instead, we advise keeping the dataset archived in `tar` format on the shared filesystem and uncompressing the archives in the `/tmp/` directory at the beginning of your job. Iris and Aion feature a local SSD or NVME that is user-writeable and mounted in `/tmp` for temporary files.

To uncompress such a file efficiently, you can use `pigz`, which is a parallelized implementation of `gzip`:

```bash
cd /tmp
tar -I pigz -xf /scratch/users/hcartiaux/dataset.tar.gz
```

For example, uncompressing the [Malnet image dataset](https://www.mal-net.org/) (an 80GB tarball) into the /tmp/ directory of an Aion node takes less than 5 minutes. This is an order of magnitude faster than manipulating over one billion files on any of our shared filesystems.
