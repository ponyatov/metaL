from meta import *
from IO import *

class Cpp(File): pass

cpp = Cpp(f'src/{MODULE}.cpp') / \
    f'#include "{MODULE}.hpp"' / '' / 'int main(){}'
hpp = Cpp(f'inc/{MODULE}.hpp') / '#pragma once'

cpp.sync()
hpp.sync()


from presets import *
from cmake import *
