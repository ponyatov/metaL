from IO import *
from S import *

def launch():
    json = JSON('launch.json')

    return json

(Dir('.vscode') / launch()).sync()
