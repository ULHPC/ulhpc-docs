## Password and Account Protection

A user is given a username (also known as a login name) and associated
password that permits her/him to access ULHPC resources.  This
username/password pair may be used by a **single** individual only:
*passwords must not be shared with any other person*. Users who
share their passwords will have their access to ULHPC disabled.

!!! tip "Do not confuse your UL[HPC] password/passphrase and your SSH passphrase"
    We sometimes receive requests to reset your SSH passphrase, which is something you control upon SSH key generation - see [SSH documentation](../connect/ssh.md).

Passwords must be changed as soon as possible after exposure or
suspected compromise. Exposure of passwords and suspected compromises
must immediately be reported to ULHPC and the University CISO (see below).
In all cases, recommendations for the creation of strong passwords is proposed [below](#password-requirements-and-guidelines).


### Password Manager

You are **strongly** encouraged also to rely on password manager applications to store your different passwords. You may want to use your browser embedded solution but it's not the safest option.
Here is a list of recommended applications:

* [BitWarden](https://bitwarden.com/) - free with no limits ($10 per year for families) - [Github](https://github.com/bitwarden)
* [Dashlane](https://www.dashlane.com) - free for up to 50 passwords - 40€ per year for premium (60€ for families)
* [LastPass](https://www.lastpass.com/)
* [NordPass](https://nordpass.com/) - free version limited to one device with unlimited number of passwords; 36$ per year for premium plan
* [1Password](https://1password.com/) - paid version only (yet worth it) with 30-day free trial, 36$ per year (60$ for families)
* _Self-Hosted solutions_:
    - [KeepassXC](https://keepassxc.org/download/)
    - [`pass`: the Standard Unix Password Manager](https://www.passwordstore.org/).
        <!-- * See also [our tutorial on pass setup within the ULHPC team](services/pass.md) -->


### Forgotten Passwords

If you forget your password or if it has recently expired, you can simply [contact us](../support/index.md) to initiate the process of resetting your password.

### Login Failures

Your login privileges will be disabled if you have several login failures
while entering your password on a ULHPC resource. You do not need
a new password in this situation. The login failures will be
automatically cleared after a couple of minutes. No additional actions are
necessary.


## How To Change Your Password on IPA

See [IPA documentation](../connect/ipa.md#change-your-password)

!!! tip
    Passwords must be changed under any one of the following circumstances:

    *  Immediately after someone else has obtained your password (do *NOT* give your password to anyone else).
    *  As soon as possible, but at least within one business day after a password has been compromised or after you suspect that a password has been compromised.
    *  On direction from ULHPC staff, or by IPA password policy requesting to frequently change your password.

**Your new password must adhere to ULHPC's password requirements.**

## Password Requirements and Guidelines

One of the potentially weakest links in computer security is the individual password. Despite the University's and ULHPC's efforts to keep hackers out of your personal files and away from University resources (e.g., email, web files, licensed software), easily-guessed passwords are still a big problem so you should really pay attention to the following guidelines and recommendations.

Recently, the National Institute of Standards and Technology (NIST) has updated
their Digital Identity Guidelines in [Special Publication
800-63B](https://pages.nist.gov/800-63-3/sp800-63b.html).
We have updated our password policy to bring it in closer alignment with this guidelines. In particular, the updated guidance is counter to the long-held philosophy that passwords must be long and complex. In contrast, the new guidelines recommend that passwords should be "__easy to remember__" but "__hard to guess__", allowing for usability and security to go hand-in-hand.
Inpired with other password policies and guidelines ([Stanford](https://uit.stanford.edu/service/accounts/passwords), [NERSC](https://docs.nersc.gov/accounts/passwords/)), ULHPC thus recommends the usage of  "_pass phrases_" instead of passwords. Pass phrases are longer, but easier to remember than complex passwords, and if well-chosen can provide better protection against hackers.
In addition, the following rules based on password length and usage of [Multi-Factor Authentication (MFA)](connect/mfa.md) must be satisfied:

* The enforced minimum length for accounts _with_ MFA enabled is 8 characters. If MFA is **not** enabled for your account the minimum password length is 14 characters.
* The ability to use all special characters according to the following guidelines (see also the [Stanford Password Requirements Quick Guide](https://uit.stanford.edu/service/accounts/passwords/quickguide)) depending on the password length:
    - 8-11: mixed case letters, numbers, & symbols
    - 12-15: mixed case letters & numbers
    - 16-19: mixed case letters
    - 20+: no restrictions
    - [illustrating image](https://uit.stanford.edu/sites/default/files/images/2014/04/17/pwstrength.jpg)
* Restrict sequential and repetitive characters (e.g. `12345` or `aaaaaa`)
* Restrict context specific passwords (e.g. the name of the site, etc.)
* Restrict commonly used passwords (e.g. `p@ssw0rd`, etc.) and dictionary words
* Restrict passwords obtained from previous breach corpuses
* Passwords must be changed every six months.

If you are struggling to come up with a good password, you can inspire from the following approach:

??? tips "Creating a pass phrase (source: [Stanford password  policy](https://uit.stanford.edu/service/accounts/passwords))"
    A pass phrase is basically just a series of words, which can include spaces, that you employ instead of a single pass "word." Pass phrases should be at least 16 to 25 characters in length (spaces count as characters), but no less. Longer is better because, though pass phrases look simple, the increased length provides so many possible permutations that a standard password-cracking program will not be effective. It is always a good thing to disguise that simplicity by throwing in elements of weirdness, nonsense, or randomness. Here, for example, are a couple pass phrase candidates:

    > pizza with crispy spaniels

    > mangled persimmon therapy

    Punctuate and capitalize your phrase:

    > Pizza with crispy Spaniels!

    > mangled Persimmon Therapy?

    Toss in a few numbers or symbols from the top row of the keyboard, plus some deliberately misspelled words, and you'll create an almost unguessable key to your account:

    > Pizza w/ 6 krispy Spaniels!

    > mangl3d Persimmon Th3rapy?
