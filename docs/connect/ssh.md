# SSH

All ULHPC servers are reached using either the Secure
Shell (SSH) communication and encryption protocol (version 2).

Developed by [SSH Communications Security Ltd.](http://www.ssh.com), Secure Shell is a an encrypted network protocol used to log into another computer over an unsecured network, to execute commands in a remote machine, and to move files from one machine to another in a secure way.
On UNIX/LINUX/BSD type systems, SSH is also the name of a suite of software applications for
connecting via the SSH protocol. The SSH applications can execute
commands on a remote machine and transfer files from one machine to
another.  All communications are automatically and transparently
encrypted, including passwords. Most versions of SSH provide login
(`ssh`, `slogin`), a remote copy operation (`scp`), and many also provide a
secure ftp client (`sftp`). Additionally, SSH allows secure X Window
connections.

To use SSH, you have to generate a pair of keys, one **public** and the other
**private**.
The public key authentication is the most secure and flexible approach to ensure a multi-purpose transparent connection to a remote server.
This approach is enforced on the ULHPC platforms and assumes that the _public_ key is known by the system in order to perform an authentication based on a challenge/response protocol instead of the
classical password-based protocol.

The way SSH handles the keys and the configuration files is illustrated in the following figure:

![](images/ssh.png)

## Installation

* OpenSSH is natively supported on Linux / Mac OS / Unix / WSL (see below)
* On Windows, you are thus encouraged to install [Windows Subsystem for Linux](https://docs.microsoft.com/en-us/windows/wsl/about) (WSL) and setup an Ubuntu subsystem from  [Microsoft Store](https://aka.ms/wslstore).
    - You probably want to also install [Windows Terminal](https://github.com/microsoft/terminal) and  [MobaXterm](http://mobaxterm.mobatek.net/)
    - Better performances of your Linux subsystem can be obtained by migrating to WSL 2
    - Follow the [ULHPC Tutorial: Setup Pre-Requisites / Windows](https://ulhpc-tutorials.readthedocs.io/en/latest/setup/preliminaries/#microsoft-windows) for detailed instructions.

## SSH Key Generation

To generate an RSA SSH keys **of 4096-bit length**, just use the `ssh-keygen` command [as follows](https://explainshell.com/explain?cmd=ssh-keygen+-t+rsa+-o+-a+100):

```bash
ssh-keygen -t rsa -b 4096 -o -a 100
```

!!! danger "To passphrase or not to passphrase"
    To ensure the security of your SSH key-pair on your laptop, you **MUST** protect your SSH keys with a passphrase!
    Note however that while possible, this passphrase is purely private and has _a priori_ nothing to do with your University or your ULHPC credentials. Nevertheless, a strong passphrase follows the same recommendations as for strong passwords (for instance: see [Google password tips](https://support.google.com/accounts/answer/32040?hl=en)).

    Finally, just like encryption keys, passphrases need to be kept safe and protected from _unauthorised_ access. A _Password Manager_  can help you to store all your passwords safely. The University is currently not offering a university wide password manger but there are many free and paid ones you can use, for example: [KeePassX](https://www.keepassx.org/), [PWSafe](https://www.pwsafe.org/relatedprojects.shtml), [Dashlane](https://www.dashlane.com/), [1Password](https://1password.com/) or [LastPass](https://www.lastpass.com/).

You may want to generate also **ED25519** Key Pairs (which is the most recommended public-key algorithm available today) -- see [explaination](https://explainshell.com/explain?cmd=ssh-keygen+-t+ed25519+-o+-a+100)

```
ssh-keygen -t ed25519 -o -a 100
```

Your key pairs will be located under `~/.ssh/` and follow the following format -- the `.pub` extension indicated the **public** key part and is the **ONLY one SAFE to distribute**:

```bash
$ ls -l ~/.ssh/id_*
-rw------- username groupname ~/.ssh/id_rsa
-rw-r--r-- username groupname ~/.ssh/id_rsa.pub		# Public  RSA key
-rw------- username groupname ~/.ssh/id_ed25519
-rw-r--r-- username groupname ~/.ssh/id_ed25519.pub # Public ED25519 key
```

For more details, follow the [ULHPC Tutorials: Preliminaries / SSH](https://ulhpc-tutorials.readthedocs.io/en/latest/preliminaries/#secure-shell-ssh).

??? note "(deprecated) Windows only: SSH key management with MobaKeyGen tool"
    On Windows with [MobaXterm](http://mobaxterm.mobatek.net/), a tool exists and can be used to generate an SSH key pair. While not recommended (we encourage you to run WSL), here are the instructions to follow to generate these keys:

    * Open the application **Start > Program Files > MobaXterm**.
    * Change the default home directory for a persistent home directory instead of the default Temp directory. Go onto **Settings > Configuration > General > Persistent home directory**.
         - choose a location for your home directory.
             * your local SSH configuration will be located under `HOME/.ssh/`
    * Go onto **Tools > Network > MobaKeyGen (SSH key generator)**.
         - Choose **RSA** as the type of key to generate and change "Number of bits in a generated key" to 4096.
         - Click on the **Generate** button. Move your mouse to generate some randomness.
         - Select a strong passphrase in the **Key passphrase** field for your key.
    * Save the public and private keys as respectively `id_rsa.pub` and `id_rsa.ppk`.
         - Please keep a copy of the public key, you will have to add this public key into your account, using the IPA user portal (use the URL communicated to you by the UL HPC team in your "welcome" mail).

    ![MobaKeyGen (SSH key generator)](images/moba-ssh-key-gen.png)

!!! note "(deprecated) Windows only: SSH key management with PuTTY"
    While no longer recommended, you may still want to use [Putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/) and the associated tools, more precisely:

    * [PuTTY](https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe), the free SSH client
    * [Pageant](https://the.earth.li/~sgtatham/putty/latest/w64/pageant.exe), an SSH authentication agent for PuTTY tools
    * [PuTTYgen](https://the.earth.li/~sgtatham/putty/latest/w64/puttygen.exe), an RSA key generation utility
    * [PSCP](https://the.earth.li/~sgtatham/putty/latest/w64/pscp.exe), an SCP (file transfer) client, i.e. command-line secure file copy
    * [WinSCP](http://winscp.net/eng/download.php), SCP/SFTP (file transfer) client with easy-to-use graphical interface

    The different steps involved in the installation process are illustrated below (**REMEMBER to tick the option "Associate .PPK files (PuTTY Private Key) with Pageant and PuTTYGen"**):

    ![Putty Setup Screen #4](images/putty-screenshot-5.png)

    Now you can use the [PuTTYgen](http://the.earth.li/~sgtatham/putty/latest/x86/puttygen.exe) utility to generate an RSA key pair. The main steps for the generation of the keys are illustrated below (yet with **4096 bits** instead of 2048):

    ![Configuring a passphrase](images/puttygen-screenshot-8.png)

    ![Saving the private key](images/puttygen-screenshot-9.png)

    ![Saving the public key](images/puttygen-screenshot-10.png)

    * Save the public and private keys as respectively `id_rsa.pub` and `id_rsa.ppk`.
         - Please keep a copy of the public key, you will have to add this public key into your account, using the IPA user portal (use the URL communicated to you by the UL HPC team in your "welcome" mail).


## Password-less logins and transfers

Password based authentication is disabled on all ULHPC servers.
You can only use public-key authentication.

Consult the documentation on using the [IPA service](ipa.md) service
for ways to upload your SSH public key to your account.

## SSH Configuration

On Linux / Mac OS / Unix / WSL, your SSH configuration is defined in `~/.ssh/config`.
As recommended in the [ULHPC Tutorials: Preliminaries / SSH](https://ulhpc-tutorials.readthedocs.io/en/latest/preliminaries/#secure-shell-ssh), you probably want to create the following configuration to easiest further access and data transfers:

```bash
# ~/.ssh/config -- SSH Configuration
# Common options
Host *
    Compression yes
    ConnectTimeout 15

# ULHPC Clusters
Host iris-cluster
    Hostname access-iris.uni.lu

Host aion-cluster
    Hostname access-aion.uni.lu

# /!\ ADAPT 'yourlogin' accordingly
Host *-cluster
    User yourlogin
    Port 8022
    ForwardAgent no
```


## Key fingerprints

ULHPC may occasionally update the host keys on the major systems.  Check here
to confirm the current fingerprints.

=== "Iris"

    With regards `access-iris.uni.lu`:

    ```
    256 SHA256:BzLVnnTO2NcPqAyUepwYkbNJWnfAYEgiUCDInJHwpdw /etc/ssh/ssh_host_ecdsa_key.pub (ECDSA)
    256 SHA256:tkhRD9IVo04NPw4OV/s2LSKEwe54LAEphm7yx8nq1pE /etc/ssh/ssh_host_ed25519_key.pub (ED25519)
    2048 SHA256:WDWb2hh5uPU6RgaSotxzUe567F3scioJWy+9iftVmhI /etc/ssh/ssh_host_rsa_key.pub (RSA)
	```

===  "Aion"

    With regards `access-aion.uni.lu`:


!!! info "Get SSH key fingerprint"
    The ssh fingerprints can be obtained via:
    ```
    ssh-keygen -lf <(ssh-keyscan -t rsa,ed25519,ecdsa $(hostname) 2>/dev/null)
    ```

??? tips "Putty key fingerprint format"
    Depending on the ssh client you use to connect to ULHPC systems, you may see different key fingerprints.
    For example, Putty uses different format of fingerprints as follows:

    * `access-iris.uni.lu`
    ```
    ssh-ed25519 255 4096 07:6a:5f:11:df:d4:3f:d4:97:98:12:69:3a:63:70:2f
    ```

    You may see the following warning when connecting to Cori with Putty, but it is safe to ingore.

    ```
    PuTTY Security Alert
    The server's host key is not cached in the registry. You have no guarantee that the server is the computer you think it is.
    The server's ssh-ed25519 key fingerprint is:
    ssh-ed25519 255 4096 07:6a:5f:11:df:d4:3f:d4:97:98:12:69:3a:63:70:2f
    If you trust this host, hit Yes to add the key to PuTTY's cache and carry on connecting.
    If you want to carry on connecting just once, without adding the key to the cache, hit No.
    If you do not trust this host, hit Cancel to abandon the connection.
    ```

## Host Keys

These are the entries in `~/.ssh/known_hosts`.

=== "Iris"

    The known host SSH entry for the [Iris cluster](../systems/iris/index.md)  should be as follows:

    ```
    [access-iris.uni.lu]:8022 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOazFRMcdqEn6MpG4H5viEkImw0WwbqZ5SbOlAbZOCrVRA43cNwHkYg5q0RaqeNPEwGHxwTEZ7ACRgReNEo2iGs=
    ```

===  "Aion"

    The known host SSH entry for the [Aion cluster](../systems/aion/index.md) should be as follows:

    ```
    [access-aion.uni.lu]:8022 TODO
    ```

## Troubleshooting

See [the corresponding section](troubleshooting.md).
