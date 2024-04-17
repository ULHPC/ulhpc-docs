# Jupyter Notebook

![](https://upload.wikimedia.org/wikipedia/commons/thumb/3/38/Jupyter_logo.svg/1200px-Jupyter_logo.svg.png){: style="width:300px;float: right;"}


[Jupyter](https://jupyter-notebook.readthedocs.io/en/stable/) is a flexible, popular literate-computing web application for creating notebooks containing code, equations, visualization, and text. Notebooks are documents that contain both computer code and rich text elements (paragraphs, equations, figures, widgets, links). They are human-readable documents containing analysis descriptions and results but are also executable data analytics artifacts. Notebooks are associated with kernels, processes that actually execute code. Notebooks can be shared or converted into static HTML documents. They are a powerful tool for reproducible research and teaching.


## Install Jupyter

While Jupyter runs code in many programming languages, Python is a requirement (Python 3.3 or greater, or Python 2.7) for installing the Jupyter Notebook. New users may wish to use Anaconda or conda to install Jupyter. Hereafter, the `pip` package manager will be used to install Jupyter.

We strongly recommend to use the Python module provided by the ULHPC and installing `jupyter` inside a virtualenv after upgrading `pip`.

```shell
$ si
$ module load lang/Python #Loading default Python
$ python -m venv jupyter_env
$ source jupyter_env/bin/activate
$ python -m pip install --upgrade pip
$ python -m pip install jupyter ipykernel
```

!!! warning
    Modules are not allowed on the access servers. To test interactively Singularity, remember to ask for an [interactive job](../jobs/interactive.md) first using  for instance the `si` tool.

Once Jupyter is installed along with [IPython](https://ipython.readthedocs.io/en/stable/index.html), you can start to configure your installation setting the environment variables corresponding to your needs:


- `JUPYTER_CONFIG_DIR`: Set this environment variable to use a particular directory, other than the default, for Jupyter config files
- `JUPYTER_PATH`: Set this environment variable to provide extra directories for the data search path. `JUPYTER_PATH` should contain a series of directories, separated by os.pathsep(; on Windows, : on Unix). Directories given in JUPYTER_PATH are searched before other locations. This is used in addition to other entries, rather than replacing any
- `JUPYTER_DATA_DIR`: Set this environment variable to use a particular directory, other than the default, as the user data directory
- `JUPYTER_RUNTIME_DIR`: Set this to override where Jupyter stores runtime files
- `IPYTHONDIR`: If set, this environment variable should be the path to a directory, which IPython will use for user data. IPython will create it if it does not exist.

Jupyter Notebook makes sure that the [IPython kernel](https://ipython.readthedocs.io/en/stable/install/kernel_install.html#) is available, but you have to manually add a kernel with a different version of Python or a virtual environment.

Register the kernel using the following command:

```shell
python -m ipykernel install --sys-prefix --name jupyter_env
```
Jupyter and your virtualenv are now installed and ready.

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
    source jupyter_env/bin/activate

    jupyter notebook --ip $(hostname -i) --no-browser  &
    pid=$!
    sleep 5s
    jupyter notebook list
    jupyter --paths
    jupyter kernelspec list
    echo "Enter this command on your laptop: ssh -p 8022 -NL 8888:$(hostname -i):8888 ${USER}@access-iris.uni.lu " > notebook.log
    wait $pid
    ```

Once your job is running (see [Joining/monitoring running jobs](../jobs/submit.md#joiningmonitoring-running-jobs), you can use `ssh` [forwarding](../connect/ssh.md#ssh-port-forwarding) to connect to the notebook from your laptop. Open a terminal on your laptop and copy-paste the ssh command in the file `notebook.log`.
You should be now able to reach your notebook.

Then open your browser and go to the url: `http://127.0.0.1:8888/`. Jupyter should ask you for a password (see screenshot below). This password can be set before running the jupyter notebook and his part of the initial configuartion detailed at [Jupyter official documentation](https://jupyter-notebook.readthedocs.io/en/stable/public_server.html).

![](./images/jupyter_login.png)

if by mistake, you forgot to setup this password, have a look in the slurm-****.out file in which the output of the command `jupyter notebook list` has been recorded.

```shell
>$ cat slurm-2152135.out
Currently running servers:
config:
    /mnt/irisgpfs/users/ekieffer/.jupyter
    /mnt/irisgpfs/users/ekieffer/jupyter_env/etc/jupyter
    /usr/local/etc/jupyter
    /etc/jupyter
data:
    /home/users/ekieffer/.local/share/jupyter
    /mnt/irisgpfs/users/ekieffer/jupyter_env/share/jupyter
    /usr/local/share/jupyter
    /usr/share/jupyter
runtime:
    /home/users/ekieffer/.local/share/jupyter/runtime
Available kernels:
  jupyter_env    /home/users/ekieffer/.local/share/jupyter/kernels/jupyter_env
  python3        /home/users/ekieffer/.local/share/jupyter/kernels/python3
  venv           /home/users/ekieffer/.local/share/jupyter/kernels/venv
[I 15:15:42.682 NotebookApp] Serving notebooks from local directory: /mnt/irisgpfs/users/ekieffer
[I 15:15:42.682 NotebookApp] Jupyter Notebook 6.1.5 is running at:
[I 15:15:42.682 NotebookApp] http://172.17.6.75:8888/?token=5e976373fcb84e9be7796c35a17d232eb594a7b0bb6647a1
[I 15:15:42.682 NotebookApp]  or http://127.0.0.1:8888/?token=5e976373fcb84e9be7796c35a17d232eb594a7b0bb6647a1
[I 15:15:42.682 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 15:15:42.697 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///home/users/ekieffer/.local/share/jupyter/runtime/nbserver-21681-open.html
    Or copy and paste one of these URLs:
        http://172.17.6.75:8888/?token=5e976373fcb84e9be7796c35a17d232eb594a7b0bb6647a1
     or http://127.0.0.1:8888/?token=5e976373fcb84e9be7796c35a17d232eb594a7b0bb6647a1
[I 15:36:47.512 NotebookApp] 302 GET / (172.17.2.11) 0.88ms
[I 15:36:47.572 NotebookApp] 302 GET /tree? (172.17.2.11) 1.21ms
```

Jupyter provides you a token to connect to the notebook. You can also notice the available kernels and more specifically the jupyter_env.

!!! warning
    Do not forget to click on the `quit` button when finished to stop the jupyter server and release the ressources.
