import pickle
import os
import pandas


class Gloo():

    def __init__(self, project_name="My Project", vcs=None,
                 full_structure=None, packages=None, logging=None):

        self.project_name = project_name
        self.config_file = ".gloo"
        self.config = self._load_config()

        override_config = lambda x, y: x if x else y
        self.vcs = override_config(vcs, self.config['vcs'])
        self.full_structure = \
                override_config(full_structure, self.config['full_structure'])
        self.packages = override_config(packages, self.config['packages'])
        self.logging = override_config(logging, self.config['logging'])

    def _load_config(self):
        try:
            if os.path.basename(os.getcwd()) == self.project_name:
                cf = file(self.config_file, 'r')
            else:
                cf = file(os.path.join(self.project_name,
                                       self.config_file), 'r')

            cnfg_dict = pickle.load(cf)
            cf.close()

            return cnfg_dict

        except IOError:
            #If nothing exists return default config
            return {
                    'vcs': None,
                    'full_structure': None,
                    'packages': None,
                    'logging': None
                   }

    def _write_to_config(self):
        config = {
                    'project_name': self.project_name,
                    'vcs': self.vcs,
                    'full_structure': self.full_structure,
                    'packages': self.packages,
                    'logging': self.logging
                 }

        with open(self.config_file, mode='w') as f:
            pickle.dump(config, f)

    def _create_folders(self):

        os.mkdir(self.project_name)
        os.chdir(self.project_name)

        if self.full_structure:
            folders = ['data', 'diagnostics', 'doc', 'graphs',
                        'lib', 'reports', 'profiling', 'tests', 'munge']
        else:
            folders = ['data', 'lib', 'munge']

        map(os.mkdir, folders)

    def _init_vcs(self):
        supported_vcs = ['git', 'bzr']
        if self.vcs:
            if isinstance(self.vcs, list):
                for vcs in self.vcs:
                    if vcs in supported_vcs:
                        os.system('%s init --quiet' % vcs)
                    else:
                        raise NameError('vcs %s is not supported' % vcs)
            elif isinstance(self.vcs, str):
                if self.vcs in supported_vcs:
                    os.system('%s init --quiet' % self.vcs)
                else:
                    raise NameError('vcs %s is not supported' % self.vcs)
            else:
                raise TypeError('Only lists or stings are supported')

    def create_project(self):
        """
        Creates the project and cd's into it
        """
        self._create_folders()
        self._write_to_config()
        self._init_vcs()

    def load_project(self):
        """
        Loads the project into the workspace

        Does four things currently
          1. Recursively loads you csv files into data frames
             prepending the folder if not in data
          2. Runs files in the munge folder.  These are
             preprocessing scripts
          3. Imports files in lib
          4. Starts Logging

        """

        shell = get_ipython()

        with open('.gloo', 'r') as f:
            config = pickle.load(f)

        filename = lambda x: x.split('.')[0]

        #Push variables namespace
        vars_to_push = {}
        for directory, _, datafiles in os.walk('data', topdown=False):
            for datafile in datafiles:
                if directory == 'data':
                    var_name = filename(datafile)
                    read_location = os.path.join('data', datafile)
                    vars_to_push[var_name] = pandas.read_csv(read_location)
                else:
                    var_name = os.path.split(directory)[-1] + '_' \
                            + filename(datafile)
                    read_location = os.path.join(directory, datafile)
                    vars_to_push[var_name] = pandas.read_csv(read_location)
        shell.push(vars_to_push)

        #Run munge file
        mungefiles = os.listdir('munge')
        for mungefile in mungefiles:
            shell.magic('run -i munge/%s' % mungefile)

        #import lib files
        libfiles = os.listdir('lib')
        libs_to_push = {}
        os.chdir('lib')
        for libfile in libfiles:
            mod = filename(libfile)
            libs_to_push[mod] = __import__(filename(libfile))
        shell.push(libs_to_push)
        os.chdir('..')

        #Import packages
        if self.packages:
            packages = self.packages
            for package in packages:
                if isinstance(package, str):
                    shell.runcode('import %s' % package)
                elif isinstance(package, tuple):
                    package_name, alias = package
                    shell.runcode('import %s as %s' % (package_name, alias))

        if config['logging']:
            shell.magic_logstart(os.getcwd().split('/')[-1]
              + '_logging.py append')

    def save_project(self):
        self._write_to_config()
