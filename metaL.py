import os, sys


class Object:

    def __init__(self, V):
        self.value = V
        self.slot = {}
        self.nest = []

    def box(self, that):
        if isinstance(that, Object): return that
        if isinstance(that, str): return S(that)
        raise TypeError(['box', type(that), that])

    def __repr__(self):
        return self.dump()

    def __format__(self, spec):
        return self.val()

    def dump(self, cycle=[], depth=0, prefix=''):
        # head
        def pad(depth): return '\n' + '\t' * depth
        ret = pad(depth) + self.head(prefix)
        # cycle
        if not depth: cycle = []
        if self in cycle: return f'{ret} _/'
        else: cycle.append(self)
        # slot{}s
        for i in self.keys():
            ret += self[i].dump(cycle, depth + 1, prefix=f'{i} = ')
        # nest[]ed
        for j, k in enumerate(self):
            ret += k.dump(cycle, depth + 1, prefix=f'{j}: ')
        # subtree
        return ret

    def head(self, prefix=''):
        gid = f' @{id(self):x}'
        return f'{prefix}<{self.tag()}:{self.val()}>{gid}'

    def tag(self):
        return self.__class__.__name__.lower()

    def val(self):
        return f'{self.value}'

    def keys(self):
        return sorted(self.slot.keys())

    def __iter__(self):
        return iter(self.nest)

    def __floordiv__(self, that):
        self.nest.append(self.box(that)); return self

    def ins(self, idx, that):
        self.nest.insert(idx, self.box(that))

class Primitive(Object):
    pass

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

class Container(Object):
    pass

class Map(Container):
    pass

class Vector(Container):
    pass

class Stack(Container):
    pass

class Queue(Container):
    pass

class Active(Object):
    pass

class VM(Active):
    pass

class Op(Active):
    pass

class Fn(Active):
    def __init__(self, V, args=[], pfx=''):
        super().__init__(V)
        self.args = args; self.pfx = pfx

    def gen(self, to, depth=0):
        return to.fn(self, depth).gen(to, depth)

class Meta(Object):
    pass

class Class(Meta):
    def __init__(self, C, sup=[], pfx=''):
        assert callable(C)
        super().__init__(C.__name__)
        self.sup = sup; self.pfx = pfx

    def gen(self, to, depth=0):
        return to.clazz(self, depth).gen(to, depth)


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
        self.vscode.extensions = jsonFile('extensions')
        self.vscode // self.vscode.extensions
        self.extensions = \
            (S('"recommendations": [', ']')
             // '"ryuta46.multi-command",'
             // '"stkb.rewrap",'
             // '"tabnine.tabnine-vscode",'
             // '// "auchenberg.vscode-browser-preview",'
             // '// "ms-vscode-remote.remote-ssh",'
             // '// "ms-azuretools.vscode-docker",'
             )
        self.vscode.extensions // (S('{', '}') // self.extensions)
        # //
        # // "ms-vscode.cpptools",
        # "vsciot-vscode.vscode-arduino",

    def tasks(self):
        self.tasks = jsonFile('tasks'); self.vscode // self.tasks

        def task(group, task): return \
            (S('{', '},')
             // f'"label":          "{group}: {task}",'
             // f'"type":           "shell",'
             // f'"command":        "make {task}",'
             // f'"problemMatcher": []')

        self.tasks \
            // (S('{', '}')
                // '"version": "2.0.0",'
                // (S('"tasks": [', ']')
                // task('project', 'install')
                // task('project', 'update')
                // task('git', 'dev')
                // task('git', 'shadow')
                    ))

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
        self.readme = mdFile('README'); self.d // self.readme
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
            (S('install: $(OS)_install gz', pfx='.PHONY: install update')
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
        self.mk.gz_ = Sec('gz', pfx=''); self.mk.install_ // self.mk.gz_
        self.mk.gz = S('gz:', pfx='.PHONY: gz'); self.mk.gz_ // self.mk.gz
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

class Makefile(File):
    def __init__(self, V='Makefile', ext='', tab='\t'):
        super().__init__(V, ext, tab=tab)

class mdFile(File):
    def __init__(self, V, ext='.md'):
        super().__init__(V, ext)

class jsonFile(File):
    def __init__(self, V, ext='.json', comment='//'):
        super().__init__(V, ext, comment=comment)

class pyFile(File):
    def __init__(self, V, ext='.py'):
        super().__init__(V, ext)
        self.imports = (Sec(sfx='')); self.top // self.imports

    def clazz(self, clazz, depth):
        sup = list(map(lambda i: i.__name__, clazz.sup))
        sup = '(%s)' % ', '.join(sup) if sup else ''
        ret = S(f'class {clazz}{sup}:', pfx=clazz.pfx)
        for i in clazz: ret // i
        return ret

    def fn(self, fn, depth):
        args = ', '.join(fn.args)
        ret = S(f'def {fn}({args}):', pfx=fn.pfx)
        if not fn.nest: ret // 'pass'
        for i in fn: ret // i
        return ret

class Mod(Meta):
    def __init__(self, V=None):
        if not V: V = self.tag()
        super().__init__(V)

    def pipe(self, p):
        p.mod += [self.__class__]
        self.dirs(p)
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

    def dirs(self, p): pass
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

    def reqs(self, p):
        p.reqs = File('requirements', '.txt'); p.d // p.reqs

    def settings(self, p):
        mask = '"**/__pycache__/**":true,'
        p.settings.exclude // mask; p.settings.watcher // mask

    def extensions(self, p):
        p.extensions // '"tht13.python",'

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
        p.metal.imports // 'import os, sys'
        p.metal.object = Class(Object)
        #
        p.metal.init = (Fn('__init__', ['self', 'V'])
                        // 'self.value = V'
                        // 'self.slot = {}'
                        // 'self.nest = []')
        #
        p.metal.box_ = (Fn('box', ['self', 'that'])
                        // "if isinstance(that, Object): return that"
                        // "if isinstance(that, str): return S(that)"
                        // "raise TypeError(['box', type(that), that])"
                        )
        #
        p.metal.dump_ = \
            (Fn('dump', ['self', 'cycle=[]', 'depth=0', "prefix=''"])
             // '# head'
                // "def pad(depth): return '\\n' + '\\t' * depth"
                // "ret = pad(depth) + self.head(prefix)"
             // '# cycle'
                // r"if not depth: cycle = []"
                // r"if self in cycle: return f'{ret} _/'"
                // r"else: cycle.append(self)"
             // '# slot{}s'
                // (S('for i in self.keys():')
                    // r"ret += self[i].dump(cycle, depth + 1, prefix=f'{i} = ')")
             // '# nest[]ed'
             // (S('for j, k in enumerate(self):')
                 // r"ret += k.dump(cycle, depth + 1, prefix=f'{j}: ')")
             // '# subtree'
                // 'return ret'
             )
        p.metal.head_ = \
            (Fn('head', ['self', "prefix=''"])
             // r"gid = f' @{id(self):x}'"
             // r"return f'{prefix}<{self.tag()}:{self.val()}>{gid}'"
             )
        #
        (p.metal.object
            // (Sec()
                // p.metal.init
                // p.metal.box_
                )
            // (Sec()
                // (Fn('__repr__', ['self']) // 'return self.dump()')
                // (Fn('__format__', ['self', 'spec']) // 'return self.val()')
                // p.metal.dump_
                // p.metal.head_
                // (Fn('tag', ['self'])
                    // "return self.__class__.__name__.lower()")
                // (Fn('val', ['self'])
                    // "return f'{self.value}'")
                )
            // (Sec()
                // (Fn('keys', ['self'])
                    // r"return sorted(self.slot.keys())")
                // (Fn('__iter__', ['self'])
                    // r"return iter(self.nest)")
                // (Fn('__floordiv__', ['self', 'that'])
                    // r"self.nest.append(self.box(that)); return self")
                // (Fn('ins', ['self', 'idx', 'that'])
                    // r"self.nest.insert(idx, self.box(that))")
                )
         )
        p.metal // p.metal.object
        #
        p.metal // Class(Primitive, [Object])
        #
        p.metal.s = (Class(S, [Primitive])
                     // Fn('__init__', ['self', 'V=None', 'end=None', 'pfx=None', 'sfx=None'])
                     // Fn('gen', ['self', 'to', 'depth=0']))
        p.metal // p.metal.s
        #
        p.metal.sec = (Class(Sec, [S])
                       // Fn('gen', ['self', 'to', 'depth=0'])
                       )
        p.metal // p.metal.sec
        #
        p.metal // Class(Container, [Object])
        p.metal // Class(Map, [Container])
        p.metal // Class(Vector, [Container])
        p.metal // Class(Stack, [Container])
        p.metal // Class(Queue, [Container])
        #
        p.metal // Class(Active, [Object])
        p.metal // (Class(VM, [Active]))
        p.metal // (Class(Op, [Active]))
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
        p.metal // (Class(mdFile, [File]))
        p.metal // (Class(jsonFile, [File])
                    // Fn('__init', ['self']))
        p.metal // (Class(pyFile, [File])
                    // Fn('__init', ['self']))
        #
        p.metal // Class(Mod, [Meta])
        p.metal // Class(Py, [Mod])
        p.metal // Class(metaL, [Mod])

class htmlFile(File):
    def __init__(self, V, ext='.html'):
        super().__init__(V, ext)

class cssFile(File):
    def __init__(self, V, ext='.css'):
        super().__init__(V, ext)

class jsFile(File):
    def __init__(self, V, ext='.js'):
        super().__init__(V, ext)

class HTML(S):
    def __init__(self, V):
        super().__init__(f'<{V}>', f'</{V}>')

class Flask(Mod):
    def src(self, p):
        self.py(p)
        self.reqs(p)

    def dirs(self, p):
        self.static(p)
        self.templates(p)

    def mk(self, p):
        p.mk.gz_ \
            // S('CDNJS = https://cdnjs.cloudflare.com/ajax/libs', pfx='')
        p.mk.version \
            // 'JQUERY_VER = 3.6.0'
        p.mk.gz.value += ' static/jquery.js'
        p.mk.gz_ \
            // (S('static/jquery.js:', pfx='')
                // '$(CURL) $@ $(CDNJS)/jquery/$(JQUERY_VER)/jquery.min.js')

    def static(self, p):
        p.static = Dir('static'); p.d // p.static
        #
        self.css(p)
        self.js(p)

    def js(self, p):
        p.js = jsFile('js'); p.static // p.js

    def css(self, p):
        p.css = cssFile('css'); p.static // p.css
        (p.css
            // (S('body {', '}')
                // 'background: #222;'
                // 'border: 1pt solid yellow;'
                ))

    def templates(self, p):
        p.templates = Dir('templates'); p.d // p.templates
        #
        self.index(p)
        self.all(p)

    def index(self, p):
        p.index = htmlFile('index'); p.templates // p.index
        p.index // "{% extends 'all.html' %}"

    def block(self, name):
        return f'{{% block {name} %}}{{% endblock %}}'

    def all(self, p):
        p.all = htmlFile('all'); p.templates // p.all
        p.all // '<!DOCTYPE html>'
        #
        p.all.head = \
            (HTML('head')
             // '<link rel="stylesheet" href="/static/css.css">'
             // '<script src="/static/jquery.js"></script>'
             // self.block('head')
             )
        #
        p.all.body = HTML('body') // self.block('body')
        #
        p.all.script = \
            S('<script src="/static/js.js"></script>') \
            // self.block('script')
        #
        p.all // (HTML('html') // p.all.head // p.all.body // p.all.script)

    def reqs(self, p):
        p.reqs // 'Flask'

    def py(self, p):
        p.py.imports // 'import flask'
        #
        p.py.index = \
            (Fn('index', pfx="\n@app.route('/')")
                // "return flask.render_template('index.html')")
        #
        p.py.favicon = \
            (Fn('favicon', pfx="\n@app.route('/favicon.ico')")
                // "return flask.send_from_directory('doc', 'logo.png')")
        #
        p.py // (Sec()
                 // "app = flask.Flask(__name__)"
                 // p.py.index
                 // p.py.favicon
                 // '' // "app.run(debug=True)")
