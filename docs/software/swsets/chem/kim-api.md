### [kim-api](https://openkim.org/)

* [Official website](https://openkim.org/)
* __Category__: Chemistry (chem)
    -  `module load chem/kim-api[/<version>]`

Available versions of [kim-api](https://openkim.org/) on ULHPC platforms:

|    | Version   | Swset   | Architectures      | Clusters   |
|---:|:----------|:--------|:-------------------|:-----------|
|  0 | 2.1.3     | 2019b   | broadwell, skylake | iris       |

> Open Knowledgebase of Interatomic Models. KIM is an API and OpenKIM is a collection of interatomic models (potentials) for atomistic simulations.  This is a library that can be used by simulation programs to get access to the models in the OpenKIM database. This EasyBuild only installs the API, the models can be installed with the package openkim-models, or the user can install them manually by running kim-api-collections-management install user MODELNAME or kim-api-collections-management install user OpenKIM to install them all.
