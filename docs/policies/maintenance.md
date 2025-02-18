# Maintenance and Downtime Policy


![](images/downtime.jpg){: style="width:325px; float: right;"}

## Scheduled Maintenance

The ULHPC team  will schedule maintenance in one of three manners:

1. __Rolling reboots__
   Whenever possible, ULHPC will apply updates and do other maintenance in a rolling fashion in such a manner as to have either no or as little impact as possible to ULHPC services
2. __Partial outages__
   We will do these as needed but in a manner that impacts only some ULHPC services at a time
3. __Full outages__
   These are outages that will affect all ULHPC services, such as outages of core datacenter networking services,  datacenter power of HVAC/cooling system maintenance or [global GPFS/Spectrumscale filesystem updates](../filesystems/gpfs.md).
   Such maintenance windows typically happen on a **quarterly basis**.
   **_It should be noted that we are not always able to anticipate when these outages are needed_**.

   ULHPC's goal for these downtimes is to have them completed as fast as possible.
   However, validation and qualification of the full platform takes typically one working day, and unforeseen or unusual circumstances may occur. So **count for such outages a multiple-day downtime**.

## Notifications

We _normally_ inform users of cluster maintenance **at least 3 weeks in advance** by mail using the HPC User community mailing list (moderated): [`hpc-users@uni.lu`](mailto:hpc-users 'at' uni.lu).
A second reminder is sent a few days prior to actual downtime.

The news of the downtimes is also posted on the [hpc/support/infra issue tracker](https://gitlab.com/uniluxembourg/hpc/support/infra/-/issues)/.

A colored "_message of the day_" (motd) banner is displayed on all [access/login servers](../connect/access.md) such that you can quickly be informed of any incoming maintenance operation upon connection to the cluster.
You can see this when you login or (again),any time by issuing the command:

```console
cat /etc/motd
```

!!! tips "Detecting maintenance... During the maintenance"
    * During the maintenance period, access to the involved cluster access/login serveur is **DENIED** and any users still logged-in are disconnected at the beginning of the maintenance
         - you will receive a written message in your terminal
         - if for some reason during the maintenance you urgently need to collect data from your account, please contact the [UL HPC Team](mailto:hpc-team@uni.lu) by sending a mail to: [`hpc-team@uni.lu`](mailto:hpc-team@uni.lu).
     * We will notify you of the end of the maintenance with a summary of the performed operations.


## Exceptional "EMERGENCY"  maintenance

Unscheduled downtimes can occur for any number of reasons, including:

* Loss of cooling and/or power in the data center.
* Loss of supporting infrastructure (i.e. hardware).
* Critical need to make changes to hardware
or software that negatively impacts performance or access.
* Application of critical patches that can't wait until the next scheduled maintenance.
* For safety or security issues that require immediate action.

We will _try_ to notify users in the advent of such event by email.

!!! danger
    The ULHPC team reserves the right to intervene in user activity without notice when such activity may destabilize the platform and/or is at the expense of other users, and/or to monitor/verify/debug ongoing system activity.
