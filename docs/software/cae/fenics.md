[![](https://fenicsproject.org/pub/tutorial/sphinx1/_static/fenics_banner.png){: style="width:200px;float: right;" }](https://fenicsproject.org/)
[FEniCS](https://fenicsproject.org/) is a popular open-source (LGPLv3) computing platform for
solving partial differential equations (PDEs).
FEniCS enables users to quickly translate scientific models
into efficient finite element code. With the high-level
Python and C++ interfaces to FEniCS, it is easy to get started,
but FEniCS offers also powerful capabilities for more
experienced programmers. FEniCS runs on a multitude of
platforms ranging from laptops to high-performance clusters.

## How to access the FEniCS through [Anaconda](https://www.anaconda.com/products/individual)
The following steps provides information about how to installed
on your local path. 
```bash
# From your local computer
$ ssh -X iris-cluster    # OR ssh -Y iris-cluster on Mac

# Reserve the node for interactive computation with grahics view (plots)
$ si --x11 --ntasks-per-node 1 -c 4
# salloc -p interactive --qos debug -C batch --x11 --ntasks-per-node 1 -c 4

# Go to scratch directory 
$ cds

/scratch/users/<login> $ Anaconda3-2020.07-Linux-x86_64.sh
/scratch/users/<login> $ chmod +x Anaconda3-2020.07-Linux-x86_64.sh
/scratch/users/<login> $ ./Anaconda3-2020.07-Linux-x86_64.sh

Do you accept the license terms? [yes|no]
yes
Anaconda3 will now be installed into this location:
/home/users/<login>/anaconda3

  - Press ENTER to confirm the location
  - Press CTRL-C to abort the installation
  - Or specify a different location below

# You can choose your path where you want to install it
[/home/users/<login>/anaconda3] >>> /scratch/users/<login>/Anaconda3

# To activate the anaconda 
/scratch/users/<login> $ source /scratch/users/<login>/Anaconda3/bin/activate

# Install the fenics in anaconda environment 
/scratch/users/<login> $ conda create -n fenicsproject -c conda-forge fenics

# Install matplotlib for the visualization 
/scratch/users/<login> $ conda install -c conda-forge matplotlib 
```
Once you have installed the anaconda, you can always
activate it by calling the `source activate` path where `anaconda`
has been installed. 

## Working example
### Interactive mode
```bash
# From your local computer
$ ssh -X iris-cluster      # or ssh -Y iris-cluster on Mac

# Reserve the node for interactive computation with grahics view (plots)
$ si --ntasks-per-node 1 -c 4 --x11
# salloc -p interactive --qos debug -C batch --x11 --ntasks-per-node 1 -c 4

# Activate anaconda  
$ source /${SCRATCH}/Anaconda3/bin/activate

# activate the fenicsproject
$ conda activate fenicsproject

# execute the Poisson.py example (you can uncomment the plot lines in Poission.py example)
$ python3 Poisson.py
```

### Batch script
```bash
#!/bin/bash -l                                                                                                 
#SBATCH -J FEniCS                                                                                        
#SBATCH -N 1
###SBATCH -A <project name>
###SBATCH --ntasks-per-node=1
#SBATCH -c 1
#SBATCH --time=00:05:00                                                                      
#SBATCH -p batch

echo "== Starting run at $(date)"                                                                                             
echo "== Job ID: ${SLURM_JOBID}"                                                                                            
echo "== Node list: ${SLURM_NODELIST}"                                                                                       
echo "== Submit dir. : ${SLURM_SUBMIT_DIR}"

# activate the anaconda source 
source ${SCRATCH}/Anaconda3/bin/activate

# activate the fenicsproject from anaconda 
conda activate fenicsproject

# execute the poisson.py through python
srun python3 Poisson.py  
```

### Example (Poisson.py)
```bash
# FEniCS tutorial demo program: Poisson equation with Dirichlet conditions.
# Test problem is chosen to give an exact solution at all nodes of the mesh.
#  -Laplace(u) = f    in the unit square
#            u = u_D  on the boundary
#  u_D = 1 + x^2 + 2y^2
#    f = -6

from __future__ import print_function
from fenics import *
import matplotlib.pyplot as plt

# Create mesh and define function space
mesh = UnitSquareMesh(8, 8)
V = FunctionSpace(mesh, 'P', 1)

# Define boundary condition
u_D = Expression('1 + x[0]*x[0] + 2*x[1]*x[1]', degree=2)

def boundary(x, on_boundary):
    return on_boundary

bc = DirichletBC(V, u_D, boundary)

# Define variational problem
u = TrialFunction(V)
v = TestFunction(V)
f = Constant(-6.0)
a = dot(grad(u), grad(v))*dx
L = f*v*dx

# Compute solution
u = Function(V)
solve(a == L, u, bc)

# Plot solution and mesh
#plot(u)
#plot(mesh)

# Save solution to file in VTK format
vtkfile = File('poisson/solution.pvd')
vtkfile << u

# Compute error in L2 norm
error_L2 = errornorm(u_D, u, 'L2')

# Compute maximum error at vertices
vertex_values_u_D = u_D.compute_vertex_values(mesh)
vertex_values_u = u.compute_vertex_values(mesh)
import numpy as np
error_max = np.max(np.abs(vertex_values_u_D - vertex_values_u))

# Print errors
print('error_L2  =', error_L2)
print('error_max =', error_max)

# Hold plot
#plt.show()
```

## Additional information
FEniCS provides the [technical documentation](https://fenicsproject.org/documentation/),
and also it provides lots of [communication channel](https://fenicsproject.org/community/)
for support and development.

!!! tip
    If you find some issues with the instructions above,
    please file a [support ticket](https://hpc.uni.lu/support).
