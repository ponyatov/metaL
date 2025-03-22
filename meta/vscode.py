from IO import *
from S import *


from settings import *
from extensions import *
from tasks import *


launch = JSON('launch.json')
c_cpp_properties = JSON('c_cpp_properties.json')

(Dir('.vscode')
 / settings()
 / extensions()
 / tasks()
 / launch
 / c_cpp_properties).sync()
