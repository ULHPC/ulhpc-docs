# Jupyter Notebook

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/1200px-Jupyter_logo.svg.png){: style="width:300px;float: right;"}


[JupyterLab](https://jupyterlab.readthedocs.io/en/stable/) is a flexible, popular literate-computing web application for creating notebooks containing code, equations, visualization, and text. Notebooks are documents that contain both computer code and rich text elements (paragraphs, equations, figures, widgets, links). They are human-readable documents containing analysis descriptions and results but are also executable data analytics artifacts. Notebooks are associated with kernels, processes that actually execute code. Notebooks can be shared or converted into static HTML documents. They are a powerful tool for reproducible research and teaching.


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

!!! warning
    Modules are not allowed on the access servers. To test interactively Singularity, remember to ask for an [interactive job](../jobs/interactive.md) first using  for instance the `si` tool.

Once JupyterLab is installed along with , you can start to configure your installation setting the environment variables corresponding to your needs:

- `JUPYTER_CONFIG_DIR`: Set this environment variable to use a particular directory, other than the default, for Jupyter config files
- `JUPYTER_PATH`: Set this environment variable to provide extra directories for the data search path. `JUPYTER_PATH` should contain a series of directories, separated by os.pathsep(; on Windows, : on Unix). Directories given in JUPYTER_PATH are searched before other locations. This is used in addition to other entries, rather than replacing any
- `JUPYTER_DATA_DIR`: Set this environment variable to use a particular directory, other than the default, as the user data directory
- `JUPYTER_RUNTIME_DIR`: Set this to override where Jupyter stores runtime files
- `IPYTHONDIR`: If set, this environment variable should be the path to a directory, which IPython will use for user data. IPython will create it if it does not exist.

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

??? info "Managing multiple kernels"
    JupyterLab makes sure that a default [IPython kernel](https://ipython.readthedocs.io/en/stable/install/kernel_install.html#) is available, with the environment (and the Python version) with which the lab was created.

    You can [setup kernels with different environments on the same notebook](https://ipython.readthedocs.io/en/stable/install/kernel_install.html). Create the environment with the Python version and the packages you require, and then register the kernel in any environment with Jupyter (lab or classic notebook) installed. For instance, if we have installed Jupyter in `~/environments/jupyter_env`:
    ```shell
    source ~/environments/other_python_env/bins/activate
    python -m pip install ipykernel
    python -m ipykernel install --prefix=~/environments/jupyter_env --name "Other Python env"
    ```
    Then all kernels and their associated environment can be start from the same Jupyter instance.

    You can also use the flag `--user` instead of `--prefix` to install the kernel in the default system location available to all Jupyter environments.

## Starting a Jupyter Notebook

Jupyter notebooks can be started as a [slurm job](../jobs/submit.md).
The following script is an example how to proceed:

!!! example "Slurm Launcher script for Jupyter Notebook"
    ```slurm
    #!/bin/bash -l
    #SBATCH -J Jupyter
    #SBATCH -N 1
    #SBATCH --ntasks-per-node=1
    #SBATCH -c 2                # Cores assigned to each tasks
    #SBATCH --time=0-01:00:00
    #SBATCH -p batch

    print_error_and_exit() { echo "***ERROR*** $*"; exit 1; }
    module purge || print_error_and_exit "No 'module' command"
    
    # Python 3.X by default (also on system)
    module load lang/Python
    source "${HOME}/environments/jupyter_env/bin/activate"

    jupyter lab --ip $(hostname -i) --no-browser &
    pid=$!
    sleep 5s
    jupyter lab list
    jupyter --paths
    jupyter kernelspec list
    echo "Enter this command on your laptop: ssh -i ~/.ssh/hpc_id_ed25519 -J ${USER}@access-iris.uni.lu:8022 -L 8888:$(hostname -i):8888 ${USER}@$(hostname -i)" > notebook.log
    wait $pid
    ```

Once your job is running (see [Joining/monitoring running jobs](../jobs/submit.md#joiningmonitoring-running-jobs)), you can use `ssh` [forwarding](../connect/ssh.md#ssh-port-forwarding) and an [ssh jump](../connect/ssh.md#ssh-jumps) through the login node to connect to the notebook from your laptop. Open a terminal on your laptop and copy-paste the ssh command in the file `notebook.log`.
You should be now able to reach your notebook.

Then open your browser and go to the url: `http://127.0.0.1:8888/`. Jupyter should ask you for a password (see screenshot below). This password can be set before running the jupyter notebook and his part of the initial configuartion detailed at [Jupyter official documentation](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html).

![](./images/jupyter_login.png)

if by mistake, you forgot to setup this password, have a look in the slurm-****.out file in which the output of the command `jupyter notebook list` has been recorded.

```shell
>$ cat slurm-3528839.out 
[I 2024-07-15 16:14:22.538 ServerApp] jupyter_lsp | extension was successfully linked.
[I 2024-07-15 16:14:22.545 ServerApp] jupyter_server_terminals | extension was successfully linked.
[I 2024-07-15 16:14:22.552 ServerApp] jupyterlab | extension was successfully linked.
[I 2024-07-15 16:14:22.843 ServerApp] notebook_shim | extension was successfully linked.
[I 2024-07-15 16:14:22.865 ServerApp] notebook_shim | extension was successfully loaded.
[I 2024-07-15 16:14:22.871 ServerApp] jupyter_lsp | extension was successfully loaded.
[I 2024-07-15 16:14:22.872 ServerApp] jupyter_server_terminals | extension was successfully loaded.
[I 2024-07-15 16:14:22.875 LabApp] JupyterLab extension loaded from /mnt/aiongpfs/users/gkafanas/environments/jupyter_env/lib/python3.8/site-packages/jupyterlab
[I 2024-07-15 16:14:22.875 LabApp] JupyterLab application directory is /mnt/aiongpfs/users/gkafanas/environments/jupyter_env/share/jupyter/lab
[I 2024-07-15 16:14:22.876 LabApp] Extension Manager is 'pypi'.
[I 2024-07-15 16:14:22.889 ServerApp] jupyterlab | extension was successfully loaded.
[I 2024-07-15 16:14:22.890 ServerApp] Serving notebooks from local directory: /mnt/aiongpfs/users/gkafanas/tmp
[I 2024-07-15 16:14:22.890 ServerApp] Jupyter Server 2.14.2 is running at:
[I 2024-07-15 16:14:22.890 ServerApp] http://172.17.6.2:8888/lab?token=a3bcac16d3923f7e8909ac3dfb7593affe6fdb547b5ebd88
[I 2024-07-15 16:14:22.890 ServerApp]     http://127.0.0.1:8888/lab?token=a3bcac16d3923f7e8909ac3dfb7593affe6fdb547b5ebd88
[I 2024-07-15 16:14:22.890 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2024-07-15 16:14:22.897 ServerApp] 
    
    To access the server, open this file in a browser:
        file:///home/users/gkafanas/.local/share/jupyter/runtime/jpserver-126637-open.html
    Or copy and paste one of these URLs:
        http://172.17.6.2:8888/lab?token=a3bcac16d3923f7e8909ac3dfb7593affe6fdb547b5ebd88
        http://127.0.0.1:8888/lab?token=a3bcac16d3923f7e8909ac3dfb7593affe6fdb547b5ebd88
[I 2024-07-15 16:14:22.919 ServerApp] Skipped non-installed server(s): bash-language-server, dockerfile-language-server-nodejs, javascript-typescript-langserver, jedi-language-server, julia-language-server, pyright, python-language-server, python-lsp-server, r-languageserver, sql-language-server, texlab, typescript-language-server, unified-language-server, vscode-css-languageserver-bin, vscode-html-languageserver-bin, vscode-json-languageserver-bin, yaml-language-server
Currently running servers:
http://172.17.6.2:8888/?token=a3bcac16d3923f7e8909ac3dfb7593affe6fdb547b5ebd88 :: /mnt/aiongpfs/users/gkafanas/tmp
config:
    /mnt/aiongpfs/users/gkafanas/environments/jupyter_env/etc/jupyter
    /mnt/aiongpfs/users/gkafanas/.jupyter
    /usr/local/etc/jupyter
    /etc/jupyter
data:
    /mnt/aiongpfs/users/gkafanas/environments/jupyter_env/share/jupyter
    /home/users/gkafanas/.local/share/jupyter
    /usr/local/share/jupyter
    /usr/share/jupyter
runtime:
    /home/users/gkafanas/.local/share/jupyter/runtime
Available kernels:
  python3    /mnt/aiongpfs/users/gkafanas/environments/jupyter_env/share/jupyter/kernels/python3
  ir         /home/users/gkafanas/.local/share/jupyter/kernels/ir 
```

Jupyter provides you a token to connect to the lab. You can also notice the available kernels.

!!! warning
    Do not forget to click on the `quit` button when finished to stop the jupyter server and release the ressources.
