
You are more than welcome to contribute to the development of this project.
You are however expected to follow the model of [Github Flow](https://guides.github.com/introduction/flow/) for your contributions.

!!! tips "What is a [good] Git Workflow?"
    A Git Workflow is a recipe or recommendation for how to use Git to accomplish work in a consistent and productive manner. Indeed, Git offers a lot of flexibility in how changes can be managed, yet there is no standardized process on how to interact with Git. The following questions are expected to be addressed by a successful workflow:

    1. __Q1__: Does this workflow scale with team size?
    2. __Q2__: Is it possible to prevent/limit mistakes and errors ?
    3. __Q3__: Is it easy to undo mistakes and errors with this workflow?
    4. __Q4__: Does this workflow permits to easily test new feature/functionnalities before production release ?
    5. __Q5__: Does this workflow allow for Continuous Integration (even if not yet planned at the beginning)
    6. __Q6__: Does this workflow permit to master the production release
    7. __Q7__: Does this workflow impose any new unnecessary cognitive overhead to the team?
    8. __Q8__: The workflow is easy to use/setup and maintain

    In particular, the default "**_workflow_**" centralizedgitl (where everybody just commit to the single `master` branch), while being the only one satisfying Q7, proved to be easily error-prone and can break production system relying on the underlying repository. For this reason, other more or less complex workflows have emerged -- all [feature-branch-based](https://www.atlassian.com/git/tutorials/comparing-workflows/feature-branch-workflow), that supports teams and projects where production deployments are made regularly:

    * [Git-flow](http://nvie.com/posts/a-successful-git-branching-model/), the historical successful workflow featuring two main branches with an infinite lifetime (`production` and `{master | devel}`)
        - all operations are facilitated by the `git-flow` CLI extension
        - maintaining both branches can be bothersome - `make up`
        - the only one permitting to really control production release

    * [Github Flow](https://guides.github.com/introduction/flow/), a lightweight version with a single branch (`master`)
        - pull-request based - requires interaction with Gitlab/Github web interface (`git request-pull` might help)

    The ULHPC team enforces an hydrid workflow detailed [below](#ulhpc-git-workflow), **HOWEVER** you can safely contribute to this documentation by following the [Github Flow](https://guides.github.com/introduction/flow/) explained now.

## Default Git workflow for contributions

We expect contributors to follow the [Github Flow](https://guides.github.com/introduction/flow/) concept.

![](images/github_flow.png)

This flow is ideal for organizations that need simplicity, and roll out frequently. If you are already using Git, you are probably using a version of the Github flow. Every unit of work, whether it be a bugfix or feature, is done through a branch that is created from master. After the work has been completed in the branch, it is reviewed and tested before being merged into master and pushed out to production.

In details:

* As preliminaries (to be done only once),  __[Fork](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) the `ULHPC/ulhpc-docs` repository under `<YOUR-USERNAME>/ulhpc-docs`__
    - A _fork_ is a copy of a repository placed under your Github namespace. Forking a repository allows you to freely experiment with changes without affecting the original project.
    - In the top-right corner of the  `ULHPC/ulhpc-docs` repository, click "Fork" button.
    - Under Settings, change the repository name from `docs` to `ulhpc-docs`
    - Once done, you can clone your __copy__ (forked) repository: select the SSH url under the "Code" button:
    ```bash
    # (Recommended) Place your repo in a clean (and self-explicit) directory layout
    # /!\ ADAPT 'YOUR-USERNAME' with your Github username
    $> mkdir -p ~/git/github.com/YOUR-USERNAME
    $> cd ~/git/github.com/YOUR-USERNAME
    # /!\ ADAPT 'YOUR-USERNAME' with your Github username
    git clone git@github.com:YOUR-USERNAME/ulhpc-docs.git
    $> cd ulhpc-docs
    $> make setup
    ```
    - Configure your working forked copy to sync with the original `ULHPC/ulhpc-docs` repository through a dedicated `upstream` [remote](https://git-scm.com/docs/git-remote)
    ```bash
    # Check current remote: only 'origin' should be listed
    $> git remote -v
    origin  git@github.com:YOUR-USERNAME/ulhpc-docs.git (fetch)
    origin  git@github.com:YOUR-USERNAME/ulhpc-docs.git (push)
    # Add upstream
    $> make setup-upstream
    # OR, manually:
    $> git remote add upstream https://github.com/ULHPC/ulhpc-docs.git
    # Check the new remote
    $> git remote -v
    origin  git@github.com:YOUR-USERNAME/ulhpc-docs.git (fetch)
    origin  git@github.com:YOUR-USERNAME/ulhpc-docs.git (push)
    upstream https://github.com/ULHPC/ulhpc-docs.git (fetch)
    upstream https://github.com/ULHPC/ulhpc-docs.git (push)
    ```

    - At this level, you probably want to follow the [setup](../setup.md) instructions to configure your `ulhpc-docs` python virtualenv and deploy locally the documentation with `make doc`
        * access the local documentation with your favorite browser by visiting the URL <http://localhost:8000>

Then, to bring your contributions:

1. __Pull__ the latest changes from the `upstream` remote using:
   ```bash
   make sync-upstream
   ```
2. __Create your own feature branch__ with appropriate name `<name>`:
   ```bash
   # IF you have installed git-flow: {brew | apt | yum |...} install gitflow git-flow
   # /!\ ADAPT <name> with appropriate name: this will create and checkout to branch feature/<name>
   git-flow feature start <name>
   # OR
   git checkout -b feature/<name>
   ```
3. __Commit__ your changes **once** satisfied with them
   ```bash
   git add [...]
   git commit -s -m 'Added some feature'
   ```
4. __Push to the feature branch and publish it__
   ```bash
   # IF you have installed git-flow
   # /!\ ADAPT <name> accordingly
   git-flow feature publish <name>
   # OR
   git push -u origin feature/<name>
   ```
5. __Create a new [Pull Request](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request)__ to submit your changes to the ULHPC team.
   - Commit first!
   ```bash
   # check what would be put in the pull request
   git request-pull master ./
   # Open Pull Request from web interface
   # Github: Open 'new pull request'
   #      Base = feature/<name>,   compare = master
   ```

6. Pull request will be reviewed, eventually with comments/suggestion for modifications -- see [official doc](https://docs.github.com/en/free-pro-team@latest/github/collaborating-with-issues-and-pull-requests/incorporating-feedback-in-your-pull-request)
   - you may need to apply new commits to resolve the comments -- remember to mention the pull request in the commit message with the prefix  '`[PR#<ID>]`' (Ex: `[PR#5]`) in your commit message
   ```bash
   cd /path/to/ulhpc-docs
   git checkout feature/<name>
   git pull
   # [...]
   git add [...]
   # /!\ ADAPT Pull Request ID accordingly
   git commit -s -m '[PR#<ID>] ...'
   ```

After your pull request has been reviewed and __merged__, you can safely delete the feature branch.

```bash
# Adapt <name> accordingly
git checkout feature/<name> # Eventually, if needed
make sync-upstream
git-flow feature finish <name> # feature branch 'feature/<name>' will be merged into 'devel'
#                              # feature branch 'feature/<name>' will be locally deleted
#                              # you will checkout back to the 'master' branch
git push origin --delete feature/<name>   # /!\ WARNING: Ensure you delete the CORRECT remote branch
git push  # sync master branch
```

## ULHPC Git Workflow

Throughout all its projects, the ULHPC team has enforced a stricter workflow for Git repository summarized in the below figure:

![](images/gitflow.png)

The main concepts inherited from both advanced workflows ([Git-flow](http://nvie.com/posts/a-successful-git-branching-model/) and [Github Flow](https://guides.github.com/introduction/flow/)) are listed below:

* The central repository holds **two main branches** with an infinite lifetime:
    - `production`: the *production-ready* branch, used for the deployed version of the documentation.
    - `devel | master | main` (`master` in this case): the main (master) branch where the latest developments intervene (name depends on repository purpose). This is the *default* branch you get when you clone the repository.
* You should **always setup** your local copy of the repository with `make setup`
    - ensure also you have installed the `gitflow` extension
    - ensure you are properly made the initial configuration of git -- see also [sample `.gitconfig`](https://github.com/Falkor/dotfiles/blob/master/git/.gitconfig)

In compliment to the [Github Flow](https://guides.github.com/introduction/flow/) described above, several additional operations are facilitated by the root `Makefile`:

* Initial setup of the repository with `make setup`
* Release of a new version of this repository with `make start_bump_{patch,minor,major}` and `make release`
    - this action is managed by the ULHPC team according to the [semantic versioning](versioning.md) scheme implemented within this this project.
