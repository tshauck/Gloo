import gloo
import os

j = gloo.Gloo('new_test', packages=['scipy', ('json', 'j')])
j.create_project()

#os.chdir('test_project')

#j.load_project()
