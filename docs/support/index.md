# Support

ULHPC strives to support in a user friendly way your [super]computing needs.
Note however that we are not here to make your PhD at your place ;)

[:fontawesome-solid-hand-holding-medical: Service Now HPC Support Portal](https://hpc.uni.lu/support){: .md-button .md-button--link }

## FAQ/Troubleshooting

* [Password reset](../policies/passwords/#forgotten-passwords)
* [Connection issues](../connect/troubleshooting.md)
* [File Permissions](../filesystems/unix-file-permissions.md)
    - [Access rights to project directory](../data/transfer.md#data-transfer-within-project-directories)
    - [Quotas](../filesystems/quotas.md#troubleshooting)

## Read the Friendly Manual

We have always maintained an extensive [documentation](https://hpc-docs.uni.lu) and [tutorials](https://ulhpc-tutorials.readthedocs.io) available online, which aims at being the most up-to-date and comprehensive.

So please, [read the documentation **first**](https://hpc-docs.uni.lu) if you have a question of problem -- we probably provide detailed instructions [here](/)

## Help Desk

The [online help desk Service](https://hpc.uni.lu/support/) is the **preferred**
method for contacting ULHPC.

!!! tips
    _Before_ reporting a problem or and issue, kindly remember that:

    1. Your issue is probably documented here on the [ULHPC Technical documentation](https://hpc-docs.uni.lu)
    2. An event may be on-going:
           * Planned maintenance are announced _at least_ 2 weeks in advance - -- see [Maintenance and Downtime Policy](../policies/maintenance.md)
           * The proper SSH banner is displayed during _planned_ downtime
    3. check the state of your nodes and jobs
           - [Joining/monitoring running jobs](../jobs/submit.md#joiningmonitoring-running-jobs)
           - [Monitoring _post-mortem_ Job status and efficiency](../slurm/commands.md#job-efficiency-seff-susage-or-sacct)

[:fontawesome-solid-hand-holding-medical: Service Now HPC Support Portal](https://hpc.uni.lu/support){: .md-button .md-button--link }

You can make code snippets, shell outputs, etc in your ticket much more readable by inserting a line with:
```
[code]<pre>
```
before the snippet, and another line with:
```
</pre>[/code]
```
after it. For a full list of formatting options, see [this ServiceNow article](https://community.servicenow.com/community?id=community_blog&sys_id=4d9ceae1dbd0dbc01dcaf3231f9619e1).


!!! warning "Be as precise and complete as possible"
	ULHPC team handle thousands of support requests per year.
    In order to ensure efficient timely resolution of issues, ensure that:

    1. you select the **appropriate** category (left menu)
    2. you include **as much of the following as possible** when making a request:
        - **Who?**  - Name and user id (login), eventually project name
        - **When?** - When did the problem occur?
        - **Where?** - Which cluster ? Which node ? Which job ?
            * Really include Job IDs
            * Location of relevant files
                - input/output, job launcher scripts, source code, executables etc.
        - **What?** - What happened? What exactly were you doing or trying to do ?
            * include Error messages - kindly report system or software messages _literally_ and _exactly_.
            * output of `module list`
            * any steps you have tried
            * Steps to reproduce
        - Any part of this technical documentation you checked before opening the ticket

Access to the online help system requires logging in with your **Uni.lu** username, password, and eventually one-time password.
If you are an existing user unable to log in, you can send us an [email](#email-support).

!!! info "Availability and Response Time"
    HPC support is provided on a volunteer basis by UL HPC staff and associated UL experts working at normal business hours. We offer **no guarantee** on response time except with paid support contracts.

## Email support

You can contact us by mail to the [ULHPC Team Email](mailto:hpc-team 'at' uni.lu) (**ONLY** if you cannot login/access the [HPC Support](https://hpc.uni.lu/support) helpdesk portal : [`hpc-team@uni.lu`](mailto:hpc-team 'at' uni.lu)


You may also ask the help of other ULHPC users using the HPC User community mailing list: (moderated): [`hpc-users@uni.lu`](mailto:hpc-users 'at' uni.lu)
