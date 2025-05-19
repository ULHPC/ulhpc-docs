# Jupyter

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/1200px-Jupyter_logo.svg.png){: style="width:300px;float: right;"}

[Jupyter](https://jupyter.org/) is a set of free software, open standards, and web services for interactive computing across all programming languages. Jupyter is a large umbrella project that covers many different software offerings and tools, including the popular Jupyter Notebook and JupyterLab web-based notebook authoring and editing applications. The Jupyter project and its subprojects all center around providing tools (and standards) for interactive computing with computational [notebooks](#notebooks).

We strongly recommend using [modules](/environment/modules/) for Jupter application whenever modules are available. The main applications for interacting with Jupyter notebooks that are supported in UL HPC systems through modules are the following.

- [JupyterLab](https://jupyterlab.readthedocs.io/en/latest/) provided by `tools/JupyterLab`: a web-based interactive development environment for notebooks, code, and data; typically used to develop notebook documents.

- [Jupyter Notebook](https://jupyter-notebook.readthedocs.io/en/latest/) provided by `tools/JupyterNotebook`: a notebook authoring application; notebooks are shareable document that combines computer code, plain language descriptions, data, and visualizations.

-  [JupyterHub](https://jupyterhub.readthedocs.io/en/latest/) provided by `tools/JupyterHub`: a multi-user Hub that spawns and manages multiple instances of the single-user Jupyter notebook server; useful for sharing multiple instances of a notebook to a group of users.

!!! warning
    Modules are not allowed on the access servers. To test interactively, remember to ask for an [interactive job](/jobs/interactive) first using  for instance the `si` tool.

## Notebooks

[Notebooks](https://docs.jupyter.org/en/latest/#what-is-a-notebook) are documents that contain computer code, data, and rich text elements such as normal test, graphical equations, links, figures, and widgets. Notebooks contain human-readable analysis, descriptions, and results, together with executable versions of code data. As a result, notebooks are particularly popular for data analytics jobs, where they allow the interactive development of reproducible data analytic pipelines. Notebooks can be shared or converted into static HTML documents, and they are thus a powerful teaching tool as well.

Notebooks are associated with [kernels](https://jupyter-client.readthedocs.io/en/stable/kernels.html), processes that actually execute code required for the notebook. You can host kernels in isolated Python environments. Whenever possible use the Python [module](/environment/modules/) provided to create your environment, as modules have been optimally configured for our systems. If your application requires a different version of Python you can always install one with [Conda](/environment/conda/) or other tools.

To create the Python environment, start by loading the Python module and then create the environment. 

```shell
module load lang/Python
python -m venv ~/environments/notebook_venv
```

Install the packages that you require in your environment, and then install the `ipykernel` package.

```shell
module load lang/Python
source ~/environments/notebook_venv/bin/activate
pip install ipykernel
deactivate
```

You can then export a kernel for your environment that Jupyter applications can use to create notebooks using the environment. Jupyter applications provide a default environment with a kernel and also search some default locations for additional kernels. The user default location selected with the `--user` option of `ipykernel` is:

```
${HOME}/.local/share/jupyter/kernels
```

With the command,

```shell
module load lang/Python
source ~/environments/notebook_venv/bin/activate
python -m ipykernel install --user --name notebook_venv --display-name "Notebook"
deactivate
```

the kernel will be created in the default user location:

```
${HOME}/.local/share/jupyter/kernels/notebook_venv
```

and the kernel will appear with the name "Notebook" in your list of available kernels in all Jupyter applications launched by the user.

### Kernels in environments with site packages

The UL HPC systems offer optimized Python packages for applications such as PyTorch. You can access the optimized packages in your environments if you build your environment with access to system site packages. For instance to access the PyTorch packages that have been optimized for GPUs in the Iris GPU nodes create the environment for your notebook as follows.

```shell
module load ai/PyTorch/2.3.0-foss-2023b-CUDA-12.6.0
python -m venv --system-site-packages ~/environments/notebook_venv
source ~/environments/notebook_venv/bin/activate
pip install ipykernel
python -m ipykernel install --user --name notebook_venv --display-name "Notebook"
deactivate
```

With the `--system-site-packages` flag, the packages provided by the `ai/PyTorch/2.3.0-foss-2023b-CUDA-12.6.0` module are accessible to your `notebook_venv`.

### Kernels in arbitrary directories

You can also specify an installation location for your kernel that is different than the default user location. For instance you may want to store your kernel in a [project directory](/filesystems/#project-directories) to share it with other members of your team. In this case you can use the `--prefix` option to create the project.

```shell
module load lang/Python
source ~/environments/notebook_venv/bin/activate
python -m ipykernel install --prefix=${PROJECTHOME}/project_name/environments/jupyter_env --name notebook_venv --display-name "Notebook"
deactivate
```

To use a kernel from a custom installation path instruct the Jupyter application to search for environments in the extra path with the `--notebook-dir` option. For instance with the command

```shell
module load tools/JupyterLab
jupyter lab --notebook-dir=${PROJECTHOME}/project_name/environments/jupyter_env
```

the "Notebook" will be listed in the available kernels in the Jupyter lab application.

### Kernels for Conda environments

Some packages may require a specific version of Python. In this case install the required Python version in a Conda environment. Then follow the steps above to create the Python environment while using the Python of the Conda environment. For instance, the commands
```bash
micromamba create --name conda_notebook conda-forge::python=3.8
micromamba run --name conda_notebook python -m venv ~/environments/conda_notebook_venv
source ~/environments/conda_notebook_vemv/bin/activate
python -m ipykernel install --user --name conda_notebook_venv --display-name "Conda notebook"
deactivate
```
create a kernel for the `conda_notebook_venv` environment with Python 3.8.

Note that Jupyter does not currently support kernels for Conda environments, so you have to create a Python environment (`venv`) for your kernel.


## Working with JupyterLab

[JupyterLab](https://jupyterlab.readthedocs.io/en/latest/) is a web-based interactive development environment for notebooks, code, and data. Typically used to develop notebook documents, is highly extensible, and more feature-rich that the traditional Jupyter Notebook. In UL HPC systems Jupyter lab is provided by the `tools/JupyterLab` [module](/environment/modules/). Load the Jupyter module with the following command.

```shell
module load tools/JupyterLab
```
### Starting a JupyterLab session

Jupyter notebooks must be started as [slurm jobs](/jobs/submit). The following script is a template for Jupyter submission scripts that will rarely need modifications. Most often you will need to modify the session duration (`--time` SBATCH option).

!!! example "Slurm Launcher script for Jupyter Notebook"
    ```slurm
    #!/usr/bin/bash --login
    #SBATCH --job-name=Jupyter
    #SBATCH --nodes=1
    #SBATCH --ntasks-per-node=1
    #SBATCH --cpus-per-task=2   # Change accordingly, note that ~1.7GB RAM is proivisioned per core
    #SBATCH --partition=batch
    #SBATCH --qos=normal
    #SBATCH --output=%x_%j.out  # Print messages to 'Jupyter_<job id>.out
    #SBATCH --error=%x_%j.err   # Print debug messages to 'Jupyter_<job id>.err
    #SBATCH --time=0-01:00:00   # Change maximum allowable jupyter server uptime here

    print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
    module purge || print_error_and_exit "No 'module' command"
    
    # Load the JupyterLab module
    module load tools/JupyterLab

    declare loopback_device="127.0.0.1"
    declare port="8888"
    declare connection_instructions="connection_instructions.log"

    jupyter lab --ip=${loopback_device} --port=${port} --no-browser &
    declare lab_pid=$!

    # Add connection instruction
    echo "# Connection instructions" > "${connection_instructions}"
    echo "" >> "${connection_instructions}"
    echo "To access the jupyter notebook execute on your personal machine:" >> "${connection_instructions}"
    echo "ssh -J ${USER}@access-${ULHPC_CLUSTER}.uni.lu:8022 -L ${port}:${loopback_device}:${port} ${USER}@$(hostname -i)" >> "${connection_instructions}"
    echo "" >> "${connection_instructions}"
    echo "To access the jupyter notebook if you have setup a special key (e.g ulhpc_id_ed25519) to connect to cluster nodes execute on your personal machine:" >> "${connection_instructions}"
    echo "ssh -i ~/.ssh/hpc_id_ed25519 -J ${USER}@access-${ULHPC_CLUSTER}.uni.lu:8022 -L ${port}:${loopback_device}:${port} ${USER}@$(hostname -i)" >> "${connection_instructions}"
    echo "" >> "${connection_instructions}"
    echo "Then navigate to:" >> "${connection_instructions}"

    # Wait for the server to start
    sleep 2s
    # Wait and check that the landing page is available
    curl \
        --connect-timeout 10 \
        --retry 5 \
        --retry-delay 1 \
        --retry-connrefused \
        --silent --show-error --fail \
        "http://${loopback_device}:${port}" > /dev/null
    # Note down the URL
    jupyter lab list 2>&1 \
        | grep -E '\?token=' \
        | awk 'BEGIN {FS="::"} {gsub("[ \t]*","",$1); print $1}' \
        | sed -r 's/([0-9]{1,3}\.){3}[0-9]{1,3}/127\.0\.0\.1/g' \
        >> "${connection_instructions}"

    # Save some debug information
    echo -e '\n===\n'

    echo "AVAILABLE LABS"
    echo ""
    jupyter lab list
    
    echo -e '\n===\n'

    echo "CONFIGURATION PATHS"
    echo ""
    jupyter --paths

    echo -e '\n===\n'

    echo "KERNEL SPECIFICATIONS"
    echo ""
    jupyter kernelspec list

    # Wait for the user to terminate the lab
    wait ${lab_pid}
    ```

Once your job is running (see [Joining/monitoring running jobs](/jobs/submit#joiningmonitoring-running-jobs)), you can combine 

- [`ssh` forwarding](/connect/ssh#ssh-port-forwarding), and
- an [`ssh` jump](/connect/ssh#port-forwarding-over-ssh-jumps) through the login node,

to connect to the notebook from your laptop. Open a terminal on your laptop and copy-paste the ssh command contained in the file `connection_instructions.log`, and then navigate to the webpage link provided.

!!! example "Example content  of `connection_instructions.log`"
    ```shell
    > cat connection_instructions.log
    # Connection instructions
    
    To access the jupyter notebook execute on your personal machine:
    ssh -J gkafanas@access-aion.uni.lu:8022 -L 8888:127.0.0.1:8888 gkafanas@172.21.12.29
    
    To access the jupyter notebook if you have setup a special key (e.g ulhpc_id_ed25519) to connect to cluster nodes execute on your personal machine:
    ssh -i ~/.ssh/ulhpc_id_ed25519 -J gkafanas@access-aion.uni.lu:8022 -L 8888:127.0.0.1:8888 gkafanas@172.21.12.29
    
    Then navigate to:
    http://127.0.0.1:8888/?token=b7cf9d71d5c89627250e9a73d4f28cb649cd3d9ff662e7e2
    ```

As the instructions suggest, you access the jupyter lab server in the compute node by calling
```shell
ssh -J gkafanas@access-aion.uni.lu:8022 -L 8888:127.0.0.1:8888 gkafanas@172.21.12.29
```
an SSH command that

- opens a connection to your allocated cluster node jumping through the login node (`-J gkafanas@access-aion.uni.lu:8022 gkafanas@172.21.12.29`), and
- exports the port to the jupyter server in the local machine (`-L 8888:127.0.0.1:8888`).

Then, open the connection to the browser in your local machine by following the given link:
```
http://127.0.0.1:8888/?token=b7cf9d71d5c89627250e9a73d4f28cb649cd3d9ff662e7e2
```

The link provides the access token, so you should be able to login without a password.

!!! warning
    Do not forget to click on the `quit` button when finished to stop the Jupyter server and release the resources. Note that in the last line of the submission script the job waits for your Jupyter service to finish. 

If you encounter any issues, have a look in the debug output in `Jupyter_<job id>.err`. Generic information about the setup of your system is printed in `Jupyter_<job id>.out`.

??? example "Typical content of `Jupyter_<job id>.err`"
    ```shell
    > cat Jupyter_3664038.err 
    [I 2024-11-13 23:19:52.538 ServerApp] jupyter_lsp | extension was successfully linked.
    [I 2024-11-13 23:19:52.543 ServerApp] jupyter_server_terminals | extension was successfully linked.
    [I 2024-11-13 23:19:52.547 ServerApp] jupyterlab | extension was successfully linked.
    [I 2024-11-13 23:19:52.766 ServerApp] notebook_shim | extension was successfully linked.
    [I 2024-11-13 23:19:52.808 ServerApp] notebook_shim | extension was successfully loaded.
    [I 2024-11-13 23:19:52.812 ServerApp] jupyter_lsp | extension was successfully loaded.
    [I 2024-11-13 23:19:52.813 ServerApp] jupyter_server_terminals | extension was successfully loaded.
    [I 2024-11-13 23:19:52.814 LabApp] JupyterLab extension loaded from /home/users/gkafanas/environments/jupyter_env/lib/python3.11/site-packages/jupyterlab
    [I 2024-11-13 23:19:52.814 LabApp] JupyterLab application directory is /mnt/aiongpfs/users/gkafanas/environments/jupyter_env/share/jupyter/lab
    [I 2024-11-13 23:19:52.815 LabApp] Extension Manager is 'pypi'.
    [I 2024-11-13 23:19:52.826 ServerApp] jupyterlab | extension was successfully loaded.
    [I 2024-11-13 23:19:52.827 ServerApp] Serving notebooks from local directory: /mnt/aiongpfs/users/gkafanas/support/jupyter
    [I 2024-11-13 23:19:52.827 ServerApp] Jupyter Server 2.14.2 is running at:
    [I 2024-11-13 23:19:52.827 ServerApp] http://127.0.0.1:8888/lab?token=fe665f90872927f5f84be627f54cf9056908c34b3765e17d
    [I 2024-11-13 23:19:52.827 ServerApp]     http://127.0.0.1:8888/lab?token=fe665f90872927f5f84be627f54cf9056908c34b3765e17d
    [I 2024-11-13 23:19:52.827 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
    [C 2024-11-13 23:19:52.830 ServerApp] 
        
        To access the server, open this file in a browser:
            file:///home/users/gkafanas/.local/share/jupyter/runtime/jpserver-2253096-open.html
        Or copy and paste one of these URLs:
            http://127.0.0.1:8888/lab?token=fe665f90872927f5f84be627f54cf9056908c34b3765e17d
            http://127.0.0.1:8888/lab?token=fe665f90872927f5f84be627f54cf9056908c34b3765e17d
    [I 2024-11-13 23:19:52.845 ServerApp] Skipped non-installed server(s): bash-language-server, dockerfile-language-server-nodejs, javascript-typescript-langserver, jedi-language-server, julia-language-server, pyright, python-language-server, python-lsp-server, r-languageserver, sql-language-server, texlab, typescript-language-server, unified-language-server, vscode-css-languageserver-bin, vscode-html-languageserver-bin, vscode-json-languageserver-bin, yaml-language-server
    [I 2024-11-13 23:19:53.824 ServerApp] 302 GET / (@127.0.0.1) 0.47ms
    ```

??? example "Typical content of `Jupyter_<job id>.err`"
    ```shell
    > cat Jupyter_3664038.out
    
    ===
    
    AVAILABLE LABS
    
    Currently running servers:
    http://127.0.0.1:8888/?token=fe665f90872927f5f84be627f54cf9056908c34b3765e17d :: /mnt/aiongpfs/users/gkafanas/support/jupyter
    
    ===
    
    CONFIGURATION PATHS
    
    config:
        /home/users/gkafanas/environments/jupyter_env/etc/jupyter
        /mnt/aiongpfs/users/gkafanas/.jupyter
        /usr/local/etc/jupyter
        /etc/jupyter
    data:
        /home/users/gkafanas/environments/jupyter_env/share/jupyter
        /home/users/gkafanas/.local/share/jupyter
        /usr/local/share/jupyter
        /usr/share/jupyter
    runtime:
        /home/users/gkafanas/.local/share/jupyter/runtime
    
    ===
    
    KERNEL SPECIFICATIONS
    
    Available kernels:
      other_python_env    /home/users/gkafanas/environments/jupyter_env/share/jupyter/kernels/other_python_env
      python3             /home/users/gkafanas/environments/jupyter_env/share/jupyter/kernels/python3 
    ```

### Environment configuration

Jupyter generates various files during runtime, and reads configuration files from various locations. You can control these paths using [environment variables](https://docs.jupyter.org/en/latest/use/jupyter-directories.html). For instance, you may set the `JUPYTER_RUNTIME_DIR` to point somewhere in the [`/tmp` directory](https://hpc-docs.uni.lu/filesystems/#intended-usage-of-file-systems) for better performance.

- [`JUPYTER_CONFIG_DIR`](https://docs.jupyter.org/en/latest/use/jupyter-directories.html#envvar-JUPYTER_CONFIG_DIR): Set the directory for Jupyter config files; default is `${HOME}/.jupyter`.
- [`JUPYTER_PATH`](https://docs.jupyter.org/en/latest/use/jupyter-directories.html#envvar-JUPYTER_PATH): Extra directories to search for installable data files, such as [kernelspecs](https://jupyter-client.readthedocs.io/en/stable/kernels.html#making-kernels-for-jupyter) and [notebook extensions](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/); should contain a series of directories, separated by `os.pathsep` (`;` on Windows and `:` on Unix); directories given in `JUPYTER_PATH` are searched before other locations.
- [`JUPYTER_DATA_DIR`](https://docs.jupyter.org/en/latest/use/jupyter-directories.html#envvar-JUPYTER_DATA_DIR): Set the user data directory which contains files such as [kernelspecs](https://jupyter-client.readthedocs.io/en/stable/kernels.html#making-kernels-for-jupyter), [notebook extensions](https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/), or [voila templates](https://voila.readthedocs.io/en/stable/index.html); default is `${HOME}/.local/share/jupyter/` (respects `${XDG_DATA_HOME}`).
- [`JUPYTER_RUNTIME_DIR`](https://docs.jupyter.org/en/latest/use/jupyter-directories.html#envvar-JUPYTER_RUNTIME_DIR): Set the location where Jupyter stores runtime files, such as connection files, which are only useful for the lifetime of a particular process; default is `${JUPYTER_DATA_DIR}/runtime`.

### Password protected access

You can also set a password when launching the jupyter lab as detailed in the [Jupyter official documentation](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html). In that case, simply direct you browser to the URL `http://127.0.0.1:8888/` and provide your password. You can see bellow an example of the login page.

??? example "Typical content of a password protected login page"
    ![](./images/jupyter_login.png)


## Install Jupyter

While JupyterLab runs code in Jupyter notebooks for many programming languages, Python is a requirement (Python 3.3 or greater, or Python 2.7) for installing the JupyterLab. New users may wish to install JupyterLab in a Conda environment. Hereafter, the `pip` package manager will be used to install JupyterLab.

We strongly recommend to use the Python module provided by the ULHPC and installing `jupyter` inside a Python virtual environment after upgrading `pip`.

```shell
$ si
$ module load lang/Python #Loading default Python
$ python -m venv ~/environments/jupyter_env
$ source ~/environments/jupyter_env/bin/activate
$ python -m pip install --upgrade pip
$ python -m pip install jupyterlab
```

Once JupyterLab is installed along with , you can start to configure your installation setting the environment variables corresponding to your needs.

JupyterLab is now installed and ready.

??? info "Installing the classic Notebook"
    JupyterLab (`jupyterlab`) is a new package which automates many task that where performed manually in the traditional Jupyter package (`jupyter`). If you prefer to install the classic notebook, you also need to install the [IPython](https://ipython.readthedocs.io/en/stable/index.html) manually as well, replacing
    ```bash
    python -m pip install jupyterlab
    ```
    with:
    ```bash
    python -m pip install jupyter ipykernel
    ```

### Providing access to kernels of other environments

JupyterLab makes sure that a default [IPython kernel](https://ipython.readthedocs.io/en/stable/install/kernel_install.html#) is available, with the environment (and the Python version) with which the lab was created. Other environments can export a _kernel_ to a JupyterLab instance, allowing the instance to launch interactive session inside environments others from the environment where JupyterLab is installed.

You can [setup kernels with different environments on the same notebook](https://ipython.readthedocs.io/en/stable/install/kernel_install.html). Create the environment with the Python version and the packages you require, and then register the kernel in any environment with Jupyter (lab or classic notebook) installed. For instance, if we have installed Jupyter in `~/environments/jupyter_env`:
```shell
source ~/environments/other_python_venv/bin/activate
python -m pip install ipykernel
python -m ipykernel install --prefix=${HOME}/environments/jupyter_env --name other_python_env --display-name "Other Python env"
deactivate
```
Then all kernels and their associated environment can be started from the same Jupyter instance in the `~/environments/jupyter_env` Python venv.

You can also use the flag `--user` instead of `--prefix` to install the kernel in the default system location available to all Jupyter environments for a user.




