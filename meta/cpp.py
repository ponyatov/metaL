from meta import *
from IO import *

class Cpp(File): pass

cpp = Cpp(f'src/{MODULE}.cpp') / \
    f'#include "{MODULE}.hpp"' / ''

hpp = (Cpp(f'inc/{MODULE}.hpp') / '#pragma once')

class group(G):
    def __init__(self, name, doc=None):
        super().__init__(
            f'/// @defgroup {name} {name}', r'/// @}', pfx='')
        self.doc = doc
        if doc: self / f'/// @brief {doc}'
        self / '/// @{'

libc = group('libc'); hpp / libc
for i in ['stdio', 'stdlib', 'assert']: libc / f'#include <{i}.h>'

(libc / (group('main')
         / S(r'extern int main(int argc, char *argv[]);', pfx='\n/// @brief POSIX entry point')
         / S(r'extern void arg(int argc, char *argv);', pfx='\n/// @brief print command line argument')))

main = S('int main(int argc, char *argv[]) {', '}'); cpp / main
main / 'arg(0, argv[0]);'
(main
 / (S(r'for (int i = 1; i < argc; i++) {  //', '}')
    / 'arg(i, argv[i]);'))

arg = S(r'void arg(int argc, char *argv) {  //', '}', pfx=''); cpp / arg
arg / r'fprintf(stderr, "argv[%i] = <%s>\n", argc, argv);'

from Class import *

core = group('core', doc='executable object graph'); hpp / core
gc = group('gc', doc='garbage collection'); core / gc
obj = Class('Object', doc='executable object graph root class'); core / obj
obj / (G('/// @{', '/// @}', pfx='/// @ingroup gc')
       / r'size_t ref;           ///< reference counter'
       / r'static Object *pool;  ///< flobal object pool'
       / r"Object *prev;         ///< global @ref Object's linked list"
       )

primg = group('prim', doc='primitive/machine elements'); core / primg
prim = Class('Primitive', [obj], primg.doc); primg / prim
intt = Class('Int', [prim], 'integer') / 'int value;'; primg / intt
hex = Class('Hex', [intt], 'hexadecimal'); primg / hex
oct = Class('Oct', [intt], 'octal'); primg / oct
bin = Class('Bin', [intt], 'binary'); primg / bin
num = Class('Num', [prim], 'floating point') / 'float value;'; primg / num

cpp.sync()
hpp.sync()

from presets import *
from cmake import *
