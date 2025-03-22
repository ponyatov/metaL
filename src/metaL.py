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

# executable object graph item


class Object:
    def tag(self): return self.__class__.__name__.lower()
    def val(self): return ''
    def head(self): return f'<{self.tag()}:{self.val()}>'
    def __repr__(self): return self.head()

    # nested elements (object subtree)
    nest = []

    def __truediv__(self, o):
        assert isinstance(o, Object)
        self.nest.append(o)
        return self


class IO(Object):
    def __init__(self, path):
        self.path = path

    def val(self): return self.path

    def __truediv__(self, o):
        assert isinstance(o, IO)
        o.path = f'{self.path}/{o.path}'
        return super().__truediv__(o)


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


class Cpp(File):
    pass


cpp = Cpp(f'src/{MODULE}.cpp')
hpp = Cpp(f'inc/{MODULE}.hpp')

cpp.sync()
hpp.sync()


class JSON(File):
    pass


settings = JSON('settings.json')
extensions = JSON('extensions.json')
tasks = JSON('tasks.json')
launch = JSON('launch.json')
c_cpp_properties = JSON('c_cpp_properties.json')

(Dir('.vscode') / settings
 / extensions
 / tasks
 / launch
 / c_cpp_properties).sync()
