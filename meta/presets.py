from IO import *

preset = JSON('CMakePresets.json')

class B(S):
    def __init__(self, name):
        super().__init__('{', '}')
        (self
            / f'"name"            :  "{name}",'
            / f'"configurePreset" :  "{name}",'
            / f'"targets"         : ["all","install"]'
         )

class C(S):
    def __init__(self, name, inherits=None):
        super().__init__('{', '},')
        self / f'"name"            : "{name}",'
        if inherits: self / f'"inherits"        : "{inherits}",'

class H(C):
    def __init__(self, name, inherits=None):
        super().__init__(name, inherits)
        self / '"hidden"          :  true,'

build = S('"buildPresets": [', '],') / B('linux')

common = (H('common')
          / '"binaryDir"       : "${sourceDir}/tmp/${presetName}",'
            / '"generator"       : "Unix Makefiles",'
            / (S('"cacheVariables"  : {', '}')
                / '"CMAKE_INSTALL_PREFIX"    : "${sourceDir}/bin",'
                / '"CMAKE_MODULE_PATH"       : "${sourceDir}/cmake",'
                / '"CMAKE_COLOR_DIAGNOSTICS" :  false,'
                / '"CMAKE_BUILD_TYPE"        : "Debug",'
                / '"CMAKE_VERBOSE_MAKEFILE"  :  false'
               ))

pc = (H('pc', inherits='common')
      / '"cacheVariables"  : {"HW":"pc", "CPU":"i5", "ARCH":"x86_64"}')

linux = (C('linux', inherits='pc')
         / r'"toolchainFile"   : "${sourceDir}/cmake/x86_64-linux-gnu.cmake",'
         / r'"cacheVariables"  : {"OS":"linux"}')
linux.end = '}'

configure = S('"configurePresets": [', ']') / common / pc / linux

preset / (S('{', '}') / '"version": 6,' / build / configure)

preset.sync()
