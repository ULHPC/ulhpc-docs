[![](https://fenicsproject.org/pub/tutorial/sphinx1/_static/fenics_banner.png){: style="width:200px;float: right;" }](https://fenicsproject.org/)

<!-- Intro start -->

[FEniCS](https://fenicsproject.org/) is a popular open-source computing platform for solving partial differential equations (PDEs) using the finite element method ([FEM](https://en.wikipedia.org/wiki/Finite_element_method)). Originally developed in 2003, the earlier version is now known as legacy FEniCS. In 2020, the next-generation framework [FEniCSx](https://docs.fenicsproject.org/) was introduced, with the latest stable [release v0.9.0](https://fenicsproject.org/blog/v0.9.0/) in October 2024. Though it builds on the legacy FEniCS but introduces significant improvements over the legacy libraries. FEniCSx is comprised of the libraries [UFL](https://github.com/FEniCS/ufl), [Basix](https://github.com/FEniCS/basix), [FFCx](https://github.com/FEniCS/ffcx), and [DOLFINx](https://github.com/FEniCS/dolfinx) which are the build blocks of it. And new users are encouraged to adopt [FEniCSx](https://docs.fenicsproject.org/) for its modern features and active development support.


<!-- // Tutorials: https://jsdokken.com/dolfinx-tutorial/index.html -->


<!-- Intro end  -->

## Installation of FEniCSx

FEniCSx can be installed on [ULHPC](https://www.uni.lu/research-en/core-facilities/hpc/) systems using [Easybuild](https://docs.easybuild.io) or [Spack](https://spack.io/), Below are detailed instructions for each method, 



### Building FEniCS With Spack


Building FEniCSx with Spack requires that Spack is already installed, configured, and its environment sourced on the [ULHPC] system. If Spack is not yet configured, follow the [spack documentation](../../environment/spack.md) for installation and configuration.  

!!! note 
        Spack can a good choice to  build FEniCSx with its many complex dependencies, leveraging the system-provided packages defined in ~/.spack/packages.yaml for optimal performance. 

Create and Activate a  Spack Environment: 

To maintain an isolated installation, create a dedicated Spack environment in a chosen directory.
The following example builds FEniCSx in the `home` directory:

    cd ~
    spack env create -d fenicsx-main-20230126/
    spack env activate fenicsx-main-20230126/

 
Add the core FEniCSx components and common dependencies:

    spack add py-fenics-dolfinx@0.9.0+petsc4py fenics-dolfinx+adios2+petsc adios2+python petsc+mumps

    # Change @0.9.0 to any version in the above if you want a another version.
    spack concretize
    spack install -j16


!!! note 

        `spack concretize` resolves all dependencies and selects compatible versions for the specified packages. `-j16` sets the number of parallel build jobs. Using a higher number can speed up the build but should be chosen based on available CPU cores and cluster policies.



or the same directly in `spack.yaml` in `$SPACK_ENV`

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
    
The following are also commonly used in FEniCS scripts and may be useful

    spack add gmsh+opencascade py-numba py-scipy py-matplotlib
    
It is possible to build a specific version (git ref) of DOLFINx. 
Note that the hash must be the full hash.
It is best to specify appropriate git refs on all components.

    # This is a Spack Environment file.
    #
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
        
It is also possible to build only the C++ layer using

    spack add fenics-dolfinx@main+adios2 py-fenics-ffcx@main petsc+mumps
    
To rebuild FEniCSx from main branches inside an existing environment

    spack install --overwrite -j16 fenics-basix py-fenics-basix py-fenics-ffcx fenics-ufcx py-fenics-ufl fenics-dolfinx py-fenics-dolfinx

#### Testing the build

Quickly test the build with

    srun python -c "from mpi4py import MPI; import dolfinx"

#### Using the build

See the uni.lu documentation for full details - using the environment should be as 
simple as adding the following where `...` is the name/folder of your environment.

    #!/bin/bash -l
    source $HOME/spack/share/spack/setup-env.sh
    spack env activate ...

#### Known issues

Workaround for inability to find gmsh Python package:

    export PYTHONPATH=$SPACK_ENV/.spack-env/view/lib64/:$PYTHONPATH

Workaround for inability to find adios2 Python package:

    export PYTHONPATH=$(find $SPACK_ENV/.spack-env -type d -name 'site-packages' | grep venv):$PYTHONPATH


### Building FEniCS With EasyBuild


### Example (Poisson.py)
```bash

# Demo possion problem 
# https://docs.fenicsproject.org/dolfinx/main/python/demos/demo_poisson.html

from mpi4py import MPI
from petsc4py.PETSc import ScalarType

import numpy as np

import ufl
from dolfinx import fem, mesh
from dolfinx.fem.petsc import LinearProblem

# Create mesh
msh = mesh.create_rectangle(
    comm=MPI.COMM_WORLD,
    points=((0.0, 0.0), (2.0, 1.0)),
    n=(32, 16),
    cell_type=mesh.CellType.triangle,
)

# Function space
V = fem.functionspace(msh, ("Lagrange", 1))

# Boundary facets (x=0 and x=2)
facets = mesh.locate_entities_boundary(
    msh,
    dim=(msh.topology.dim - 1),
    marker=lambda x: np.isclose(x[0], 0.0) | np.isclose(x[0], 2.0),
)
dofs = fem.locate_dofs_topological(V=V, entity_dim=1, entities=facets)

# Dirichlet BC u = 0
bc = fem.dirichletbc(value=ScalarType(0), dofs=dofs, V=V)

# Variational problem
u = ufl.TrialFunction(V)
v = ufl.TestFunction(V)
x = ufl.SpatialCoordinate(msh)
f = 10 * ufl.exp(-((x[0] - 0.5) ** 2 + (x[1] - 0.5) ** 2) / 0.02)
g = ufl.sin(5 * x[0])
a = ufl.inner(ufl.grad(u), ufl.grad(v)) * ufl.dx
L = ufl.inner(f, v) * ufl.dx + ufl.inner(g, v) * ufl.ds

# Create problem (no petsc_options_prefix in 0.9.0)
problem = LinearProblem(
    a,
    L,
    bcs=[bc],
    petsc_options={"ksp_type": "preonly", "pc_type": "lu", "ksp_error_if_not_converged": True},
)

# Solve
uh = problem.solve()

# Only print from rank 0 to avoid MPI spam
if MPI.COMM_WORLD.rank == 0:
    print("First 10 values of the solution vector:", uh.x.array[:10])

assert isinstance(uh, fem.Function)


```

## Additional information
FEniCS provides the [technical documentation](https://fenicsproject.org/documentation/),
and also it provides lots of [communication channel](https://fenicsproject.org/community/)
for support and development.

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
