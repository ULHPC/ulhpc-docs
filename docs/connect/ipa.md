# ULHPC Identity Management Portal (IdM/IPA)

[:fontawesome-solid-link: ULHPC Identity Management Portal](https://hpc-ipa.uni.lu/ipa/ui/){: .md-button .md-button--link }

Red Hat Identity Management (IdM), formally referred to as IPA ("Identity, Policy, and Audit" -- see also
<https://www.freeipa.org>),  provides a centralized and unified way to manage
identity stores, authentication, policies, and authorization policies in a
Linux-based domain. IdM significantly reduces the administrative overhead of
managing different services individually and using different tools on different
machines.

All services (HPC and complementary ones) managed by the ULHPC team rely on a
highly redundant setup involving several Redhat IdM/IPA server.

!!! tips "SSH Key Management"
    You are responsible for uploading and managing your _authorized_ public SSH
    keys for your account, under the terms of the [Acceptable Use Policy](../policies/aup.md).
    **Be aware that the ULHPC team review on a periodical basis the compliance to the policy, as well as the security of your keys.**
    See also the [note on deprecated/weak DSA/RSA keys](troubleshooting.md#access-denied-or-permission-denied-publickey)

_References_

* [Redhat 7 Documentation](https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/7/html/Linux_Domain_Identity_Authentication_and_Policy_Guide/introduction.html)

## Upload your SSH key on the ULHPC Identity Management Portal

You should upload your public SSH key(s) `*.pub` to your user entry on the  ULHPC Identity Management Portal.
For that, connect to the ULHPC IdM portal (use the URL communicated to you by the UL HPC team in your "welcome" mail) and enter your **ULHPC** credentials.

![](https://access.redhat.com/webassets/avalon/d/Red_Hat_Enterprise_Linux-7-Linux_Domain_Identity_Authentication_and_Policy_Guide-en-US/images/0b67bd0c53b2b26b1d9ce416280f1e83/web_ui_login_screen.png)

First copy the content of the key you want to add

``` bash
# Example with ED25519 **public** key
(laptop)$> cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAA[...]
# OR the RSA **public** key
(laptop)$> cat ~/.ssh/id_rsa.pub
ssh-rsa AAAA[...]
```

Then on the portal:

1. Select Identity / Users.
2. Select your login entry
3. Under the Settings tab in the Account Settings area, click SSH public keys: **Add**.

![](https://access.redhat.com/webassets/avalon/d/Red_Hat_Enterprise_Linux-7-Linux_Domain_Identity_Authentication_and_Policy_Guide-en-US/images/162d5680e990e7cb5f2629377a5d288a/sshkeys-user1.png)

Paste in the Base 64-encoded public key string, and click **Set**.

![](https://access.redhat.com/webassets/avalon/d/Red_Hat_Enterprise_Linux-7-Linux_Domain_Identity_Authentication_and_Policy_Guide-en-US/images/fbb26af5fd8a911253a61cde7240d3b4/sshkeys-user3.png)

Click **Save** at the top of the page.
Your [key fingerprint](ssh.md##key-fingerprints) should be listed now.

![IPA user portal](images/ipa.png)

!!! tips "Listing SSH keys attached to your account through SSSD"
    [SSSD](https://sssd.io/) is a system daemon used on ULHPC computational
    resources. Its primary function is to provide access to local or remote
    identity and authentication resources through a common framework that can
    provide caching and offline support to the system.
    To easily access the _authorized_ keys configured for your account from the
    command-line (i.e. without login on the ULHPC IPA portal), you can use:
    ```
    sss_ssh_authorizedkeys $(whoami)
    ```

## Change Your Password

1. connect to the ULHPC IdM portal (use the URL communicated to you by the UL
   HPC team in your "welcome" mail) and enter your **ULHPC** credentials.
2. On the top right under your name, select the entry "Change Password"
3.  In the dialog window that appears, enter the current password,
    and your new password. Your password should meet the password
    requirements explained in the next section below, and must be
    'safe' or 'very safe' according to the provided password strength
    meter.
