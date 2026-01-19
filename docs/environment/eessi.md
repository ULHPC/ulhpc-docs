# EESSI - European Environment for Scientific Software Installations

[<img width='400px' style='float:left' src='https://www.eessi.io/docs/img/logos/EESSI_logo_horizontal.jpg'/>](https://www.eessi.io/)

The [European Environment for Scientific Software Installations (EESSI, pronounced as "easy")](https://www.eessi.io/) is a collaboration between different European partners in HPC community.
The goal of this project is to build a common stack of scientific software installations for HPC systems and beyond, including laptops, personal workstations and cloud infrastructure.

The EESSI software stack is available on the ULHPC platform, and gives you access to software modules maintained by the EESSI project and optimized for the CPU architectures available on the ULHPC platform.

## UL HPC systems compute nodes

On a compute node, to set up the EESSI environment, simply load the EESSI [module](/environment/modules/):

```bash
module load EESSI
```

The first usage may be slow as the files are downloaded from an upstream Stratum 1 server, but the files are cached locally.

You should see the following output:

```console
$ module load EESSI
EESSI/2023.06 loaded successfully
```

Your environment is now set up, you are ready to start running software provided by EESSI! To see which modules (and extensions) are available, run:

```bash
module avail
```

Here is a short excerpt of the output produced by module avail:

```
----- /cvmfs/software.eessi.io/versions/2023.06/software/linux/x86_64/amd/zen2/modules/all -----
   ALL/0.9.2-foss-2023a           ESPResSo/4.2.1-foss-2023a        foss/2023a            h5py/3.9.0-foss-2023a
   ParaView/5.11.2-foss-2023a     PyTorch/2.1.2-foss-2023a         QuantumESPRESSO/7.2-foss-2022b   VTK/9.3.0-foss-2023a
   ELPA/2022.05.001-foss-2022b    foss/2022b                       foss/2023b (D)        OpenFOAM/11-foss-2023a
...
```

??? note "Accessing development versions of EESSI"
    New releases of EESSI are hidden while they are under development. However, you can still access the hidden modules. To view releases under development enable reporting of hidden modules, with
    ```console
    $ module --show_hidden avail
    ```
    or
    ```console
    $ module --show_hidden avail EESSI
    ```
    to search specifically for EESSI. You can load a hidden module by providing the full name of the module, for instance
    ```console
    $ module load EESSI/2025.06
    ```
    even though autocompletion will not work for hidden module names.


For more precise information, please refer to the [official documentation](https://www.eessi.io/docs).

## Grid'5000 compute nodes

The EESSI environment is also accessible on [Grid'5000](/g5k/getting-started-g5k/) compute nodes, but EESSI must first be installed. This article explains the installation of EESSI in a node running Debian, which is the default operating system for Grid'5000. The installation process is similar if you prefer to deploy another operating system.

Root rights are required to install EESSI. Start an interactive session in a compute node and get access to the `sudo` command with the `sudo-g5k` command.

```bash
sudo-g5k
```

The installation of EESSI requires first the installation of [CernVM-FS](https://cvmfs.readthedocs.io/en/stable/index.html) which the underlying file system used to distribute the software binaries. 

- Start by adding the GPG keys for the CernVM-FS repository.

  ```bash
  wget https://ecsft.cern.ch/dist/cvmfs/cvmfs-release/cvmfs-release-latest_all.deb
  dpkg-deb --raw-extract cvmfs-release-latest_all.deb cvmfs-release
  sudo cp cvmfs-release/etc/apt/trusted.gpg.d/cernvm.gpg /etc/apt/trusted.gpg.d/cernvm.gpg
  ```

- Add the CernVM-FS repository in the list of sources.

  ```bash
  sudo cp cvmfs-release/usr/share/cvmfs-release/cernvm.list.$(lsb_release --codename | awk '{print $2}') /etc/apt/sources.list.d/cernvm.list
  ```

  ??? info "Installation in Debian 13 (trixie)"
      The APT interface was updated in Debian 13. Currently Debian 13 (trixie) is only supported by the experimental release of CERN VM-FS. Install the APT sources with the following command:
      ```bash
      sudo bash -c 'cat <<EOF > /etc/apt/sources.list.d/cernvm.sources
      Types: deb
      URIs: http://cvmrepo.s3.cern.ch/cvmrepo/apt/
      Suites: trixie-testing
      Components: main
      Signed-By: /etc/apt/trusted.gpg.d/cernvm.gpg
      EOF'
      ```

- Install CernVM-FS.

  ```bash
  sudo apt update
  sudo apt install cvmfs
  ```

Now the EESSI can be installed and configured from the official package.

- Download the package for EESSI.

  ```bash
  wget https://github.com/EESSI/filesystem-layer/releases/download/latest/cvmfs-config-eessi_latest_all.deb
  ```

- Install and configure EESSI.

  ```
  sudo dpkg -i cvmfs-config-eessi_latest_all.deb
  # create client configuration file for CernVM-FS (no squid proxy, 10GB local CernVM-FS client cache)
  sudo bash -c "echo 'CVMFS_CLIENT_PROFILE="single"' > /etc/cvmfs/default.local"
  sudo bash -c "echo 'CVMFS_QUOTA_LIMIT=10000' >> /etc/cvmfs/default.local"
  # make sure that EESSI CernVM-FS repository is accessible
  sudo cvmfs_config setup
  ```

The EESSI environment can now be accessed by sourcing the appropriate initialization script.

```
source /cvmfs/software.eessi.io/versions/2023.06/init/lmod/bash
```

### Installing in all nodes of a job

The installation process for EESSI must be performed every time you access a new compute node. _If your job involves multiple nodes, you have to repeat the process in each compute node._

The UL HPC provides a [repository of installation scripts](https://github.com/ULHPC/Installing-EESSI-in-G5K-nodes.git) that automate the installation of EESSI in all nodes of a Grid'5000 job. To install, clone the repository on your Grid'5000 home directory that is mount on all login and compute nodes of a site:

```shell
git clone https://github.com/ULHPC/Installing-EESSI-in-G5K-nodes.git
```

Then, launch a job, change into the repository directory _in a login node_, and run the installation script:

```shell
cd Installing-EESSI-in-G5K-nodes
./install-eessi-in-g5k-job-nodes <job ID>
```

??? info "Accessing the job ID"

    To get the job ID of a submitted job, use the `oarstat` command.
    ```terminal
    $ oarstat --user "${USER}"
    Job id     Name           User           Submission Date     S        Queue
    ---------- -------------- -------------- ------------------- -------- ----------
    <job ID>                  <user name>    <date>              <status> <queue>   
    ```

    The first column of the output contains the job ID.

!!! info "Installation scripts"

    The installation uses a couple of installation scripts. The main script extracts the nodes of the job, and then lunches an installation script to all nodes of the job with cluster shell (`clush`).

    ??? info "`install-eessi-in-g5k-job-nodes`"
        #!/usr/bin/bash

        set -euo pipefail

        declare node_list=""
        declare job_id="${1}"

        while [ -z "${node_list}" ]; do
          node_list=$(oarstat --full --job "${job_id}" | awk 'BEGIN {FS="="} $1 ~ /assigned_hostnames/ {gsub(" ", "", $2); gsub(".luxembourg.grid5000.fr", "", $2); gsub("+", ",", $2); print $2}')
          [ -z "${node_list}" ] && sleep 5
        done

        clush --dshbak -w "${node_list}" "${PWD}/setup-eessi-in-g5k"

    ??? info "`install-eessi-in-g5k`"
        #!/usr/bin/bash

        set -euo pipefail

        declare DEBIAN_FRONTEND=noninteractive

        main() {
          sudo-g5k
          install_cvmfs
          install_eessi
        }

        install_cvmfs() {
          # Install CMFS keys
          if [ ! -f /tmp/cvmfs-release-latest_all.deb ]; then
            wget --output-document=/tmp/cvmfs-release-latest_all.deb https://ecsft.cern.ch/dist/cvmfs/cvmfs-release/cvmfs-release-latest_all.deb
          fi
          dpkg-deb --raw-extract /tmp/cvmfs-release-latest_all.deb /tmp/cvmfs-release
          sudo cp /tmp/cvmfs-release/etc/apt/trusted.gpg.d/cernvm.gpg /etc/apt/trusted.gpg.d/cernvm.gpg

          # Add CVMFS sources
          sudo cp /tmp/cvmfs-release/usr/share/cvmfs-release/cernvm.list.$(lsb_release --codename | awk '{print $2}') /etc/apt/sources.list.d/cernvm.list

          # Install CVMFS
          sudo apt --assume-yes update
          sudo apt --assume-yes install cvmfs

          cleaup_cvmfs_installation_files
        }

        cleaup_cvmfs_installation_files() {
          rm /tmp/cvmfs-release-latest_all.deb
          rm -r /tmp/cvmfs-release
        }

        install_eessi() {
          # Install EESSI package
          if [ ! -f /tmp/cvmfs-config-eessi_latest_all.deb ]; then
            wget --output-document=/tmp/cvmfs-config-eessi_latest_all.deb https://github.com/EESSI/filesystem-layer/releases/download/latest/cvmfs-config-eessi_latest_all.deb
          fi
          sudo dpkg -i /tmp/cvmfs-config-eessi_latest_all.deb
          # create client configuration file for CernVM-FS (no squid proxy, 10GB local CernVM-FS client cache)
          sudo bash -c "echo 'CVMFS_CLIENT_PROFILE="single"' > /etc/cvmfs/default.local"
          sudo bash -c "echo 'CVMFS_QUOTA_LIMIT=10000' >> /etc/cvmfs/default.local"
          # make sure that EESSI CernVM-FS repository is accessible
          sudo cvmfs_config setup

          cleanup_eessi_installation_files
        }

        cleanup_eessi_installation_files() {
          rm /tmp/cvmfs-config-eessi_latest_all.deb
        }

        main
