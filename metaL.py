import os, sys

class Object:
    def __init__(self, V):
        self.value = V
        self.nest = []

    def box(self, that):
        if isinstance(that, Object): return that
        if isinstance(that, str): return S(that)
        raise TypeError(['box', type(that), that])

    def __repr__(self):
        return self.dump()

    def __format__(self, spec):
        return self.val()

    def tag(self): return self.__class__.__name__.lower()
    def val(self): return f'{self.value}'

    def __floordiv__(self, that):
        self.nest.append(self.box(that)); return self

    def __iter__(self): return iter(self.nest)

    def ins(self, idx, that):
        assert isinstance(idx, int)
        self.nest.insert(idx, self.box(that))

class Primitive(Object): pass

class S(Primitive):
    def __init__(self, V=None, end=None, pfx=None, sfx=None):
        super().__init__(V)
        self.end = end; self.pfx = pfx; self.sfx = sfx

    def gen(self, to, depth=0):
        assert isinstance(to, File)
        ret = ''
        if self.pfx is not None:
            ret += f'{to.tab*depth}{self.pfx}\n' if self.pfx else '\n'
        if self.value is not None:
            ret += f'{to.tab*depth}{self}\n'
        for i in self:
            ret += i.gen(to, depth + 1)
        if self.end is not None:
            ret += f'{to.tab*depth}{self.end}\n'
        if self.sfx is not None:
            ret += f'{to.tab*depth}{self.sfx}\n' if self.sfx else '\n'
        return ret

class Sec(S):
    def gen(self, to, depth=0):
        ret = ''
        if self.nest:
            if self.pfx is not None:
                ret += f'{to.tab*depth}{self.pfx}\n' if self.pfx else '\n'
            if self.value is not None:
                ret += f'{to.tab*depth}{to.comment} \\ {self}\n'
            for i in self:
                ret += i.gen(to, depth + 0)
            if self.value is not None:
                ret += f'{to.tab*depth}{to.comment} / {self}\n'
            if self.sfx is not None:
                ret += f'{to.tab*depth}{self.sfx}\n' if self.sfx else '\n'
        return ret

class Container(Object): pass

class Active(Object): pass

class Fn(Active):
    def __init__(self, V, args=[]):
        super().__init__(V)
        self.args = args

    def gen(self, to, depth=0):
        ret = to.fn(self, depth)
        for i in self: ret // i.gen(to, depth + 1)
        return ret.gen(to, depth)

class Meta(Object): pass

class Class(Meta):
    def __init__(self, C, sup=[]):
        assert callable(C)
        super().__init__(C.__name__)
        self.sup = sup

    def gen(self, to, depth=0):
        ret = to.clazz(self, depth)
        for i in self: ret // i.gen(to, depth + 1)
        return ret.gen(to, depth)


class Project(Meta):
    def __init__(self, V=None):
        if not V: V = os.getcwd().split('/')[-1]
        super().__init__(V)
        self.mod = []
        self.dirs()
        self.metainfo()
        self.mk()
        self.apt()
        self.giti()
        self.cf()

    def cf(self):
        self.cf = File('', '.clang-format'); self.d // self.cf
        self.cf // '''
# https://clang.llvm.org/docs/ClangFormatStyleOptions.html

BasedOnStyle: Google
IndentWidth: 4
ColumnLimit: 80

SortIncludes: false

AllowShortBlocksOnASingleLine: Always
AllowShortFunctionsOnASingleLine: All

Language: Cpp'''

    def giti(self):
        self.giti = giti(); self.d // self.giti
        self.giti // (Sec(sfx='') // '*~' // '*.swp' // '*.log')
        self.giti // (Sec(sfx='') // f'/docs/' // f'/{self}/')

    def metainfo(self):
        self.TITLE = f'{self}'
        self.AUTHOR = 'Dmitry Ponyatov'
        self.EMAIL = 'dponyatov@gmail.com'
        self.YEAR = 2020
        self.LICENSE = 'All rights reserved'
        self.GITHUB = 'https://github.com/ponyatov'

    def apt(self):
        self.apt = File('apt', '.txt'); self.d // self.apt
        self.apt // 'git make curl' // 'code meld doxygen' // 'python3 python3-pip python3-venv'

    def __or__(self, that):
        return that.pipe(self)

    def sync(self):
        self.readme()
        self.d.sync()

    def dirs(self):
        self.d = Dir(f'{self}')
        #
        self.vscode()
        self.bin()
        self.doc()
        self.lib()
        self.src()
        self.tmp()

    def vscode(self):
        self.vscode = Dir('.vscode'); self.d // self.vscode
        self.settings()
        self.extensions()
        self.tasks()

    def settings(self):
        self.settings = jsonFile('settings'); self.vscode // self.settings

        def multi(key, cmd): return \
            (S('{', '},')
                // f'"command": "multiCommand.{key}",'
                // (S('"sequence": [')
                    // '"workbench.action.files.saveAll",'
                    // '{"command": "workbench.action.terminal.sendSequence",'
                    // f'    "args": {{"text": "\\u000D clear ; LANG=C {cmd} \\u000D"}}}}]'
                    ))
        #
        self.settings.exclude = (S('"files.exclude": {', '},')
                                 // f'"**/{self}/**":true,')
        self.settings.watcher = (S('"files.watcherExclude": {', '},'))
        for i in ['docs']:
            mask = f'"**/{i}/**":true,'
            self.settings.exclude // mask; self.settings.watcher // mask
        self.settings.assoc = (S('"files.associations": {', '},'))
        files = (Sec('files', pfx='')
                 // self.settings.exclude
                 // self.settings.watcher
                 // self.settings.assoc)
        #
        editor = (Sec('editor', pfx='')
                  // '"editor.tabSize": 4,'
                  // '"editor.rulers": [80],'
                  // '"workbench.tree.indent": 32,')
        self.settings // (S('{', '}')
                          // (S('"multiCommand.commands": [', '],')
                              // multi('f11', 'make meta')
                              // multi('f12', 'make all ')
                              )
                          // files
                          // editor)

    def extensions(self):
        self.extensions = jsonFile('extensions')
        self.vscode // self.extensions

    def tasks(self):
        self.tasks = jsonFile('tasks'); self.vscode // self.tasks

    def bin(self):
        self.bin = Dir('bin'); self.d // self.bin
        self.bin.giti = giti(); self.bin // (self.bin.giti // '*')

    def doc(self):
        self.doc = Dir('doc'); self.d // self.doc
        self.doc.giti = giti(); self.doc // (self.doc.giti // '*.pdf' // '*.djvu')

    def lib(self):
        self.lib = Dir('lib'); self.d // self.lib
        self.lib.giti = giti(); self.lib // self.lib.giti

    def src(self):
        self.src = Dir('src'); self.d // self.src
        self.src.giti = giti(); self.src // (self.src.giti // '*-*/')

    def tmp(self):
        self.tmp = Dir('tmp'); self.d // self.tmp
        self.tmp.giti = giti(); self.tmp // (self.tmp.giti // '*')

    def readme(self):
        self.readme = File('README.md'); self.d // self.readme
        (self.readme
            // '![logo](doc/logo.png)'
            // f'#  {self}'
            // f'## {self.TITLE}'
            // ''
            // f'(c) {self.AUTHOR} <<{self.EMAIL}>> {self.YEAR} {self.LICENSE}'
            // ''
            // f'github: {self.GITHUB}/{self}/')

    def mk(self):
        self.mk = Makefile(); self.d // self.mk
        #
        self.mk.var = Sec('var'); self.mk // self.mk.var
        (self.mk.var
         // 'MODULE  = $(notdir $(CURDIR))'
         // 'OS      = $(shell uname -o|tr / _)'
         // 'NOW     = $(shell date +%d%m%y)'
         // 'REL     = $(shell git rev-parse --short=4 HEAD)'
         // 'BRANCH  = $(shell git rev-parse --abbrev-ref HEAD)'
         // 'PEPS    = E26,E302,E305,E401,E402,E701,E702')
        #
        self.mk.version = Sec('version', pfx=''); self.mk // self.mk.version
        #
        self.mk.dir = Sec('dir', pfx=''); self.mk // self.mk.dir
        #
        self.mk.tool = Sec('tool', pfx=''); self.mk // self.mk.tool
        (self.mk.tool
         // 'CURL    = curl -L -o'
         // 'CF      = clang-format-11 -style=file -i'
         // 'PY      = $(shell which python3)'
         // 'PIP     = $(shell which pip3)'
         // 'PEP     = $(shell which autopep8) --ignore=$(PEPS) --in-place')
        #
        self.mk.src = Sec('src', pfx=''); self.mk // self.mk.src
        (self.mk.src
         // 'Y += $(MODULE).py'
         // 'S += $(Y)')
        #
        self.mk.cfg = Sec('cfg', pfx=''); self.mk // self.mk.cfg
        #
        self.mk.all = Sec('all', pfx=''); self.mk // self.mk.all
        (self.mk.all
         // (S('all: $(PY) $(MODULE).py')
             // '$^' // '$(MAKE) tmp/format_py'))
        #
        self.mk.format = Sec('format', pfx=''); self.mk // self.mk.format
        (self.mk.format
         // (S('tmp/format_py: $(Y)')
             // '$(PEP) $? && touch $@'))
        #
        self.mk.rule = Sec('rule', pfx=''); self.mk // self.mk.rule
        #
        self.mk.doc = Sec('doc', pfx=''); self.mk // self.mk.doc
        #
        self.mk.install_ = Sec('install', pfx=''); self.mk // self.mk.install_
        self.mk.install = \
            (S('install: $(OS)_install', pfx='.PHONY: install update')
             // '$(MAKE) update')
        self.mk.update = \
            (S('update: $(OS)_update', pfx=''))
        self.mk.install_ // self.mk.install // self.mk.update
        self.mk.install_ \
            // (S('GNU_Linux_install GNU_Linux_update:',
                pfx='\n.PHONY: GNU_Linux_install GNU_Linux_update')
                // 'sudo apt update'
                // 'sudo apt install -u `cat apt.txt`')
        #
        self.mk.merge = Sec('merge', pfx=''); self.mk // self.mk.merge
        (self.mk.merge
            // 'MERGE  = Makefile README.md .gitignore apt.txt .clang-format $(S)'
            // 'MERGE += .vscode bin doc lib src tmp'
            // ''
            // '.PHONY: dev shadow release zip')
        self.mk.merge \
            // (S('dev:', pfx='')
                // 'git push -v'
                // 'git checkout $@'
                // 'git pull -v'
                // 'git checkout shadow -- $(MERGE)')
        self.mk.merge \
            // (S('shadow:', pfx='')
                // 'git push -v'
                // 'git checkout $@'
                // 'git pull -v')
        self.mk.merge \
            // (S('zip:', pfx='\nZIP = tmp/$(MODULE)_$(BRANCH)_$(NOW)_$(REL).src.zip')
                // 'git archive --format zip --output $(ZIP) HEAD'
                // '$(MAKE) doxy ; zip -r $(ZIP) docs')


class IO(Object):
    def __init__(self, V):
        super().__init__(V)
        self.path = V

class Dir(IO):
    def __floordiv__(self, that):
        that.path = f'{self.path}/{that.path}'
        return super().__floordiv__(that)

    def sync(self):
        try: os.mkdir(self.path)
        except FileExistsError: pass
        for i in self: i.sync()

class File(IO):
    def __init__(self, V, ext='', tab=' ' * 4, comment='#'):
        super().__init__(V + ext)
        self.tab = tab; self.comment = comment
        self.top = Sec()
        self.bot = Sec()

    def sync(self):
        with open(self.path, 'w') as F:
            F.write(self.top.gen(self))
            for i in self: F.write(i.gen(self))
            F.write(self.bot.gen(self))

class giti(File):
    def __init__(self, V='', ext='.gitignore'):
        super().__init__(V, ext)
        self.bot // '!.gitignore'

class jsonFile(File):
    def __init__(self, V, ext='.json', comment='//'):
        super().__init__(V, ext, comment=comment)

class pyFile(File):
    def __init__(self, V, ext='.py'):
        super().__init__(V, ext)

    def clazz(self, clazz, depth):
        sup = list(map(lambda i: i.__name__, clazz.sup))
        sup = '(%s)' % ', '.join(sup) if sup else ''
        pazz = ' pass' if not clazz.nest else ''
        ret = S(f'class {clazz}{sup}:{pazz}', pfx='')
        return ret

    def fn(self, fn, depth):
        args = ', '.join(fn.args)
        ret = S(f'def {fn}({args}):')
        return ret

class Makefile(File):
    def __init__(self, V='Makefile', ext='', tab='\t'):
        super().__init__(V, ext, tab=tab)

class Mod(Meta):
    def __init__(self, V=None):
        if not V: V = self.tag()
        super().__init__(V)

    def pipe(self, p):
        p.mod += [self.__class__]
        self.mk(p)
        self.apt(p)
        self.giti(p)
        self.src(p)
        self.vscode(p)
        return p

    def vscode(self, p):
        self.settings(p)
        self.extensions(p)
        self.tasks(p)

    def settings(self, p): pass
    def extensions(self, p): pass
    def tasks(self, p): pass

    def mk(self, p): pass
    def apt(self, p): pass
    def giti(self, p): pass
    def src(self, p): pass

class Py(Mod):

    def mk(self, p):
        p.mk.update // '$(PIP) install --user -U pip autopep8 pytest'
        p.mk.merge.ins(2, 'MERGE += requirements.txt')

    def giti(self, p):
        p.giti // (Sec(sfx='') // '/__pycache__/')

    def src(self, p):
        self.py(p)
        self.reqs(p)

    def py(self, p):
        p.py = pyFile(f'{p}'); p.d // p.py
        p.py.imports = (Sec(sfx='')); p.py // p.py.imports

    def reqs(self, p):
        p.reqs = File('requirements', '.txt'); p.d // p.reqs

    def settings(self, p):
        mask = '"**/__pycache__/**":true,'
        p.settings.exclude // mask; p.settings.watcher // mask

class metaL(Mod):

    def mk(self, p):
        p.mk.src.ins(1, 'Y += $(MODULE).meta.py metaL.py')
        #
        p.mk.all // (S('meta: $(PY) $(MODULE).meta.py', pfx='')
                     // '$^'
                     // '$(MAKE) tmp/format_py')

    def meta(self, p):
        p.meta = pyFile(f'{p}.meta'); p.d // p.meta
        mods = ''.join(map(lambda i: f' | {i.__name__}()', p.mod))
        (p.meta
         // f"from metaL import *"
         // f"p = Project()"
         // f"p.TITLE = '{p.TITLE}'"
         // f"p{mods}"
         // f"p.sync()")

    def src(self, p):
        assert Py in p.mod
        self.meta(p)
        self.metal(p)

    def metal(self, p):
        p.metal = pyFile(f'metaL'); p.d // p.metal
        #
        p.py.imports // 'import os, sys'
        p.py.object = Class(Object)
        (p.py.object
            // (Sec()
                // Fn('__init__', ['self', 'V'])
                // Fn('box', ['self', 'that'])
                )
            // (Sec()
                // Fn('__repr__', ['self'])
                // Fn('__format__', ['self', 'spec'])
                )

         )
        p.metal // p.py.object
        #
        p.metal // Class(Primitive, [Object])
        #
        p.py.s = (Class(S, [Primitive])
                  // Fn('__init__', ['self', 'V=None', 'end=None', 'pfx=None', 'sfx=None'])
                  // Fn('gen', ['self', 'to', 'depth=0']))
        p.metal // p.py.s
        #
        p.py.sec = (Class(Sec, [S])
                    // Fn('gen', ['self', 'to', 'depth=0'])
                    )
        p.metal // p.py.sec
        #
        p.metal // Class(Container, [Object])
        #
        p.metal // Class(Active, [Object])
        p.metal // (Class(Fn, [Active])
                    // Fn('__init__', ['self', 'V', 'args=[]'])
                    // Fn('gen', ['self', 'to', 'depth=0'])
                    )
        #
        p.metal // Class(Meta, [Object])
        p.metal // (Class(Class, [Meta])
                    // Fn('__init__', ['self', 'C', 'sup=[]']))
        p.metal // Class(Project, [Meta])
        #
        p.metal // (Class(IO, [Object])
                    // Fn('__init__', ['self', 'V', 'ext', "tab=' '*4", "comment='#'"])
                    )
        p.metal // (Class(Dir, [IO])
                    // Fn('sync', ['self']))
        p.metal // (Class(File, [IO])
                    // Fn('sync', ['self']))
        p.metal // (Class(giti, [File])
                    // Fn('__init', ['self']))
        p.metal // (Class(Makefile, [File])
                    // Fn('__init', ['self', "V='Makefile'", "ext=''", "tab='\\t'"]))
        p.metal // (Class(jsonFile, [File])
                    // Fn('__init', ['self']))
        p.metal // (Class(pyFile, [File])
                    // Fn('__init', ['self']))
        #
        p.metal // Class(Mod, [Meta])
        p.metal // Class(Py, [Mod])
        p.metal // Class(metaL, [Mod])
