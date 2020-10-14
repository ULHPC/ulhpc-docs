# SSH

All ULHPC servers are reached using either the Secure
Shell (SSH) communication and encryption protocol (version 2).

SSH (Secure Shell) is an encrypted network protocol used to log into
computers over an unsecured network. On UNIX/LINUX/BSD type systems,
SSH is also the name of a suite of software applications for
connecting via the SSH protocol. The SSH applications can execute
commands on a remote machine and transfer files from one machine to
another.  All communications are automatically and transparently
encrypted, including passwords. Most versions of SSH provide login
(`ssh`, `slogin`), a remote copy operation (`scp`), and many also provide a
secure ftp client (`sftp`). Additionally, SSH allows secure X Window
connections.

To use SSH, you have to generate a pair of keys, one public and the other
private. The public key authentication practiced on the ULHPC platforms
assumes that the public key is known by the system in order to perform
an authentication based on a challenge/response protocol instead of the
classical password-based protocol.

The way SSH handles the keys and the configuration files is illustrated in the following figure:

![](images/ssh.png)

## Password-less logins and transfers

Password based authentication is disabled on all ULHPC servers.
You can only use public-key authentication.

Consult the documentation on using the [IPA service](ipa.md) service 
for ways to upload your SSH public key to your account.

## Key fingerprints

ULHPC may occasionally update the host keys on the major systems.  Check here
to confirm the current fingerprints.

 *  `access-iris.uni.lu`
	```
    256 SHA256:BzLVnnTO2NcPqAyUepwYkbNJWnfAYEgiUCDInJHwpdw /etc/ssh/ssh_host_ecdsa_key.pub (ECDSA)
    256 SHA256:tkhRD9IVo04NPw4OV/s2LSKEwe54LAEphm7yx8nq1pE /etc/ssh/ssh_host_ed25519_key.pub (ED25519)
    2048 SHA256:WDWb2hh5uPU6RgaSotxzUe567F3scioJWy+9iftVmhI /etc/ssh/ssh_host_rsa_key.pub (RSA)
	```


!!! note
    The ssh fingerprints can be obtained via:
    ```
    ssh-keygen -lf <(ssh-keyscan -t rsa,ed25519,ecdsa $hostname 2>/dev/null)
    ```
!!! note 

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

### Iris

```
[access-iris.uni.lu]:8022 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBOazFRMcdqEn6MpG4H5viEkImw0WwbqZ5SbOlAbZOCrVRA43cNwHkYg5q0RaqeNPEwGHxwTEZ7ACRgReNEo2iGs=
```

## Troubleshooting

### "Access Denied" or "Permission Denied"

This is likely a username or ssh public key problem.

1. Make sure you are using the proper ULHPC user name, check your mail entitled
   "[HPC@Uni.lu] Welcome - Account information".
1. Log into [IPA](ipa.md) and double check your SSH public key.

!!! note
	If you are still unable to login, open a ticket on [Service Now](https://service.uni.lu/)
    and contact ULHPC at [hpc-team@uni.lu](mailto:hpc-team@uni.lu).

### Host identification changed

```
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY!
Someone could be eavesdropping on you right now (man-in-the-middle attack)!
It is also possible that a host key has just been changed.
...
```

Ensure that your `~/.ssh/known_hosts` file contains the correct entries for
Iris and confirm the fingerprints using the posted fingerprints above. 

1. Open `~/.ssh/known_hosts`
1. Remove any lines referring Iris and save the file
1. Paste the host key entries from above or retry connecting to the host and
   accept the new host key after verify that you have the correct "fingerprint"
   from the above list.

