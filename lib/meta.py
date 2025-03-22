MODULE = 'metaL'
TITLE = '[meta]programming Language/Layer'
SUBTITLE = 'software prototyping system'

AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
YEAR = '2022'
LICENSE = 'MIT'
GITHUB = f'https://github.com/ponyatov/{MODULE}'

DIRS = ['.vscode', 'bin', 'doc', 'lib', 'inc', 'src', 'tmp', 'ref']

from readme import *

import os

def dirs():
    for d in DIRS:
        try:
            os.mkdir(d)
        except FileExistsError:
            pass

dirs()
