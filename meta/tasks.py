from IO import *
from S import *

class T(S):
    def __init__(self, label, cmd):
        super().__init__('{', '}')
        (self
         / f'"label"          : "{label}",'
         / r'"type"           : "shell",'
         / f'"command"        : "{cmd}",'
         / r'"problemMatcher" : [],')

def tasks():
    json = JSON('tasks.json')
    json / (S('{', '}')
            / r'"version": "2.0.0",'
            / (S('"tasks": [', ']')
               / T('doc: doxygen', 'rm -rf doc/html ; doxygen .doxygen')
               / (T('python: run', 'python3 ${file}')
                  / r'"presentation"   : {"showReuseMessage": false, "focus": false, "reveal": "silent"},'
                  / r'"group"          : {"kind": "build","isDefault": true}')))
    return json

(Dir('.vscode') / tasks()).sync()
