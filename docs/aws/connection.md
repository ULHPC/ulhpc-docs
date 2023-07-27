# Connection to the AWS Cluster

## Access to the frontend

**The ULHPC team will create specific access for the AWS Cluster and send to all project members a ssh key in order to connect to the cluster frontend.**

Once your account has been enabled, you can connect to the cluster using ssh. Computers based on Linux or Mac usually have ssh installed by default.
To create a direct connection, use the command below (using your specific cluster name if it differs from workshop-cluster).

```bash
ssh -i id_rsa username@ec2-52-5-167-162.compute-1.amazonaws.com 
```
This will open a direct, non-graphical connection in the terminal. To exit the remote terminal session, use the standard Linux command “exit”.

Alternatively, you may want to save the configuration of this connection (and create an alias for it) by editing the file `~/.ssh/config` (create it if it does not already exist) and adding the following entries:

```bash
Host aws-ulhpc-access
  User username
  Hostname ec2-52-5-167-162.compute-1.amazonaws.com 
  IdentityFile ~/.ssh/id_rsa
  IdentitiesOnly yes
```

For additionnal information about **ssh connection**, please refer to the following [page](../connect/ssh.md).


!!! danger "Data storage"
    * HOME storage is limited to 500GB for all users.
    * The ULHPC team will also create for you a project directory located at `/shared/projects/<project_id>`. All members of the project will have the possibility to read, write and execute only in this directory.
    * We strongly **advise** you to use the project directory to store data and install softwares. 



