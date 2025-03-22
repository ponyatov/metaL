from IO import *

hw = Dir('hw')
hw / (File('.gitignore') / '!.gitignore')

inc = Dir('inc'); hw / inc
hw.sync()
