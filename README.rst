==============
ProjectManager
==============

Provides utilities and functions for managing data projects in python.  Requires
use of IPython and Pandas.

A quick workflow example::
    
    import projectmanager as pm

    pm.create_project("MyProject")

    #now if we have some some scripts to use and some data in the data folder we
    #can load the project

    pm.load_project()

Introduction
============

ProjectManager's goal is to facilitate quickly loading data into the IPython
environment, help to automate data munging that would need to be done at the
start of a session, load helper functions in, and give you a nice directory.

What Happens When You Call create_project("MyProject")
---------------------------------------------------------

``create_project(project_name = "MyProject", config = {})``

``project_name``: This is a string that is the name of your project.

``config``: This is a dict that takes configuration options.

Current Config Options:
  ``full_structure`` A boolean that if true creates a full folder structure.  If
  True the folder structure outline below.  Defaults to True.
  
  ``packages`` A list of strings of python packages to load when
  ``load_project()`` is called.  Defaults to empty.

  ``logging`` A boolean to dictate if logging is started when
  ``load_project()`` is called.  Defaults to False.

  ``git`` A boolean to dictate if a git repo is init'd.  Defaults to False.

Those options are saved into a json file called .config.json at the root of the
project directory.

What Happens When You Call load_project()
-----------------------------------------

``load_project()``

1.  The config is loaded into a dictionary.
2.  Data is the ``data`` directory is loaded into the environment.  This is done
    recursively so you can have subdirectories.  If you do, the parent folder of
    the data file will be prepended to data file, ``folder_file``.  The plan is
    to make the prepending optional.
3.  Files in the ``munge`` directory are run.  This folder is where you would
    put files necessary for preprocessing the data.
4.  Files in the ``lib`` directory are imported.  This folder is where you would
    put files that you would like to load as a module.
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
