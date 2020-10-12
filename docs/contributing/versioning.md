The operation consisting of releasing a new version of this repository is automated by a set of tasks within the root `Makefile`.
In this context, a version number have the following format:

      <major>.<minor>.<patch>[-b<build>]

where:

* `< major >` corresponds to the major version number
* `< minor >` corresponds to the minor version number
* `< patch >` corresponds to the patching version number
* (eventually) `< build >` states the build number _i.e._ the total number of commits within the `devel` branch.

Example: \`1.0.0-b28\`.

!!! tips "`VERSION` file"
    The current version number is stored in the root file `VERSION`.
    __/!\ IMPORTANT: NEVER MAKE ANY MANUAL CHANGES TO THIS FILE__

!!! danger "`ULHPC/docs` repository release"
    Only the ULHPC team is allowed to perform the releasing operations (and push to the `production` branch).
    By default, the main documentation website is built against the `production` branch.

For more information on the version, run:

     $> make versioninfo


??? info "ULHPC Team procedure for repository release"
    If a new version number such be bumped, the following command is issued:
    ```bash
    make start_bump_{major,minor,patch}
    ```
    This will start the release process for you using `git-flow` within the `release/<new-version>` branch - see also [Git(hub) flow](index.md).
    Once the last changes are committed, the release becomes effective by running:
    ```bash
    make release
    ```
    It will finish the release using `git-flow`, create the appropriate tag in the `production` branch and merge all things the way they should be in the `master` branch.
