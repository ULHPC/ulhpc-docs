# Login Nodes

Opening an [SSH connection](ssh.md) to ULHPC systems results in a
connection to an access node.

## Usage

On access nodes, typical user tasks include

* Transferring and managing files
* Editing files
* Submitting [jobs](../jobs/submi.md)


!!! warning "Appropriate Use"
    Do not run compute- or memory-intensive applications on access
    nodes. These nodes are a shared resource. ULHPC admins may terminate
    processes which are having negative impacts on other users or the
    systems.

!!! warning "Avoid `watch`"
    If you _must_ use the `watch` command, please use a much longer
    interval such as 5 minutes (=300 sec), e.g., `watch -n 300
    <your_command>`.


## Tips

!!! tip "ULHPC provides a wide variety of qos's"
    * An [`interactive` qos](../jobs/interactive.md) is
    available on Iris and Aion for compute- and memory-intensive interactive
    work. Please, use an interactive job for resource-intensive processes
    instead of running them on access nodes.

!!! tip
    To help identify processes that make heavy use of resources, you
    can use:

    * `top -u $USER`
    * `/usr/bin/time -v ./my_command`
