from IO import *
from S import *

def c_cpp_properties():
    json = JSON('c_cpp_properties.json')

    return json

(Dir('.vscode') / c_cpp_properties()).sync()
