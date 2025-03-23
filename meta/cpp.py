from meta import *
from IO import *

class Cpp(File): pass

cpp = Cpp(f'src/{MODULE}.cpp') / \
    f'#include "{MODULE}.hpp"' / ''
hpp = Cpp(f'inc/{MODULE}.hpp') / '#pragma once'

main = S('int main() {', '}'); cpp / main

cpp.sync()
hpp.sync()

from presets import *
from cmake import *
