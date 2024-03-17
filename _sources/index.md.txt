<!-- .. Computer Systems and Programming Tools utils documentation primary file, created by
   sphinx-quickstart on Fri Dec 23 10:42:13 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive. -->

#  Computer Systems and Programming Tools courseutils

These are a set of tools for managing tasks and managing the markdown lesson plans. 

````{grid} 3

```{grid-item-card} Progress Reports
:link: progressreport
:link-type: ref

commands to generate progress reports
```

```{grid-item-card} Badge Instructions
:link: makeupbadgeissue
:link-type: ref

how to make a badge issue for a specific date
```

````



## Install 

You can install after cloning to work locally or directly from github. 

### By clone

You can clone first
```
git clone https://github.com/compsys-progtools/courseutils.git
```

and then install 
```
pip install courseutils
```
(possibly `pip3`)

if you clone in order to develop, you may want to install with pip's `-e` option

```
pip install -e courseutils
```

To update, pull and install again. 


### Direct install 

you can also install without cloning first with 

```
pip install git+https://github.com/compsys-progtools/courseutils.git
```

Optionally, you can specify a branch to install, by default it installs main. 

To update in this case, use the same command


## Usage 

The main use is as a CLI, for a list of all commands see the 
[CLI](cli.md) page. 

For use as a python library in component functions, see them in 
[the python library](api.md) page. 


```{toctree}
:caption: Contents
:maxdepth: 2

cli.md
examples/index.md
instructor/index.md
api.md
```

<!-- 
Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search` -->
