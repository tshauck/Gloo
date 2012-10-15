def create_project(project_name = 'DataProject', **keywords):
    """
    Creates the project and creates a skelton directory
    structure

    Params:
      project_name: A string that represents the name of the project

      keywords:
        git: create a git repo? type bool, default false
        full_structure: create a full strucutre? type bool, default false
        packages: define a list of packages to always load, type list, default empty
        logging: automatically start logging. type bool, default false
    """

    import os
    from json import dump

    os.mkdir(project_name)
    os.chdir(project_name)

    #Set up config
    config = {}

    config['git'] = keywords.get('git', False)
    config['full_structure'] = keywords.get('full_structure', False)
    config['packages'] = keywords.get('package', [])
    config['logging'] = keywords.get('logging', False)
    config['name'] = project_name


    #Create folder strucutre
    if config['full_structure']:
        folders = ['data', 'diagnostics', 'doc', 'graphs', \
                    'lib', 'reports', 'profiling', 'tests', 'munge']
    else:
        folders = ['data', 'lib', 'munge']

    map(os.mkdir, folders)

    #Create files
    os.system('touch README.txt')

    #Create git repo
    if config['git']:
        os.system('git init --quiet')

    #Dump into config file
    with open('.config.json', mode='w') as f:
        dump(config, f)
