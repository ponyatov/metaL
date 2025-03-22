from meta import *
from IO import *

for d in DIRS:
    (Dir(d) / (File('.gitignore') / '!.gitignore')).sync()
