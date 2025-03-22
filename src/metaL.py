import os

MODULE = 'metaL'
TITLE = '[meta]programming Language/Layer'
SUBTITLE = 'software prototyping system'

AUTHOR = 'Dmitry Ponyatov'
EMAIL = 'dponyatov@gmail.com'
YEAR = '2022'
LICENSE = 'MIT'
GITHUB = f'https://github.com/ponyatov/{MODULE}'


def readme():
    with open('README.md', 'w') as f:
        print(f'''#  `{MODULE}`
##  {TITLE}
### {SUBTITLE}

(c) {AUTHOR} <<{EMAIL}>> {YEAR} {LICENSE}

github: {GITHUB}''', file=f)


readme()

DIRS = ['.vscode', 'bin', 'doc', 'lib', 'inc', 'src', 'tmp', 'ref']

def dirs():
    for d in DIRS:
        try:
            os.mkdir(d)
        except FileExistsError:
            pass


dirs()

## executable object graph item
class Object:
    def tag(self):
        return self.__class__.__name__.lower()

    def val(self):
        return ''

    def head(self, prefix=''):
        return f'{prefix}<{self.tag()}:{self.val()}>'

    def pad(self, depth):
        return '\n' + ' ' * 4 * depth

    def dump(self, depth=0, prefix=''):
        ret = self.pad(depth) + self.head(prefix)
        for i in self.nest:
            ret += i.dump(depth + 1)
        return ret

    def __repr__(self): return self.dump()

    # nested elements (object subtree)
    nest = []

    def __truediv__(self, o):
        assert isinstance(o, Object)
        self.nest.append(o)
        return self

## source code block
class S(Object):
    ## @param[in] pfx prefix line
    ## @paramp[in] sfx suffix line
    def __init__(self, pfx=None, sfx=None):
        self.pfx = pfx
        self.sfx = sfx


class IO(Object):
    def __init__(self, path):
        self.path = path

    def val(self): return self.path

    def __truediv__(self, o):
        assert isinstance(o, IO)
        o.path = f'{self.path}/{o.path}'
        self.nest.append(o)
        return self


class Dir(IO):
    def sync(self):
        try:
            os.mkdir(self.path)
        except FileExistsError:
            pass
        for i in self.nest:
            i.sync()


class File(IO):
    def sync(self):
        with open(self.path, 'w') as f:
            pass

    def __truediv__(self, o):
        assert isinstance(o, S)
        self.nest.append(o)
        return self


class Cpp(File):
    pass


cpp = Cpp(f'src/{MODULE}.cpp')
hpp = Cpp(f'inc/{MODULE}.hpp')

cpp.sync()
hpp.sync()


class JSON(File):
    pass


def settings():
    json = JSON('settings.json')
    json / S('{', '}')
    return json


extensions = JSON('extensions.json')
tasks = JSON('tasks.json')
launch = JSON('launch.json')
c_cpp_properties = JSON('c_cpp_properties.json')

print(Dir('.vscode') / settings())
# (Dir('.vscode') / settings()).sync()
#  / extensions
#  / tasks
#  / launch
#  / c_cpp_properties).sync()
