import os
import sys

from meta import *

def readme():
    with open('README.md', 'w') as f:
        print(f'''#  `{MODULE}`
##  {TITLE}
### {SUBTITLE}

(c) {AUTHOR} <<{EMAIL}>> {YEAR} {LICENSE}

github: {GITHUB}''', file=f)


readme()



def dirs():
    for d in DIRS:
        try:
            os.mkdir(d)
        except FileExistsError:
            pass


dirs()

# executable object graph item

from Object import *
from S import *
from IO import *


class Cpp(File):
    pass


cpp = Cpp(f'src/{MODULE}.cpp')
hpp = Cpp(f'inc/{MODULE}.hpp')

cpp.sync()
hpp.sync()


from vscode import *


extensions = JSON('extensions.json')

def tasks():
    json = JSON('tasks.json')
    json / (S(None, '{', '}')
            / r'"version": "2.0.0",'
            / (S(None, '"tasks": [', ']')
               / (S(None, '{', '}')
                  / r'"label"          : "python: run",'
                  / r'"type"           : "shell",'
                  / r'"command"        : "python3 ${file}",'
                  / r'"problemMatcher" : [],'
                  / r'"presentation"   : {"showReuseMessage": false, "focus": false, "reveal": "silent"},'
                  / r'"group"          : {"kind": "build","isDefault": true}')))
    return json

launch = JSON('launch.json')
c_cpp_properties = JSON('c_cpp_properties.json')

(Dir('.vscode')
 / settings()
 / extensions
 / tasks()
 / launch
 / c_cpp_properties).sync()

(File('.gitignore')
 / r'*~'
 / r'*.swp'
 / r'*.log'
 / r'__pycache__'
 / r'!.gitignore'
 ).sync()

from giti import *
