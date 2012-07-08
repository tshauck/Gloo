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

    from os import mkdir, chdir, system
    from json import dump
    mkdir(project_name)
    chdir(project_name)

    config = {}

    config['git'] = keywords.get('git', False)
    config['full_structure'] = keywords.get('full_structure', False)
    config['packages'] = keywords.get('package', [])
    config['logging'] = keywords.get('logging', False)

    if config['full_structure']:
        folders = ['data', 'diagnostics', 'doc', 'graphs', \
                    'lib', 'reports', 'profiling', 'tests', 'munge']
    else:
        folders = ['data', 'lib', 'munge']

    map(mkdir, folders)

    system('touch README.txt')
    if config['git']:
        system('git init --quiet')

    with open('.config.json', mode='w') as f:
        dump(config, f)
