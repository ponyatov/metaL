from meta import *
from IO import *

class Cpp(File): pass

cpp = Cpp(f'src/{MODULE}.cpp')
hpp = Cpp(f'inc/{MODULE}.hpp')

cpp.sync()
hpp.sync()


from presets import *
from cmake import *
