from IO import *
from S import *


from settings import *


def extensions():
    json = JSON('extensions.json')
    json / (S(None, '{', '}')
            / (S(None, '"recommendations": [', ']')
               / r'"stkb.rewrap",'
               / r'"ryuta46.multi-command",'
               / r'"tabnine.tabnine-vscode",'
               / r'"ms-vscode.makefile-tools",'
               / r'"IBM.output-colorizer",'
            #
               / r'// Linux'
               / r'"ms-vscode-remote.remote-ssh",'
               / r'"coolbear.systemd-unit-file",'
               #
               / r'// formatters'
               / r'"xaver.clang-format",'
               / r'"foxundermoon.shell-format",'
               / r'"esbenp.prettier-vscode",'
               #
               / r'// misc'
               / r'"usernamehw.errorlens",'
               #
               / r'// Web'
               / r'"esbenp.prettier-vscode",'
               / r'"mechatroner.rainbow-csv",'
               #
               / r'// C++'
               / r'"ms-vscode.cpptools",'
               / r'"jeff-hykin.better-cpp-syntax",'
               / r'"ms-vscode.cmake-tools",'
               / r'"twxs.cmake",'
               #
               / r'// parser'
               / r'"daohong-emilio.yash",'
               / r'"rreverser.ragel",'
               #
               / r'// embedded'
               / r'"dan-c-underwood.arm",'
               / r'"zixuanwang.linkerscript",'
               / r'"ms-vscode.vscode-serial-monitor",'
               / r'// "espressif.esp-idf-extension",'
               #
               / r'// Python'
               / r'"ms-python.python",'
               / r'"ms-python.autopep8",'

               ))
    return json

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
 / extensions()
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
