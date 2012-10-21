import os, nose, shutil
from gloo.interactive import create_project, load_project


def test_small_structure():
    path = 'tmp'

    create_project(path)
    os.chdir('..')

    readlist = os.listdir(path)
    testlist = ['data', 'lib', 'munge', 'README.txt', '.config.json']

    assert sorted(readlist) == sorted(testlist)
    
    shutil.rmtree(path)

def test_full_structure():
    path = 'tmp'

    create_project(path, full_structure=True)
    os.chdir('..')

    readlist = os.listdir(path)
    testlist = ['.config.json', 'data', 'diagnostics', 'doc', \
                'graphs', 'lib', 'munge', 'profiling', 'README.txt', \
                'reports', 'tests']

    assert sorted(readlist) == sorted(testlist)
    
    shutil.rmtree(path)

def test_git():
    path = 'tmp'

    create_project(path, git=True)
    os.chdir('..')

    assert '.git' in os.listdir(path)

    shutil.rmtree(path)
