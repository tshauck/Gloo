def load_project():
    """
    Loads the project into the workspace
    
    Does three things currently
      1. Recursively loads you csv files into data frames
         prepending the folder if not in data
      2. Runs files in the munge folder.  These are
         preprocessing scripts
      3. Imports files in lib
      4. Starts Logging
    
    """
    from os import listdir, chdir, walk, getcwd
    from os.path import join, split
    from pandas import read_csv
    from json import load
    
    shell = get_ipython()

    with open('.config.json', 'r') as f:
        config = load(f)

    filename = lambda x: x.split('.')[0]

    vars_to_push = {}
    for directory, _, datafiles in walk('data', topdown=False):
        for datafile in datafiles:
            if directory == 'data':
                var_name = filename(datafile)
                read_location = join('data', datafile)
                vars_to_push[var_name] = read_csv(read_location)
            else:
                var_name = split(directory)[-1] + '_' + filename(datafile)
                read_location = join(directory, datafile)
                vars_to_push[var_name] = read_csv(read_location)
    shell.push(vars_to_push)

    mungefiles = listdir('munge')
    for mungefile in mungefiles:
        shell.magic('run -i munge/%s' % mungefile)

    libfiles = listdir('lib')
    libs_to_push = {}
    chdir('lib')
    for libfile in libfiles:
        mod = filename(libfile)
        libs_to_push[mod] = __import__(filename(libfile))
    shell.push(libs_to_push)
    chdir('..')

    packages = config['packages']
    for package in packages:
        shell.runcode('import %s' % package)

    if config['logging']:
      shell.magic_logstart(getcwd().split('/')[-1] \
          + '_logging.py append')
