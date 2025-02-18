# Sensitive Data Protection

The advent of the EU [General Data Protection Regulation](http://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv:OJ.L_.2016.119.01.0001.01.ENG&toc=OJ:L:2016:119:TOC) (_GDPR_) permitted to highlight the need to protect sensitive information from leakage.

## GPG

A basic approach relies on GPG to encrypt single files -- see [this tutorial for more details](https://varrette.gforge.uni.lu/blog/2017/03/14/tutorial-gpg-gnu-privacy-guard/)

```bash
# File encryption
$ gpg --encrypt [-r <recipient>] <file>     # => produces <file>.gpg
$ rm -f <file>    # /!\ WARNING: encryption DOES NOT delete the input (clear-text) file
$ gpg --armor --detach-sign <file>          # Generate signature file <file>.asc

# Decryption
$ gpg --verify <file>.asc           # (eventually but STRONGLY encouraged) verify signature file
$ gpg --decrypt <file>.gpg          # Decrypt PGP encrypted file
```

One drawback is that files need to be completely decrypted for processing

[:fontawesome-solid-sign-in-alt: Tutorial: Using GnuPG aka Gnu Privacy Guard aka GPG](https://varrette.gforge.uni.lu/tutorials/gpg.html){: .md-button .md-button--link }


## File Encryption Frameworks (EncFS, GoCryptFS...)

In contrast to disk-encryption software that operate on whole disks (TrueCrypt, dm-crypt etc), file encryption operates on individual files that can be backed up or synchronised easily, especially within a Git repository.

* [Comparison matrix](https://nuetzlich.net/gocryptfs/comparison/)
   - [gocryptfs](https://nuetzlich.net/gocryptfs/), aspiring successor of EncFS written in Go
   - [EncFS](https://github.com/vgough/encfs), mature with known security issues
   - [eCryptFS](http://ecryptfs.org/), integrated into the Linux kernel
   - [Cryptomator](https://cryptomator.org/), strong cross-platform support through Java and WebDAV
   - [securefs](https://github.com/netheril96/securefs), a cross-platform project implemented in C++.
   - [CryFS](https://www.cryfs.org/), result of a master thesis at the KIT University that uses chunked storage to obfuscate file sizes.

Assuming you are working from `/path/to/my/project`, your workflow (mentionned below for EncFS, but it can be adpated to all the other tools) operated on encrypted _vaults_ and would be as follows:

* (_eventually_) if operating within a working copy of a git repository, you should ignore the mounting directory (ex: `vault/*`) in the root `.gitignore` of the repository
    - this ensures neither you nor a collaborator will commit any unencrypted version of a file by mistake
    - you commit only the EncFS / GocryptFS / eCryptFS / Cryptomator / securefs / CryFS raw directory (ex: `.crypt/`) in your repository. Thus only encrypted form or your files are commited
* You create the EncFS / GocryptFS / eCryptFS / Cryptomator / securefs / CryFS encrypted vault
* You prepare macros/scripts/Makefile/Rakefile tasks to lock/unlock the vault on demand

Here are for instance a few example of these operations in live to **create** a encrypted vault:

=== "EncFS"
    ```bash
    $ cd /path/to/my/project
    $ rawdir=.crypt      # /!\ ADAPT accordingly
    $ mountdir=vault     # /!\ ADAPT accordingly
    #
    # (eventually) Ignore the mount dir
    $ echo $mountdir >> .gitignore
    ### EncFS: Creation of an EncFS vault (only once)
    $ encfs --standard $rawdir $mountdir
    ```

=== "GoCryptFS"
    you SHOULD be on a computing node to use [GoCryptFS](https://nuetzlich.net/gocryptfs/).

    ```bash
    $ cd /path/to/my/project
    $ rawdir=.crypt      # /!\ ADAPT accordingly
    $ mountdir=vault     # /!\ ADAPT accordingly
    #
    # (eventually) Ignore the mount dir
    $ echo $mountdir >> .gitignore
    ### GoCryptFS: load the module - you SHOULD be on a computing node
    $ module load tools/gocryptfs
    # Creation of a GoCryptFS vault (only once)
    $> gocryptfs -init $rawdir
    ```

Then you can mount/unmount the vault as follows:


| Tool      | OS     | Opening/Unlocking the vault                       | Closing/locking the vault |
|-----------|--------|---------------------------------------------------|---------------------------|
| EncFS     | Linux  | `encfs -o nonempty  --idle=60  $rawdir $mountdir` | `fusermount -u $mountdir` |
| EncFS     | Mac OS | `encfs  --idle=60  $rawdir $mountdir`             | `umount $mountdir`        |
| GocryptFS |        | `gocryptfs $rawdir $mountdir`                     | as above                  |

The fact that [GoCryptFS](https://nuetzlich.net/gocryptfs/) is available as a module brings the advantage that it can be mounted in a _view_ folder (`vault/`) where you can read and write the unencrypted files, which is _Automatically_ unmounted upon job termination.


## File Encryption using SSH [RSA] Key Pairs

* Man pages: [`openssl rsa`](https://www.openssl.org/docs/manmaster/man1/openssl-rsa.html), [`openssl rsautl`](https://www.openssl.org/docs/manmaster/man1/openssl-rsautl.html) and [`openssl enc`](https://www.openssl.org/docs/manmaster/man1/openssl-enc.html)
* [Tutorial: Encryption with RSA Key Pairs](http://krisjordan.com/essays/encrypting-with-rsa-key-pairs)
* [Tutorial: How to encrypt a big file using OpenSSL and someone's public key](https://www.czeskis.com/random/openssl-encrypt-file.html)
* [OpenSSL Command-Line HOWTO](https://www.madboa.com/geek/openssl/), in particular the section ['How do I simply encrypt a file?'](https://www.madboa.com/geek/openssl/#encrypt-simple)

If you encrypt/decrypt files or messages on more than a one-off occasion, you should really use GnuPGP as that is a much better suited tool for this kind of operations.
But if you already have someone's public SSH key, it can be convenient to use it, and it is safe.

!!! warning
    The below instructions are *NOT* compliant with the _new OpenSSH format_ which is used for storing encrypted (or unencrypted) RSA, EcDSA and Ed25519 keys (among others) when you use the `-o` option of `ssh-keygen`.
    You can recognize these keys by the fact that the private SSH key `~/.ssh/id_rsa` starts with `-
    ----BEGIN OPENSSH PRIVATE KEY-----`

### Encrypt a file using a public SSH key

__(eventually) SSH RSA public key conversion to PEM PKCS8__

OpenSSL encryption/decryption operations performed  using the RSA algorithm relies on keys following the PEM format [^pem] (ideally in the  PKCS#8 format).
It is possible to convert OpenSSH _public_ keys (private ones are already compliant) to the PEM PKCS8 format (a more secure format).
For that one can either use the [`ssh-keygen`](https://man.openbsd.org/ssh-keygen.1) or the [`openssl`](https://www.openssl.org/) commands, the first one being recomm
ended.

```bash
# Convert the public key of your collaborator to the PEM PKCS8 format (a more secure format)
$ ssh-keygen -f id_dst_rsa.pub -e -m pkcs8 > id_dst_rsa.pkcs8.pub
# OR use OpenSSL for that...
$ openssl rsa -in id_dst_rsa -pubout -outform PKCS8 > id_dst_rsa.pkcs8.pub
```
Note that you don't actually need to save the PKCS#8 version of his public key file -- the below command will make this conversion on demand.

__Generate a 256 bit (32 byte) random symmetric key__

There is a limit to the maximum length of a message _i.e._ size of a file  that can be encrypted using asymmetric RSA public key encryption keys (which is what SSH ke
ys are).
For this reason, you should better rely on a 256 bit key to use for symmetric AES encryption and then encrypt/decrypt that symmetric AES key with the asymmetric RSA k
eys
This is how encrypted connections usually work, by the way.

Generate the _unique_ symmetric key `key.bin` of 32 bytes (_i.e._ 256 bit) as follows:

```
openssl rand -base64 32 -out key.bin
```

You should only use this key **once**. If you send something else to the recipient at another time, you should regenerate another key.

__Encrypt the (potentially big) file with the symmetric key__


```bash
openssl enc -aes-256-cbc -salt -in bigdata.dat -out bigdata.dat.enc  -pass file:./key.bin
```

??? info "Indicative performance of OpenSSL Encryption time"
    You can quickly generate random files of 1 or 10 GiB size as follows:
    ```bash
    # Random generation of a 1GiB file
    $ dd if=/dev/urandom of=bigfile_1GiB.dat  bs=64M count=16  iflag=fullblock
    # Random generation of a 1GiB file
    $ dd if=/dev/urandom of=bigfile_10GiB.dat bs=64M count=160 iflag=fullblock
    ```
    An indicated encryption time taken for above generated random file on a local laptop (Mac OS X, local filesystem over SSD) is proposed in the below table, using
    ```
    openssl enc -aes-256-cbc -salt -in bigfile_<N>GiB.dat -out bigfile_<N>GiB.dat.enc  -pass file:./key.bin
    ```

    | File                | size   | Encryption time |
    |---------------------|--------|-----------------|
    | `bigfile_1GiB.dat`  | 1 GiB  | 0m5.395s        |
    | `bigfile_10GiB.dat` | 10 GiB | 2m50.214s       |


__Encrypt the symmetric key, using your collaborator public SSH key in PKCS8 format:__

```bash
$ openssl rsautl -encrypt -pubin -inkey <(ssh-keygen -e -m PKCS8 -f id_dst_rsa.pub) -in key.bin -out key.bin.enc
# OR, if you have a copy of the PKCS#8 version of his public key
$ openssl rsautl -encrypt -pubin -inkey  id_dst_rsa.pkcs8.pub -in key.bin -out key.bin.enc
```

Delete the unencrypted symmetric key as you don't need it any more (and you should not use it anymore)

      $> rm key.bin

Now you can transfer the `*.enc` files _i.e._ send the (potentially big) encrypted file `<file>.enc` and the encrypted symmetric key (_i.e. `key.bin.enc` ) to the recipient _i.e._ your collaborator.
Note that you are encouraged to send the encrypted file and the encrypted key separately. Although it's not absolutely necessary, it's good practice to separate the two.
If you're allowed to, transfer them by SSH to an agreed remote server. It is even safe to upload the files to a public file sharing service and tell the recipient to download them from there.


### Decrypt a file encrypted with a public SSH key

First decrypt the symmetric key using the SSH private counterpart:

```bash
# Decrypt the key -- /!\ ADAPT the path to the private SSH key
$ openssl rsautl -decrypt -inkey ~/.ssh/id_rsa -in key.bin.enc -out key.bin
Enter pass phrase for ~/.ssh/id_rsa:
```

Now the (potentially big) file can be decrypted, using the symmetric key:

```
openssl enc -d -aes-256-cbc -in bigdata.dat.enc -out bigdata.dat -pass file:./key.bin
```

[^pem]: Defined in RFCs [1421](https://tools.ietf.org/html/rfc1421) through [1424](https://tools.ietf.org/html/rfc1424), is a container format for public/private keys or certificates used preferentially by open-source software such as [OpenSSL](https://www.openssl.org/). The name is from [Privacy Enhanced Mail (PEM)](https://en.wikipedia.org/wiki/Privacy-enhanced_Electronic_Mail) (a _failed_ method for secure email, but the container format it used lives on, and is a base64 translation of the x509 ASN.1 keys.

### Misc Q&D for small files

For a 'quick and dirty' encryption/decryption of _small_ files:

```bash
# Encrypt
$  openssl rsautl -encrypt -inkey <(ssh-keygen -e -m PKCS8 -f ~/.ssh/id_rsa.pub) -pubin -in <cleartext_file>.dat -out <encrypted_file>.dat.enc
# Decrypt
$ openssl rsautl -decrypt -inkey ~/.ssh/id_rsa -in <encrypted_file>.dat.enc -out <cleartext_file>.dat
```


## Data Encryption in Git Repository with `git-crypt`

It is of course even more important __in the context of git repositories__, whether public or private, since the disposal of a working copy of the repository enable the access to the full history of commits, in particular the ones eventually done by mistake (`git commit -a`) that used to include sensitive files.
That's where [git-crypt](https://www.agwa.name/projects/git-crypt/) comes for help.
It is an open source, command line utility that empowers developers to protect specific files within a git repository.

> git-crypt enables transparent encryption and decryption of files in a git repository.
> Files which you choose to protect are encrypted when committed, and decrypted when checked
> out. git-crypt lets you freely share a repository containing a mix of public and private
> content. git-crypt gracefully degrades, so developers without the secret key can still
> clone and commit to a repository with encrypted files. This lets you store your secret
> material (such as keys or passwords) in the same repository as your code, without
> requiring you to lock down your entire repository.

The biggest advantage of [git-crypt](https://github.com/AGWA/git-crypt) is that private data and public data can live in the same location.


## PetaSuite Protect

[PetaSuite](https://www.petagene.com/products/) is a compression suite for Next-Generation-Sequencing (NGS) data.
It consists of a command-line tool and a user-mode library. The command line tool performs compression and decompression operations on files. The user-mode library allows other tools and pipelines to transparently access the NGS data in their original file formats.

PetaSuite is used within LCSB and provides the following features:

* Encrypt and compress genomic data
* Encryption keys and access managed centrally
* Decryption and decompression on-the-fly using a library that intercepts all FS access

This is a commercial software -- contact `lcsb.software@uni.lu` if you would like to use it
