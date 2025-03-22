import os
import sys

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

    def __init__(self, value):
        # scalar value
        self.value = value
        # nested elements (object subtree)
        self.nest = []

    def __getitem__(self, idx):
        assert isinstance(idx, int)
        return self.nest[idx]

    ## `<T:`
    def tag(self):
        return self.__class__.__name__.lower()

    ## `:V>`
    def val(self):
        return f'{self.value}'

    ## `<T:V>` header
    def head(self, prefix=''):
        return f'{prefix}<{self.tag()}:{self.val()}>'

    ## @ref dump tree padding
    def pad(self, depth):
        return '\n' + ' ' * 4 * depth

    ## full text tree dump
    def dump(self, depth=0, prefix=''):
        ret = self.pad(depth) + self.head(prefix)
        for i in self.nest:
            ret += i.dump(depth + 1)
        return ret

    def __repr__(self): return self.dump()

    def wrap(self, o):
        match o:
            case o if isinstance(o, Object): return o
            case o if isinstance(o, str): return S(o)
            case _: raise TypeError(type(o), o)

    def __truediv__(self, o):
        self.nest.append(self.wrap(o))
        return self


# source code block
class S(Object):
    # @param[in] pfx prefix line
    # @paramp[in] sfx suffix line
    def __init__(self, value=None, pfx=None, sfx=None):
        super().__init__(value)
        self.pfx = pfx
        self.sfx = sfx

    # generate code
    def gen(self, depth=0):
        ret = ''
        if self.pfx is not None:
            ret += f'{self.pad(depth)}{self.pfx}'
        if self.value is not None:
            ret += f'{self.pad(depth)}{self.val()}'
        for i in self.nest:
            ret += i.gen(depth + 1)
        if self.sfx is not None:
            ret += f'{self.pad(depth)}{self.sfx}'
        return ret


class IO(Object):
    def __init__(self, path):
        self.path = path
        super().__init__(path)

    def val(self): return self.path


class Dir(IO):
    def sync(self):
        try:
            os.mkdir(self.path)
        except FileExistsError:
            pass
        for i in self.nest:
            i.sync()

    def __truediv__(self, o):
        assert isinstance(o, File)
        o.path = f'{self.path}/{o.path}'
        self.nest.append(o)
        return self


class File(IO):
    def sync(self):
        with open(self.path, 'w') as f:
            for i in self.nest:
                print(i.gen(), file=f)


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
    json / (S(None, '{', '}')
            / r'// editor'
            / r'"files.eol": "\n",'
            / r'"files.insertFinalNewline": true,'
            / r'"files.trimFinalNewlines": true,'
            / r'"editor.tabSize": 4,'
            / r'"editor.insertSpaces": true,'
            / r'"editor.detectIndentation": false,'
            / r'"editor.rulers": [80],'
            / r'"editor.lineNumbers": "on",'
            / r'"workbench.tree.indent": 24,'
            / r'"editor.fontSize": 14,'
            / r'"explorer.autoReveal": false,'
            / r'"git.enabled": false,'
            / r'"terminal.integrated.copyOnSelection": true,' / '')
    (json[0]
     / r'// Python'
     / r'"python.defaultInterpreterPath":  "python3",'
     / r'"autopep8.path"                : ["autopep8"],'
     / r'"autopep8.args"                : ["--ignore","E26,E302,E305,E401,E402,E701,E702"],'
     / r'"python.analysis.extraPaths"   : ["${workspaceFolder}/lib"],'
     / r'"[python]": {'
     / r'    "editor.defaultFormatter"  : "ms-python.autopep8",'
     / r'    "editor.formatOnSave"      :  false'
     / r'},')

    return json


extensions = JSON('extensions.json')

def tasks():
    json = JSON('tasks.json')
    json / (S(None, '{', '}')
            / r'"version": "2.0.0",'
            / (S(None, '"tasks": [', ']')
               / (S(None, '{', '}')
                  / r'"label"          : "python: run",'
                  / r'"type"           : "shell",'
                  / r'"command"        : "python3 ${file}",'
                  / r'"problemMatcher" : [],'
                  / r'"presentation"   : {"showReuseMessage": false, "focus": false, "reveal": "silent"},'
                  / r'"group"          : {"kind": "build","isDefault": true}')))
    return json

launch = JSON('launch.json')
c_cpp_properties = JSON('c_cpp_properties.json')

(Dir('.vscode')
 / settings()
 / extensions
 / tasks()
 / launch
 / c_cpp_properties).sync()
