from IO import *
from S import *

class JSON(File):
    pass


def settings():
    json = JSON('settings.json')
    json / S(None, '{', '}')
    (json[0]
     / r'// files'
     / (S(None, '"files.exclude": {', '},')
        / r'"**/__pycache__": true,') / ''
     )
    (json[0]
     / r'// editor'
     / r'"files.eol": "\n",'
     / r'"files.insertFinalNewline": true,'
     / r'"files.trimFinalNewlines": true,'
     / r'"editor.tabSize": 4,'
     / r'"editor.insertSpaces": true,'
     / r'"editor.detectIndentation": false,'
     / r'"editor.rulers": [80],'
     / r'"editor.lineNumbers": "on",'
     / r'"workbench.tree.indent": 24,'
     / r'"editor.fontSize": 14,'
     / r'"explorer.autoReveal": false,'
     / r'"git.enabled": false,'
     / r'"terminal.integrated.copyOnSelection": true,' / '')
    (json[0]
     / r'// Python'
     / r'"python.defaultInterpreterPath":  "python3",'
     / r'"autopep8.path"                : ["autopep8"],'
     / r'"autopep8.args"                : ["--ignore","E26,E302,E305,E401,E402,E701,E702"],'
     / r'"python.analysis.extraPaths"   : ["${workspaceFolder}/lib"],'
     / r'"[python]": {'
     / r'    "editor.defaultFormatter"  : "ms-python.autopep8",'
     / r'    "editor.formatOnSave"      :  false'
     / r'},')

    return json

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
