# Services

The ULHPC Team is committed to excellence and support of the University research community through several side services:

* __[ULHPC Gitlab](https://gitlab.uni.lu)__, a comprehensive version control and collaboration (VC&C) solution to deliver better software faster.
* __[Gforge @ Uni.lu](https://gforge.uni.lu/)__, based on FusionForge, is the seminal web-based project management and collaboration system deployed at the university.
    - **:fontawesome-solid-exclamation-triangle: This service will be decommissioned by end of 2020**

* __[Etherpad](https://hpc.uni.lu/pad/)__ - a  web-based collaborative real-time editor
* __[Privatebin](https://hpc.uni.lu/privatebin/)__ - secured textual data sharing

## Gitlab @ Uni.lu

[![](https://gitlab.uni.lu/uploads/-/system/appearance/logo/1/gitlab-logo-gray-rgb-small.png){: style="width:300px; float:right;" }](https://gitlab.uni.lu)

Gitlab is an open source software to collaborate on code, very similar to [Github](https://github..com).
You can manage git repositories with fine grained access controls that keep your code secure and perform code reviews and enhance collaboration with merge requests. Each project can also have an issue tracker and a wiki.

The GitLab service is available for UL HPC platform users with [their ULHPC account](accounts/index.md) and to their external collaborators that have a GitHub account.

!!! warning "[Github] External accounts access are BLOCKED by default"
    * By default, external (github) accounts are **denied** and **blocked** on the Gitlab service.
         - Access can be granted **on-demand** after careful review of the ULHPC team and attached to the project indicated by the UL[HPC] PI in charge of the external.
    * _Note_: externals cannot create groups nor projects.

## Gforge @ Uni.lu


[![](https://gforge.uni.lu/images/fusionforge-resized.png){: style="width:250px; float:right;" }](https://gforge.uni.lu)

Outside [Gitlab](https://gitlab.uni.lu), the seminal web-based project management and collaboration system deployed at the university was the [Gforge @ Uni.lu](https://gforge.uni.lu) service.
Inspired by the [InriaGforge](https://gforge.inria.fr/), the general principle is to offer easy access through projects to subversion repositories, mailing lists, bug trackers, message boards/forums, task management, site hosting, permanent file archival, full backups, and total web-based administration. The major features are listed in [helpdesk website](https://helpdesk.gforge.uni.lu/).
Access to GForge is through dedicated accounts, (requested by mail: [admin@gforge.uni.lu](mailto:admin@gforge.uni.lu)), for both UL members and external partners.


**Service feature comparison between GForge ([gforge.uni.lu](https://gforge.uni.lu)) and GitLab ([gitlab.uni.lu](https://gitlab.uni.lu))**

| Service                         | Git              | SVN/Subversion   | ULHPC users      | External Users                                   | Static websites hosting   |
| :-------:                       | :---:            | :--------------: | :-----------:    | :--------------:                                 | :-----------------------: |
| [GForge](https://gforge.uni.lu) | :material-check: | :material-check: | :material-check: | :material-check:                                 | :material-check:          |
| [GitLab](https://gitlab.uni.lu) | :material-check: | :material-close: | :material-check: | :material-close: <br/><small>(restricted use)</small> | :material-close:          |

!!! danger "Gforge service will be decommissioned EOY 2020"
    * __Situation__: the [Gforge @ Uni.lu](https://gforge.uni.lu) service has been in production since 2008 and kept up-to-date until now.
    Nevertheless, the underground product line (Gforge, moved to FusionForge after the a break-up of the original open source project in february 2009) proved to be hard to maintained, security fixes takes time to be integrated and the few unique features of the service (SVN support, static website hosting) no longer justify the maintenance effort as more recent and sustainable alternatives emerged.

    ** For this reason, the Gforge service will be no longer available as of Dec 31, 2020**

    * __Migration Plan for project repositories__
        - For SVN-based projects: [Migrate to Git](https://www.atlassian.com/git/tutorials/migrating-overview)
        - Favor __public hosting services__ for your project as [github.com](https//github.com)
            * Github offers both private and public projects management free of charge
            * Github also supports [SVN clients](https://docs.github.com/en/github/importing-your-projects-to-github/support-for-subversion-clients)
        - consider _self-hosted_ solutions on servers you can maintain as [gitolite](https://gitolite.com/gitolite/index.html) or [gitea](https://gitea.io/)
        - As a last resort, consider using one of the Gitlab instances running in the different department of the university, or the ULHPC gitlab

        You can then update the Git remote url to transition to the new host for your git project as follows:
        ```bash
        git remote set-url origin [...]
        ```
        This will **allow you to keep all commit history**. Nevertheless, consider that all other information part of your Gforge project (tickets, project  and forum messages etc.) will be **lost** once Gforge is declared out-of-service.

    * __Alternative to Gforge features__
        - _Git repository hosting_: see above
        - _Project Management/Bug Tracking_: see above as all proposed alternatives ([Github](github.com) etc.) supports this feature
        - _SVN repository hosting_:
            * if you really need to stick to SVN, consider [RhodeCode](https://rhodecode.com/) or [Assembla](https://www.assembla.com/subversion)
        - _Mailing list_:
            * The IT service of the university can grant you administration rights on a custom mailing-list upon demand of the service portal
        - _Static website hosting_: if you really need to maintain a static website, consider:
            * [Github pages](https://pages.github.com/)
            * [Read the docs](https://readthedocs.org/)
            * Ask the University IT service for a website host

## EtherPad

[![](https://upload.wikimedia.org/wikipedia/commons/f/ff/Logo_Etherpad.png){ align=right }](https://hpc.uni.lu/pad/)

Etherpad is a web-based collaborative real-time editor, allowing authors to simultaneously edit a text document, and see all of the participants' edits in real-time, with the ability to display each author's text in their own color.

## PrivateBin

[![](https://privatebin.info/img/logo.png){: style="width:300px; float:right;" }](https://hpc.uni.lu/privatebin/)

PrivateBin is a minimalist, open source online [pastebin](https://en.wikipedia.org/wiki/Pastebin) where the server has zero knowledge of pasted data.
<br/>
Data is encrypted and decrypted in the browser using 256bit AES in Galois Counter mode.
