==============
A Data Project Manager for IPython
==============

Provides utilities and functions for managing data projects in python.  Requires
use of IPython and Pandas.

A quick workflow example::

    from gloo import Gloo

    proj = Gloo('My Project', full_structure, packages=['scipy',
                                              ('numpy', 'np')])

    proj.create_project()

Introduction
============

Gloo's goal is to tie together a lot of the data analysis actions that happen
regularly and make that processes easy.  Automatically loading data into the
ipython environment, running scripts, making utitlity functions available and
more.  These are things that have to be done often, but aren't the fun part.

proj.create_project() Options
---------------------------------------------------------

``project_name``: This is a string that is the name of your project.

Current Config Options:
  ``full_structure``  If True the folder structure outline below.  By default 
  creates smaller project, i.e. False.

  ``packages`` A list of strings of python packages to load when
  ``load_project()`` is called.  Defaults to empty.  If you want to alias your
  package you can pass a tuple to the list.  ``['scipy', ('numpy', 'np')]``
  will import scipy as scipy and numpy as np.

  ``logging`` A boolean to dictate if logging is started when
  ``load_project()`` is called.  Defaults to False.

  ``svn`` Pass a list or a string to init version control.  Currently supports
  git and bzr.  ``svn = ['git', 'bzr']`` will init both.

Those options are saved into a pickled file called .gloo at the root of the
project directory.

What Happens When You Call load_project()
-----------------------------------------

``proj.load_project()``

1.  The config is loaded into a dictionary.
2.  Data is the ``data`` directory is loaded into the environment.  This is done
    recursively so you can have subdirectories.  If you do, the parent folder of
    the data file will be prepended to data file, ``folder_file``.  The plan is
    to make the prepending optional.
3.  Files in the ``munge`` directory are run.  This folder is where you would
    put files necessary for preprocessing the data.
4.  Files in the ``lib`` directory are imported.  This folder is where you would
    put files that you would like to load as a module.  So if you have
    utility.py in the lib directory.  When you load the project you'll have
    utility availble in the namespace.
5.  Packages specified in the config are loaded into the environment.
6.  Logging starts

Folder Structure
----------------
The full structure is as follows::

    data/        : data  
    doc/         : documentation  
    diagnostics/ : automatically check for data issues  
    graphs/      : graph domicile  
    lib/         : utility functions  
    munge/       : preprocessing scripts  
    profiling/   : benchmark performance  
    reports/     : reports you'll produce  
    tests/       : tests

Other things you can do
----------------------
You can update the config.  Say you have ``packages = ['numpy']`` but once
you've worked on the project you realize you need pandas and you want to load
it as pd.  It's easy to update this of the future::

    >   proj.packages
        ['numpy']
    >   proj.packages.append(('pandas', 'pd'))
    >   proj.save_project()

So next time you load the project pandas as pd will be available.

Installing Gloo
===============

* ``pip install Gloo`` is available.
* There is also an ubuntu package available on `LaunchPad
  <https://code.launchpad.net/~pythonxy/+archive/pythonxy-devel>`_
* Gloo currently isn't supported on Windows

Contributing
============
Because this project is in such an early state I would love for anybody and
everybody to help contribute.  I think this could be very valuable for those
working with python for data projets.

Thanks
======
This project is a bit of a rip-off or port (however nice you're feeling) of
`Project Template <http://www.projecttemplate.net>`_, which if
you're using R I would highly recommend.  It's fantastic.
