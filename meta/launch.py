from IO import *
from S import *

class debug:
    def __init__(self, name='linux'):
        self.name = name

    def type(self): return self.__class__.__name__

    def gen(self):
        return (S(None, '{', '}')
                / f'"name"         : "{self.name}",'
                / f'"type"         : "{self.type()}",'
                / r'"request"      : "launch",'
                / r'"program"      : "${command:cmake.launchTargetPath}",'
                / r'"preLaunchTask": "CMake: build",'
                / r'"cwd"          : "${workspaceFolder}",'

                )

class cppdbg(debug):
    pass
class cortex(debug):
    def type(self): return 'cortex-debug'

def launch():
    json = JSON('launch.json') / S(None, '{', '}')
    (json[0] / r'"version": "0.2.0",' /
     (S(None, r'"configurations": [', ']')
      / cppdbg('linux').gen()
      ))
    return json

(Dir('.vscode') / launch()).sync()
