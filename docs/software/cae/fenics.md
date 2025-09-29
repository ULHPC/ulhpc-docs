[![](https://fenicsproject.org/pub/tutorial/sphinx1/_static/fenics_banner.png){: style="width:200px;float: right;" }](https://fenicsproject.org/)

<!-- Intro start -->

[FEniCS](https://fenicsproject.org/) is a popular open-source computing platform for solving partial differential equations (PDEs) using the finite element method ([FEM](https://en.wikipedia.org/wiki/Finite_element_method)). Originally developed in 2003, the earlier version is now known as legacy FEniCS. In 2020, the next-generation framework [FEniCSx](https://docs.fenicsproject.org/) was introduced, with the latest stable [release v0.9.0](https://fenicsproject.org/blog/v0.9.0/) in October 2024. Though it builds on the legacy FEniCS but introduces significant improvements over the legacy libraries. FEniCSx is composed of the following libraries that support typical workflows: [UFL](https://github.com/FEniCS/ufl) → [FFCx](https://github.com/FEniCS/ffcx) → [Basix](https://github.com/FEniCS/basix) → [DOLFINx](https://github.com/FEniCS/dolfinx), which are the build blocks of it. And new users are encouraged to adopt [FEniCSx](https://fenicsproject.org/documentation/) for its modern features and active development support.

FEniCSx can be installed on [ULHPC](https://www.uni.lu/research-en/core-facilities/hpc/) systems using [Easybuild](https://docs.easybuild.io) or [Spack](https://spack.io/), Below are detailed instructions for each method, 

<!-- Intro end  -->

### Building FEniCS With Spack

Building FEniCSx with Spack on the [ULHPC](https://www.uni.lu/research-en/core-facilities/hpc/) system requires that Users already installed Spack and sourced its enviroment on the cluster. If Spack is not yet configured, follow the [spack documentation](../../environment/spack.md) for installation and configuration.

!!! note 

        Spack would be a good choice for  building FEniCSx because it automatically manages complex dependencies, allows to isolates all installations in a dedicated environment, leverages system-provided packages  in ~/.`spack/packages.yaml` for optimal performance, and simplifies reproducibility and maintenance across different systems.

Create and Activate a  Spack Environment: 

To maintain an isolated installation, create a dedicated Spack environment in a chosen directory.
The following example sets up a stable release of FEniCSx `v0.9.0` in the `fenicsx-test` directory inside the `home` directory:

    cd ~
    spack env create -d fenicsx-test/ 
    spack env activate fenicsx-test/
    
Add the core FEniCSx components and common dependencies:

    spack add py-fenics-dolfinx@0.9.0+petsc4py fenics-dolfinx+adios2+petsc adios2+python petsc+mumps

!!! Additional

    The spack `add command` add abstract specs of packages to the currently active environment and registers them as root `specs` in the environment’s `spack.yaml` file. Alternatively, packages can be predefined directly in the `spack.yaml` file located in`$SPACK_ENV`. 

        spack:
        # add package specs to the `specs` list
        specs:
        - py-fenics-dolfinx@0.9.0+petsc4py
        - fenics-dolfinx+adios2+petsc
        - petsc+mumps
        - adios2+python

        view: true
        concretizer:
            unify: true
    !!! note 
            Replace `@0.9.0` with a different version if you prefer to install others release.
    
??? question  " why unify : true ? "
    
        `unify: true` ensures all packages share the same dependency versions, preventing multiple builds of the same library. Without it, each `spec` could resolve dependencies independently, leading to potential conflicts and redundant installations.

Once Packages `specs` have been added to the current environment, they need to be concretized. 

    spack concretize
    spack install -j16

!!! note 

        Here, [`spack concretize`](https://spack.readthedocs.io/en/latest/environments.html#spec-concretization) resolves all dependencies and selects compatible versions for the specified packages. In addition to adding individual specs to an environment, the `spack install` command installs the entire environment at once and `-j16` option sets the number of CPU cores used for building, which can speed up the installation.
        Once installed, the FEniCSx environment is ready to use on the cluster.

The following are also common dependencies used in FEniCS scripts:

    spack add gmsh+opencascade py-numba py-scipy py-matplotlib
    
It is possible to build a specific version (git ref) of DOLFINx. 
Note that the hash must be the full hash.
It is best to specify appropriate git refs on all components.

    # This is a Spack Environment file.
    # It describes a set of packages to be installed, along with
    # configuration settings.
    spack:
      # add package specs to the `specs` list
      specs:
      - fenics-dolfinx@git.4f575964c70efd02dca92f2cf10c125071b17e4d=main+adios2
      - py-fenics-dolfinx@git.4f575964c70efd02dca92f2cf10c125071b17e4d=main

      - py-fenics-basix@git.2e2a7048ea5f4255c22af18af3b828036f1c8b50=main
      - fenics-basix@git.2e2a7048ea5f4255c22af18af3b828036f1c8b50=main

      - py-fenics-ufl@git.b15d8d3fdfea5ad6fe78531ec4ce6059cafeaa89=main

      - py-fenics-ffcx@git.7bc8be738997e7ce68ef0f406eab63c00d467092=main

      - fenics-ufcx@git.7bc8be738997e7ce68ef0f406eab63c00d467092=main

      - petsc+mumps
      - adios2+python
      view: true
      concretizer:
        unify: true
        
It is also possible to build only the C++ layer using (Need to comment about why we add python depndencies?)

    spack add fenics-dolfinx@0.9.0+adios2 py-fenics-ffcx@0.9.0 petsc+mumps
    
To rebuild FEniCSx from main branches inside an existing environment: 

    spack install --overwrite -j16 fenics-basix py-fenics-basix py-fenics-ffcx fenics-ufcx py-fenics-ufl fenics-dolfinx py-fenics-dolfinx

#### Testing the build

Quickly test the build with

    srun python -c "from mpi4py import MPI; import dolfinx"

!!! info "Try the Build Explicitly" 

        After installation, the [FEniCSx](https://fenicsproject.org/documentation/) build can be tried explicitly by running the demo problems corresponding to the installed release version, as provided in the [FEniCSx documentation](https://docs.fenicsproject.org/).  
        For [DOLFINx](https://docs.fenicsproject.org/dolfinx/main/python/) Python bindings, see for example the demos in the [stable release v0.9.0](https://docs.fenicsproject.org/dolfinx/v0.9.0/python/demos.html).


#### Known issues

Workaround for inability to find gmsh Python package:

    export PYTHONPATH=$SPACK_ENV/.spack-env/view/lib64/:$PYTHONPATH

Workaround for inability to find adios2 Python package:

    export PYTHONPATH=$(find $SPACK_ENV/.spack-env -type d -name 'site-packages' | grep venv):$PYTHONPATH

<!-- if any other known issues need to be added -->


### Building FEniCS With EasyBuild




## Additional information
FEniCS provides the [technical documentation](https://fenicsproject.org/documentation/),
and also it provides lots of [communication channel](https://fenicsproject.org/community/)
for support and development.

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
