# Get an Account

In order to use the ULHPC facilities, you need to have a user account with an associated user login name (also called username) placed under an account hierarchy.

## Conditions of acceptance

### Acceptable Use Policy (AUP)

{%
   include-markdown "../policies/aup.md"
   start="<!--intro-start-->"
   end="<!--intro-end-->"
%}

Remember that **you are expected to acknowledge ULHPC in your publications**.
See [Acceptable Use Policy](../policies/aup.md) for more details.

??? warning "ULHPC Platforms are meant ONLY for R&D!"
    The ULHPC facility is made for Research and Development and it is **NOT** a full production computing center -- for such needs, consider using the [National HPC center](https://luxprovide.lu).

    In particular, we cannot make any guarantees of cluster availability or timely job completion even if we target a minimum compute node availability above 95% which is typically met - for instance, past KPI statistics in 2019 report a computing node availability above 97%.

### Resource allocation policies

[:fontawesome-solid-sign-in-alt: ULHPC Usage Charging and Resource allocation policy](../policies/usage-charging.md){: .md-button .md-button--link }

#### UL internal R&D and training

{%
   include-markdown "../policies/usage-charging.md"
   start="<!--resource-allocation-ul-start-->"
   end="<!--resource-allocation-ul-end-->"
%}

#### Research Projects

{%
   include-markdown "../policies/usage-charging.md"
   start="<!--resource-allocation-project-start-->"
   end="<!--resource-allocation-project-end-->"
%}


#### Externals and private partners

{%
   include-markdown "../policies/usage-charging.md"
   start="<!--resource-allocation-externals-start-->"
   end="<!--resource-allocation-externals-end-->"
%}

----------------------------------
## How to Get a New User account?


[:fontawesome-solid-file-signature: Account Request Form](https://service.uni.lu/sp?id=sc_cat_item&sys_id=358906c98776c610aa6d65740cbb35e6&sysparm_category=9c992749db8f84109aa59ee3db96196f){: .md-button .md-button--link }


1. University staff - you can submit a request for a new ULHPC account by using the [ServiceNow portal (Research > HPC > User access & accounts > New HPC account request)](https://service.uni.lu/sp?id=sc_cat_item&sys_id=358906c98776c610aa6d65740cbb35e6&sysparm_category=9c992749db8f84109aa59ee3db96196f).  
Students - submit your account request on the [Student Service Portal](https://service.uni.lu/ssp).  
Externals - a University staff member must request the account for you, using the section [New HPC account for external](https://service.uni.lu/sp?id=sc_cat_item&sys_id=b12bce4d8776c610aa6d65740cbb3536&sysparm_category=9c992749db8f84109aa59ee3db96196f). Enter the professional data (organization and institutional email address). Specify the line manager / project PI if needed.
2. If you need to access a specific project directory, ask the project directory owner to open a ticket using the section [Add user within project](https://service.uni.lu/sp?id=sc_cat_item&sys_id=47f37b09dbcf84109aa59ee3db9619a5&sysparm_category=9c992749db8f84109aa59ee3db96196f).
3. Your account will undergo user checks, in accordance with ULHPC policies, to verify your identity and the information proposed. Under some circumstances, there could be a delay while this vetting takes place.
4. After vetting has completed, you will receive a welcome email with your login information, and a unique link to a [PrivateBin](https://privatebin.info/) [^1] holding a random temporary password. That link will expire if not used within 24 hours.
The PI and PI Proxies for the project will be notified when applicable.
5. Finally, you will need to log into the [HPC IPA](https://hpc-ipa.uni.lu/ipa/ui/) Portal to set up your initial password and Multi-Factor Authentication (MFA) for your account.
    * **Your new password must adhere to ULHPC's password requirements**
        - see  [Password policy and guidelines](../policies/passwords.md)
    * [ULHPC Identity Management (IPA portal) documentation](../connect/ipa.md)


??? warning "UL HPC $\neq$ University credentials"
    Be aware that the source of authentication for the HPC services based on [RedHat IdM/IPA](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/linux_domain_identity_authentication_and_policy_guide/index) **DIFFERS** from the University credentials (based on UL Active Directory).

    * ULHPC credentials are maintained by the HPC team; associated portal: <https://hpc-ipa.uni.lu/ipa/ui/>
        - authentication service for: UL HPC
    * University credentials are maintained by the IT team of the University
        - authentication service for Service Now and all other UL services

[^1]: [PrivateBin](https://privatebin.info/) is a minimalist, open source online [pastebin](https://pastebin.com/) where the server has zero knowledge of pasted data. Data is encrypted / decrypted in the browser using 256bit AES in Galois Counter mode.

## Managing User Accounts

ULHPC user accounts are managed in through the [HPC IPA web portal](../connect/ipa.md).

## Security Incidents

If you think there has been a computer security incident, you should contact the ULHPC Team and the [University CISO](https://www.uni.lu/en/about/organisation/administration/it-security-team/) team as soon as possible:

> To: [hpc-team@uni.lu,laurent.weber@uni.lu](mailto:hpc-team@uni.lu,laurent.weber@uni.lu)

> Subject: Security Incident for HPC account '`<login>`' (**ADAPT accordingly**)

Please save any evidence of the break-in and include as many details as possible in your communication with us.

--------------------------------------
## How to Get a New Project account?

Projects are defined for accounting purposes and are associated to a set of user accounts allowed by the project PI to access its data and submit jobs on behalf of the project account. See [Slurm Account Hierarchy](../slurm/accounts.md).

You can request (or be automatically added) to project accounts for accounting purposes.
For more information, please see the [Project Account documentation](../accounts/projects.md)


## FAQ

### Can I share an account? – Account Security Policies


!!! danger
    The sharing of passwords or login credentials is **not allowed** under UL HPC and University information security policies. Please bear in mind that this policy also protects the end-user.

Sharing credentials removes the ability to audit and accountability for the account holder in case of account misuse. Accounts which are in violation of this policy may be disabled or otherwise limited. Accounts knowingly skirting this policy may be banned.

If you find that you need to share resources among multiple individuals, shared [projects](../accounts/projects.md) are just the way to go, and remember that the University extends access to its HPC resources (_i.e._, facility and expert HPC consultants) to the scientific staff of national public organizations and external partners for the duration of joint research projects under the conditions defined above.

When in doubt, please [contact us](../support/index.md) and we will be happy to assist you with finding a safe and secure way to do so.
