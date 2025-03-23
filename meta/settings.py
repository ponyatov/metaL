from IO import *
from S import *

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
     / r'// JS'
     / r'"prettier.requireConfig"      :  true,'
     / r'"prettier.configPath"         : ".prettierrc",'
     / r'"json.format.enable"          :  true,' / '')

    (json[0]
     / r'// clang-format'
     / r'"clang-format.executable"     : "clang-format",'
     / r'"clang-format.fallbackStyle"  : "Google",'
     / r'"clang-format.style"          : "file",' / '')

    (json[0]
     / r'// C++'
     / r'"[c]": {'
     / r'    "editor.defaultFormatter" : "xaver.clang-format",'
     / r'    "editor.formatOnSave"     :  false'
     / r'},'
     / r'"[cpp]": {'
     / r'    "editor.defaultFormatter" : "xaver.clang-format",'
     / r'    "editor.formatOnSave"     :  false'
     / r'},'
     / r'// "C_Cpp.intelliSenseEngine": "Tag Parser",'
     / r'// "C_Cpp.default.configurationProvider": "ms-vscode.cmake-tools",'
     / '')

    (json[0]
     / r'// CMake'
     / r'"cmake.sourceDirectory" : "${workspaceFolder}",'
     / r'"cmake.buildDirectory"  : "${workspaceFolder}/tmp/${workspaceFolderBasename}",'
     / r'"cmake.generator"       : "Unix Makefiles",'
     / r'"cmake.parallelJobs"    :  4,'
     / r'"cmake.useCMakePresets" : "always",'
     / r'"cmake.buildBeforeRun"  :  true,'
     / r'"cmake.saveBeforeBuild" :  true,'
     / r'"cmake.debugConfig"     : {'
     / r'    "cwd" :   "${workspaceFolder}",'
     / r'    "args": [ "lib/${workspaceFolderBasename}.ini" ] },'
     / r'"cmake.allowCommentsInPresetsFile" : true,'
     / r'"cmake.ignoreCMakeListsMissing"    : true,'
     / '')

    (json[0]
     / r'// Python'
     / r'"python.defaultInterpreterPath":  "python3",'
     / r'"autopep8.path"                : ["autopep8"],'
     / r'"autopep8.args"                : ["--ignore","E26,E302,E305,E401,E402,E701,E702"],'
     / r'"python.analysis.extraPaths"   : ["${workspaceFolder}/meta"],'
     / r'"[python]": {'
     / r'    "editor.defaultFormatter"  : "ms-python.autopep8",'
     / r'    "editor.formatOnSave"      :  false'
     / r'},')

    return json

(Dir('.vscode') / settings()).sync()
