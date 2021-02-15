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

??? warning "ULHPC Platforms are meant for R&D!"
    Note that the ULHPC facility is made for Research and Development and it is **NOT** a full production computing center -- for such needs, consider using the [national HPC center](https://luxprovide.lu).

    In particular, we cannot make any guarantees of cluster availability or timely job completion even if we target a minimum compute node availability above 95% which is typically met - for instance, past KPI statistics in 2019 report a computing node availability above 97%.

### General conditions for UL staff

As soon as you belong to the [University of Luxembourg](https://www.uni.lu) and that you accept to conform to the IT rules of the university as well as the [UL HPC Acceptable Use Policy (AUP)](https://hpc.uni.lu/download/documents/Uni.lu-HPC-Facilities_Acceptable-Use-Policy_v2.0.pdf), you are eligible for having an HPC account.

### HPC Resource Allocations for Research Projects and External Partners

The University extends access to its HPC resources (_i.e._, facility and expert HPC consultants) to the scientific staff of national public organizations and external partners for the duration of joint research projects under the conditions defined in the [below document](https://hpc.uni.lu/download/documents/Uni.lu-HPC-Facilities_Resource Allocations_for_Research_Projects_and_External_Partners.pdf)

<p class="text-center">
<button type="button" class="btn btn-light"><a href="https://hpc.uni.lu/download/documents/Uni.lu-HPC-Facilities_Resource Allocations_for_Research_Projects_and_External_Partners.pdf">Resource Allocations for Research Projects and External Partners [pdf]</a></button>
</p>


----------------------------------
## How to Get an New User account?

<p class="text-center">
<button type="button" class="btn btn-light">
   <a href="http://ulsurvey.uni.lu/index.php/723213?lang=en">
   <strong>Account Request Form</strong>
   </a>
</button>
</p>

1. You can submit a request for a new ULHPC account by using the
[Create a ULHPC account form](http://ulsurvey.uni.lu/index.php/723213?lang=en) form.
2. Enter your personal data,  your organization and your institutional contact information. Specify your direct line manager / project PI. Eventually, if you need to access a specific project directory, mention it in comment. This will be granted only after approval of the project PI.
3. Your account will undergo user checks, in accordance with ULHPC policies, to verify your identity and the information proposed. Under some circumstances, there could be a delay while this vetting takes place.
4. After vetting has completed, you will receive a welcome email with your login information, and a unique link to a [PrivateBin](https://privatebin.info/) [^1] holding a random temporary password. That link will expire if not used within 24 hours.
The PI and PI Proxies for the project will be notified when applicable.
5. Finally, you will need to log into the [HPC IPA](https://***REMOVED***) Portal to set up your initial password and Multi-Factor Authentication (MFA) for your account.
    * **Your new password must adhere to ULHPC's password requirements**
        - see  [Password policy and guidelines](passwords.md)
    * [ULHPC Identity Management (IPA portal) documentation](ipa.md)



??? warning "UL HPC $\neq$ University credentials"
    Be aware that the source of authentication for the HPC services (**including [gitlab.uni.lu](https://gitlab.uni.lu)**), based on [RedHat IdM/IPA](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/linux_domain_identity_authentication_and_policy_guide/index) **DIFFERS** from the University credentials (based on UL Active Directory).

    * ULHPC credentials are maintained by the HPC team; associated portal: <https://***REMOVED***>
        - authentication service for: UL HPC, Gitlab
    * University credentials are maintained by the IT team of the University
        - authentication service for Service Now and all other UL services

[^1]: [PrivateBin](https://privatebin.info/) is a minimalist, open source online [pastebin](https://pastebin.com/) where the server has zero knowledge of pasted data. Data is encrypted / decrypted in the browser using 256bit AES in Galois Counter mode.

--------------------------
## Managing User Accounts

ULHPC user accounts are managed in through the [HPC IPA web portal](https://***REMOVED***).
For more information on how to use it, please see the [IPA documentation](accounts/ipa.md).

## Security Incidents

If you think there has been a computer security incident you should contact the ULHPC Team and the [University CISO](https://wwwen.uni.lu/university/about_the_university/organisation_charts/organisation_chart_rectorate_central_administration/le_service_informatique_de_l_universite/ciso) team as soon as possible:

> To: [hpc-team@uni.lu,christian.hutter@uni.lu](mailto:hpc-team@uni.lu,christian.hutter@uni.lu)

> Subject: Security Incident for HPC account '`<login>`' (**ADAPT accordingly**)

Please save any evidence of the break-in and include as many details as possible in your communication with us.

--------------------------------------
## How to Get an New Project account?

Projects are defined for accounting purposes and are associated to a set of user accounts allowed by the project PI to access its data and submit jobs on behalf of the project account.

For more information, please see the [Project Management documentation](accounts/projects.md)


## FAQ

### Can I share an account? – Account Security Policies


!!! danger
    The sharing of passwords or login credentials is **not allowed** under UL HPC and University information security policies. Please bear in mind that this policy also protects the end-user.

Sharing credentials removes the ability to audit and accountability for the account holder in case of account misuse. Accounts which are in violation of this policy may be disabled or otherwise limited. Accounts knowingly skirting this policy may be banned.

If you find that you need to share resources among multiple individuals, shared [projects](accounts/projects.md) are just the way to go, and remember that the University extends access to its HPC resources (_i.e._, facility and expert HPC consultants) to the scientific staff of national public organizations and external partners for the duration of joint research projects under the conditions defined above.

When in doubt, please [contact us](contact.md) and we will be happy to assist you with finding a safe and secure way to do so.
