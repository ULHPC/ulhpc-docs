# Login Nodes

Opening an [SSH connection](ssh.md) to ULHPC systems results in a
connection to an access node.

=== "Iris"
    ```bash
    ssh iris-cluster
    ```

=== "Aion"
    ```bash
    ssh aion-cluster
    ```
=== "Iris (X11)"
    To be able to further run GUI applications within your [interactive] jobs:
    ```bash
    ssh -X iris-cluster   # OR on Mac OS: ssh -Y iris-cluster
    ```
=== "Aion (X11)"
    To be able to further run GUI applications within your [interactive] jobs:
    ```bash
    ssh -X aion-cluster   # OR on Mac OS: ssh -Y aion-cluster
    ```

!!! important
    Recall that you **SHOULD NOT** run any HPC application on the login nodes.

    That's why the `module` command is **NOT** available on them.

## Usage

On access nodes, typical user tasks include

* Transferring and managing files
* Editing files
* Submitting [jobs](../jobs/submit.md)


!!! warning "Appropriate Use"
    Do not run compute- or memory-intensive applications on access
    nodes. These nodes are a shared resource. ULHPC admins may terminate
    processes which are having negative impacts on other users or the
    systems.

!!! warning "Avoid `watch`"
    If you _must_ use the `watch` command, please use a much longer
    interval such as 5 minutes (=300 sec), e.g., `watch -n 300
    <your_command>`.

!!! warning "Avoid `Visual Studio Code`"
    Avoid using `Visual Studio Code` to connect to the HPC, as it consumes a lot of resources
    in the login nodes. Heavy development shouldn't be done directly on the HPC.
    For most tasks using a terminal based editor should be enough like:
    `Vim` or `Emacs`. If you want to have some more advanced features try [`Neovim`](https://neovim.io/)
    where you can add plugins to meet your specific needs.

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

!!! tip "Running GUI Application over X11"
    If you intend to run GUI applications (MATLAB, Stata, ParaView etc.), you **MUST** connect by SSH to the login nodes with the `-X` (or `-Y` on Mac OS) option:

    === "Iris"
        ```bash
        ssh -X iris-cluster   # OR on Mac OS: ssh -Y iris-cluster
        ```
    === "Aion"
        ```bash
        ssh -X aion-cluster   # OR on Mac OS: ssh -Y aion-cluster
        ```

!!! tip "Install Neovim using Micormamba"
    Neovim is not installed by default on the HPC but you can install it using [Micromamba](../environment/conda.md#Installation).
    
    ```bash
    micromamba create --name editor-env
    micromamba install --name editor-env conda-forge::nvim
    ```
    After installation you can create a alias in your `.bashrc` for easy access:
    ```bash 
    alias nvim='micromamba run --name editor-env nvim'
    ```
