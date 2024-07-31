# Working on the HPC
Now that the SSH is setup, you can start working on the HPC. Working on the HPC is done through the command line and its not recommended to use
heavy IDEAS to connect to the HPC. If you want to use an IDE like visual studio code, work on your local machine and use git or scp/rsync to transfer the files to the HPC.

To use rsync, you can add the following line to your `.bashrc` file:
```bash
uploadhpc() {
  rsync --rsh='ssh -p 8022' -avzu $1 aion-cluster:$2
}
```
This will allow you to use the `uploadhpc` command to upload files to the HPC.
To use it, you can run:
```bash
uploadhpc file.txt /path/to/destinationOnHPC
```

If the connection is successful, you should see something like this:
![Successful-login](./images/success_connect.png)

# Connection to HPC
When using a supercomputer, you will usually first connect to a front-end or access node. From this machine, you can check your files, disk quota and computing usage. It is intended to be used by the user to prepare his computing job and scripts and then submit them to the job scheduler.

Because the access node is shared by all the users of the platform, it should not be used to compile and install your software and it should definitely not be used to run any memory or computing-intensive task.

# Linux Command Cheat Sheet

## Basic Commands
- `ls`: List directory contents.
    - `ls -l`: Detailed listing (long format).
    - `ls -a`: List all files, including hidden files.

- `cd [directory]`: Change directory.
    - `cd ..`: Go up one directory level.
    - `cd ~`: Go to the home directory.

- `pwd`: Print the current working directory.

- `mkdir [directory]`: Create a new directory.

- `rmdir [directory]`: Remove an empty directory.

- `rm [file]`: Remove a file.
    - `rm -r [directory]`: Remove a directory and its contents recursively.
    - `rm -f [file]`: Force remove a file.

- `cp [source] [destination]`: Copy files or directories.
    - `cp -r [source] [destination]`: Copy directories recursively.

- `mv [source] [destination]`: Move or rename files or directories.

- `touch [file]`: Create an empty file or update the timestamp of an existing file.

- `cat [file]`: Display the contents of a file.

- `less [file]`: View file contents one screen at a time.

- `head [file]`: Display the first 10 lines of a file.
    - `head -n [number] [file]`: Display the first `n` lines of a file.

- `tail [file]`: Display the last 10 lines of a file.
    - `tail -f [file]`: Follow the end of the file in real-time.

## File Permissions
- `chmod [permissions] [file]`: Change file permissions.
    - Example: `chmod 755 script.sh`

- `chown [user]:[group] [file]`: Change file owner and group.
    - Example: `chown user:group file.txt`

## File Compression
- `tar -czvf [archive.tar.gz] [directory]`: Create a compressed tarball.
- `tar -xzvf [archive.tar.gz]`: Extract a compressed tarball.

- `zip [archive.zip] [file]`: Create a zip file.
- `unzip [archive.zip]`: Extract a zip file.

## Process Management
- `ps`: Display currently running processes.
    - `ps aux`: Detailed information about all running processes.

- `top`: Display a dynamic view of system processes.

- `kill [PID]`: Terminate a process by its PID.
    - `kill -9 [PID]`: Force kill a process.

- `htop`: Enhanced process viewer (requires installation).

## Networking
- `ifconfig`: Display network interfaces and IP addresses.
- `ping [host]`: Check connectivity to a host.
- `ssh [user]@[host]`: Connect to a remote host via SSH.
- `scp [source] [user]@[host]:[destination]`: Secure copy files to/from a remote host.

## Disk Usage
- `df -h`: Display disk space usage.
- `du -sh [directory]`: Display the size of a directory and its contents.

## System Information
- `uname -a`: Display detailed system information.
- `uptime`: Show how long the system has been running.
- `free -h`: Display memory usage.

## Text Processing
- `grep [pattern] [file]`: Search for a pattern in a file.
    - `grep -r [pattern] [directory]`: Recursively search for a pattern in a directory.

- `sed 's/[pattern]/[replacement]/g' [file]`: Replace a pattern in a file.

- `awk '{print $1}' [file]`: Extract specific fields from a file.

## Miscellaneous
- `man [command]`: Display the manual page for a command.
- `echo [text]`: Display a line of text.
- `history`: Show command history.
- `clear`: Clear the terminal screen.
- `alias [name]='[command]'`: Create an alias for a command.


## HPC-Specific Commands
- `squeue`: Display the job queue.
- `sbatch [script.sh]`: Submit a batch script.
- `scancel [jobID]`: Cancel a job by its ID.
- `sinfo`: Display information about the cluster.

More information about the commands can be found in ...

# Text Editors
When working on the HPC, you will need to edit files and scripts. The most common text editors on Linux are `nano`, `vim`, and `emacs`. Here is a brief overview of each:

## Nano
Nano is a simple and user-friendly text editor that is easy to use for beginners. It is a good choice for quick edits and small files.

- Open a file: `nano [file]`
- Save a file: `Ctrl + O`
- Exit nano: `Ctrl + X`

## Vim
Vim is a powerful and highly configurable text editor that is popular among developers and system administrators. It has a steep learning curve but offers advanced features and customization options.

- Open a file: `vim [file]`
- Save a file: `:w`
- Exit vim: `:q`

Vim is different from most text editors in that it has different modes (normal, insert, visual, etc.). To enter insert mode, press `i`. To exit insert mode and return to normal mode, press `Esc`.

In normal mode, you can navigate the file using the arrow keys or `hjkl` (left, down, up, right). You can also use commands like `dd` to delete a line, `yy` to copy a line, and `p` to paste.

It is recommended to learn the basics of Vim to be more productive when working on the HPC.

## Emacs
Emacs is a powerful and extensible text editor that is popular among programmers and power users. It has a steep learning curve but offers advanced features and customization options.

- Open a file: `emacs [file]`
- Save a file: `Ctrl + X, Ctrl + S`
- Exit emacs: `Ctrl + X, Ctrl + C`

Emacs has a wide range of features and modes that can be customized to suit your workflow. It is highly extensible and can be used for programming, writing, and more.

## Nvim
Nvim is a fork of Vim that aims to improve the user experience and add new features. It is compatible with Vim plugins and configurations but offers additional functionality and performance improvements.

NeoVim is not installed by default on most systems, but you can install it using conda/micromamba.

- Open a file: `nvim [file]`
- Save a file: `:w`
- Exit nvim: `:q`

Nvim is designed to be more user-friendly and modern than Vim while maintaining compatibility with existing Vim configurations. It is a good choice for users who want a more modern text editor with Vim-like keybindings.

It offers a lot of plugins and themes to customize the editor to your liking.
Consider watching videos on youtube to learn more about the text editors and the many features they offer.



