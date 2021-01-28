# Easybuild

<!--intro-start-->

[![](https://easybuild.readthedocs.io/en/latest/_static/easybuild_logo_alpha.png){:style="width:200px; float: right;"}](https://easybuild.readthedocs.io/)

[EasyBuild](https://docs.easybuild.io/) (EB for short) is a software build and installation framework that allows you to manage (scientific) software on High Performance Computing (HPC) systems in an efficient way.
A large number of scientific software are supported (**$\geq$ [2175 supported software packages](https://docs.easybuild.io/en/latest/version-specific/Supported_software.html)** since the 4.3.2 release) -- see also [What is EasyBuild?](https://docs.easybuild.io/en/latest/Introduction.html).
For several years now, [Easybuild](https://docs.easybuild.io/) is used to [manage the ULHPC User Software Set](../software/swsets.md) and generate automatically the module files available to you on our computational resource in either `prod` (default) or `devel` (early development/testing) environment -- see [ULHPC Toolchains and Software Set Versioning](../environment/modules.md#ulhpc-toolchains-and-software-set-versioning).

This enables users to easily _extend_ the global [Software Set](../software/swsets.md) with their own **local** software
builds, either performed within their [global home
directory](../data/layout.md#global-home-directory-home) or (better) in a shared [project
directory](../data/layout.md) though [Easybuild](../environment/easybuild.md), which generate automatically module files compliant with the [ULHPC module setup](../environment/modules.md).

<!--intro-end-->
