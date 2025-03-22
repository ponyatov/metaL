from IO import *

hw = Dir('hw')
hw / (File('.gitignore') / '!.gitignore')

inc = Dir('inc'); hw / inc; inc / File('hw.hpp')
src = Dir('src'); hw / src; src / File('hw.cpp')

hw.sync()
