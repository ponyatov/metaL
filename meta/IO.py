import os
from Object import *

class IO(Object):
    def __init__(self, path):
        self.path = path
        super().__init__(path)

class Dir(IO):
    def sync(self):
        try: os.mkdir(self.path)
        except FileExistsError: pass
        for i in self.nest: i.sync()

    def __truediv__(self, o):
        assert isinstance(o, File)
        o.path = f'{self.path}/{o.path}'
        self.nest.append(o)
        return self


class File(IO):
    def sync(self):
        with open(self.path, 'w') as f:
            for i in self.nest:
                f.write(i.gen())

class JSON(File):
    pass
