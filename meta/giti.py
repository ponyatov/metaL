from meta import *
from IO import *

(File('.gitignore')
 / r'*~'
 / r'*.swp'
 / r'*.log'
 / r'__pycache__'
 / r'!.gitignore'
 ).sync()

for d in DIRS:
    if d in ['bin', 'tmp', 'ref']:
        giti = (File('.gitignore') / '*' / '!.gitignore')
    elif d == 'doc':
        giti = (File('.gitignore') / 'html' / '!.gitignore')
    else:
        giti = (File('.gitignore') / '!.gitignore')
    (Dir(d) / giti).sync()
