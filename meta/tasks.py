from IO import JSON
from S import *

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
