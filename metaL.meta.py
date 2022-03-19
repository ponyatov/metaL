import sys
from metaL import *
try: p = Project(sys.argv[1])
except IndexError: p = Project()
p.TITLE = 'metaprogramming layer over Python'
p | Py() | metaL() | Flask()
p.sync()
