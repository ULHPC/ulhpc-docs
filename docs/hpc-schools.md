# On-site HPC trainings and tutorials

We propose periodical on-site events for our users. They are free of charge and can be attended by anyone from the University of Luxembourg faculties and interdisciplinary centers. 
Additionally, we also accept users from LIST, LISER and LIH. If you are part of another public research center, please [contact us](mailto:hpc-school-for-beginners@uni.lu).


## Forthcoming events

- [HPC school for beginners](#hpc-school-for-beginners): **eligible for ECTS credits**  
Quaterly, dates to be announced, Belval Campus
- [Introduction to Machine Learning](#introduction-to-hpc-and-machine-learning):
Dates to be announced, Belval Campus
- [Python for HPC](#python-hpc-school):
Dates to be announced, Belval Campus


## HPC School for beginners

This event aims to equip you with essential skills and knowledge to embark on your High-Performance Computing journey. The event is organized each trimester and is composed of six half days.

Limited spots available per session (usually 30 max).

### Upcoming sessions

No dates annouced at the moment. Future sessions will be announced here, please wait for announcements or contact the HPC team via [email](mailto:hpc-school-for-beginners@uni.lu) to express your interest.

<!---
- Date: September 2025, 11th-12th
- Time: 9am to 12pm (both days).
- Location: 2.380, MSA - Belval Campus.
-->

### Prerequisites

- No specific knowledge required
- Bring your own computer (Linux, MacOS and Windows are welcome)
- An active HPC account. You can request one [here](/accounts/#how-to-get-a-new-user-account).

### Session 1 - Accessing the Cluster and Command Line Introduction 

Learn how to:

- access the HPC cluster and set up your machine
- use the command line interface effectively (manage your files, run software, ...). Gain confidence in interacting with the cluster environment.
- tranfer data to and from the cluster

### Session 2 - HPC Basics: Job Submission and Monitoring

Learn:

- the inner workings of the university HPC clusters 
- how to submit and manage computational tasks. 
- how to monitor and optimize job performance.

### Session 3 - Reproducibility: Working with software environments and containers

Learn how to:

- setup isolated software environments
- create and use containers in the HPC systems
- Improve the reproducibility of your workflows by creating reproducible setups.

### Session 4 - Using resources efficiently

- Understand the allocation of resources in HPC systems
- Optimise your job submission workflow
- Configure you code to access cores, memory channels, and GPUs efficiently and prevent over-subscription.

### Session 5 - Optimising storage access

Learn about:

- the different storage tiers and their characteristics
- Using parallel file systems effectively
- Optimising storage access patterns

### Session 6 - TBA


### Resources

- Setup
    - [Request an account](resources/HPC_School_-_Beginner_S1-1_-_Account_request.pdf)
    - [Access the HPC - Linux and Mac](resources/HPC_School_-_Beginner_S1-1_-_Mac_and_Linux.pdf)
    - [Access the HPC - Windows](resources/HPC_School_-_Beginner_S1-1_-_Windows.pdf)
- Basic shell and cluster skills
    - [Introduction to the shell](resources/HPC_School_-_Beginner_S1-2.pdf)
    - [Introduction to the job scheduler](resources/HPC_School_-_Beginner_S2.pdf)
- [CLI Cheat Sheet](resources/CLI_Cheat_Sheet.pdf)


## Machine Learning for beginners

This two-days course introduces participants to Machine Learning (ML) and Deep Learning (DL) on HPC. During the course, we will cover the fundamentals of ML and DL, work through practical exercises on model training, and explore how to speed up computations using HPC resources, distributed computing, and GPU acceleration. The course combines theory, coding exercises, and HPC applications to give participants both a solid foundation and practical skills.

Limited spots available per session (20 max).

### Upcoming sessions


No sessions are planned at the moment. Future sessions will be announced here, please wait for announcements or contact the HPC team via [email](mailto:hpc-school-for-beginners@uni.lu) to express your interest.

<!--
- Date: 4th and 5th of June 2025
- Time: 9am to 5pm (both days)
- Location: MNO 1.040 and 1.050, Belval Campus
-->
### Training outcomes

By the end of the course, participants will:

- Understand key ML and DL concepts and techniques;
- Gain hands-on experience with data preprocessing, model training, and evaluation;
- Learn how to use HPC resources for accelerated ML workloads;
- Explore distributed computing and GPU acceleration tools;

### Course structure

#### Day 1 - ML Foundations

<!--_Location:_ MNO 1.050, Belval Campus-->

- Introduction to ML - AI & ML, types of ML, key concepts;
- Exploratory Data Analysis (EDA) in Jupyter Notebook - Loading, preprocessing, and visualizing;
- Supervised Learning - Regression vs. Classification, model evaluation, hands-on exercises;
- Introduction to Neural Networks.

#### Day 2 - DL & HPC Acceleration

<!--_Location:_ MNO 1.040, Belval Campus-->

- DL & CNNs - Building and training DL models;
- Distributed computing on HPC;
- Accelerated ML & DL.

### Requirements

- Having an HPC account to access the cluster.
- Basic knowledge on SLURM (beginners HPC school).
- A basic understanding of Python programming.
- Familiarity with Jupyter Notebook (installed and configured).
- A basic understanding of Numpy and linear algebra.


## Python HPC School

In this workshop, we will explore the process of improving Python code for efficient execution. Chances are, you 're already familiar with Python and Numpy. However, we will start by mastering profiling and efficient NumPy usage as these are crucial steps before venturing into parallelization. Once your code is fine-tuned with Numpy we will explore the utilization of Python's parallel libraries to unlock the potential of using multiple CPU cores. By the end, you will be well equipped to harness Python's potential for high-performance tasks on the HPC infrastructure. 

### Target Audience Description 
The workshop is designed for individuals who are interested in advancing their skills and knowledge in Python-based scientific and data computing. The ideal participants would typically possess basic to intermediate Python and Numpy skills, along with some familiarity with parallel programming. This workshop will give a good starting point to leverage the usage of the HPC computing power to speed up your Python programs. 

### Upcoming sessions

No sessions are planned at the moment. Future sessions will be announced here, please wait for announcements or contact the HPC team via [email](mailto:hpc-school-for-beginners@uni.lu) to express your interest.

<!--
- Date: March, 2024, 27th and 28th.
- Time: 10h to 12h and 14h to 16h (both days).
- Location: MNO 1.030. - Belval campus
-->

### First day – Jupyter notebook on ULHPC / profiling efficient usage of Numpy

#### Program

- Setting up a Jupyter notebook on an HPC node - 10am to 11am
- Taking time and profiling python code - 11am to 12pm
- Lunch break - 12pm to 2pm
- Numpy basics for replacing python loops for efficient computations - 2pm to 4pm

#### Requirements 

- Having an HPC account to access the cluster. 
- Basic knowledge on SLURM (beginners HPC school). 
- A basic understanding of Python programming. 
- Familiarity with Jupyter Notebook (installed and configured). 
- A basic understanding of Numpy and linear algebra. 

### Second day – Improving performance with python parallel packages 

#### Program

- Use case understanding and Python implementation - 10am to 10:30am
- Numpy implementation - 10:30am to 11am
- Python’s Multiprocessing - 11am to 12pm
- Lunch break - 12pm to 2pm
- PyMP - 2pm to 2:30pm
- Cython - 2:30pm to 3pm
- Numba and final remarks- 3pm to 4pm

#### Requirements

- **Having an HPC account to access the cluster.**
- Basic knowledge on SLURM (beginners HPC school). 
- A basic understanding of Python programming. 
- Familiarity with Jupyter Notebook (installed and configured). 
- A basic understanding of Numpy and linear algebra. 
- Familiarity with parallel programming. 

<!--
## Conda environment management for Python and R

The creation of Conda environments is supported in the University of Luxembourg HPC systems. But when Conda environments are needed and what tools are available to create Conda environments? Attend this tutorial if your projects involve R or Python and you need support with installing packages.

The topics that will be covered include:

- how to install packages using the facilities available in R and Python,
- how to document and exchange environment setups,
- when a Conda environment is required for a project, and
- what tools are available for the creation of Conda environments.

### Upcoming sessions

No sessions are planned at the moment. Future sessions will be announced here, please wait for announcements or contact the HPC team via [email](mailto:hpc-school-for-beginners@uni.lu) to express your interest.
-->

<!--
## Introduction to numerical methods with BLAS

This seminar covers basic principles of numerical library usage with BLAS as an example. The library mechanisms for organizing software are studied in detail, covering topics such as the differences between static and dynamic libraries. The practical sessions will demonstrate the generation of library files from source code, and how programs can use library functions.

After an overview of software libraries, the BLAS library is presented, including the available operations and the organization of the code. The attendees will have the opportunity to use functions of BLAS in a few practical examples. The effects of caches in numerical library performance are then studied in detail. In the practical sessions the attendees will have the opportunity to try cache aware programming techniques that better exploit the performance of the available hardware.

Overall in this seminar you learn how to:

- compile libraries from source code,
- compile and link code that uses numerical libraries,
- understand the effects of caches in numerical library performance, and
- exploit caches to leverage better performance.

### Upcoming sessions

No sessions are planned at the moment. Future sessions will be announced here, please wait for announcements or contact the HPC team via [email](mailto:hpc-school-for-beginners@uni.lu) to express your interest.
-->

<!--
## An overview of HPC systems and applications

This introductory presentation for HPC users with previous computing experience. It's a quite condensed course with minimal practical sections. The topics covered are

- the architecture of HPC systems,
- methods to extract architectural information about nodes,
- advanced scheduler directives such as process pinning and job dependencies,
- software distribution and containerization,
- message passing programming with MPI,
- shared memory programming with OpenMP, and
- optimizing programs execution for specific architectures.

### Upcoming sessions

The course is given only at special events.

### Resources

- [An overview of HPC systems and applications](resources/An_introduction_to_HPC.pdf)
-->
