from meta import *
from IO import *

class Cpp(File): pass

cpp = Cpp(f'src/{MODULE}.cpp') / \
    f'#include "{MODULE}.hpp"' / ''

hpp = (Cpp(f'inc/{MODULE}.hpp') / '#pragma once' / '')
for i in ['stdio', 'stdlib', 'assert']: hpp / f'#include <{i}.h>'
(hpp / ''
       / r'extern int main(int argc, char *argv[]);'
       / r'extern void arg(int argc, char *argv);')

main = S('int main(int argc, char *argv[]) {', '}'); cpp / main
main / 'arg(0, argv[0]);'
(main
 / (S(r'for (int i = 1; i < argc; i++) {  //', '}')
    / 'arg(i, argv[i]);'))

arg = S(r'void arg(int argc, char *argv) {  //', '}', pfx=''); cpp / arg
arg / r'fprintf(stderr, "argv[%i] = <%s>\n", argc, argv);'

cpp.sync()
hpp.sync()

from presets import *
from cmake import *
