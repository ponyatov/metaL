# Tutorial {#tutorial}

see also <a href=modules.html>modules</a> and 
<a href=index.html>main page</a> (README.md)

***

The `metaL` (meta)programming language was designed as a mix of Lisp and Python,
not of syntax, but to get feels of language abilities.

* *Python* is simple to use and have very friendly syntax
* *Lisp* has a power of self-modification able to change program in runtime, and
  work with program as a data structure
* *Smalltalk* is pure OOP-language works over message passing which is good for
  distributed and parallel systems

`metaL` **targets** not on writing application programs, but **on writing
programs that generate other programs** (into C code which can be compiled and
run on any computer system).

Don't try to write something which must be fast like number crunching or game
engine -- `metaL` just does not work like that, and was not designed to be fast.
It was created for manipulations with program structures, and you can write
extra fast programs in `metaL` if you use it the right way: for source code
generation of your application.

***

### System startup

* online run: https://repl.it/@metaLmasters/metaL
```
Python 3.8.2 (default, Feb 26 2020, 02:56:10)
> bin/python3 -i metaL.py

<vm:metaL> _
```
* local installation on user computer
```sh
~$ git clone -o gh https://github.com/ponyatov/metaL
~$ cd metaL
~/metaL$ make install
```
* interactive with @ref REPL() autorun
```sh
~/metaL$ make metaL/repl
```
* in Python-only mode: press [Ctrl]+[C] to exit into Pyhon interactive console
```
/home/ponyatov/metaL/bin/python3 -i metaL.py

<vm:metaL> #14ee5988 @7f12f298b128
        ABOUT = <string:homoiconic metaprogramming system\n* powered by `metaL`> #0dfa5b4e @7f12f298b5f8

<vm:metaL> Ctrl+C

Traceback (most recent call last):
  File "metaL.py", line 1246, in <module>
    REPL()
  File "metaL.py", line 1228, in REPL
    command = input(vm.head(test=True) + ' ')
KeyboardInterrupt
>>> print('Python')
Python
>>>
```

### `metaL`-script (DDL/DML)

* **only single line syntax** can be used for every command /Python `input()`
  limitation in @ref REPL() /
* can be run in Python mode as string via function @ref metaL()
```py
comment = ' # line comment '
metaL(comment)
#
```
```py
integer = ' -01 # integer '
metaL(integer)
#
# <ast:>
#     <op:-> #f70b8dac @7f131058fe10
#         0: <integer:1> #47696a48 @7f131059d160
#
# <integer:-1> #d85c1811 @7f131058f128
```
* can be interactively executed after @ref REPL() start

Recommended use is running under any IDE can send selected code from a text
editor to running terminal session with active REPL. After all code were tested
in an interactive shell, it can be saved, and system should be restarted for
changes commit.

### Literals

Some set of language elements can be inputted directly in script, which are
called literals. They are numbers, strings, and symbols.

* numbers
```py
number = ' +02.30 # floating point '
metaL(number)
# <number:2.3>
```
```py
integer = ' -01 # integer '
metaL(integer)
# <integer:-1>
```
```py
ihex = ' 0xDeadBeef # hexadecimal '
metaL(ihex)
# <hex:0xdeadbeef>
```
```py
ibin = ' 0b1101 # binary '
metaL(ibin)
# <bin:0b1101>
```

* strings
```py
simple = " 'single line\n\twith escaped chars' "
metaL(simple)
# <string:single line\n\twith escaped chars>
```
Multiline strings can be parsed, but it is not an exception from the
single-lined syntax, as REPL can't correctly input such strings. The only way to
input them is by using `metaL()` in Python mode.
```py
multiline = """ 'multiple lines
\twith escaped chars'
"""
metaL(multiline)
# <string:multiple lines\n\twith escaped chars>
```

* symbols: any none-space char groups
```py
symbol = 'MODULE'
metaL(symbol)
# <module:metaL>
```
The `Symbol` type differs from other literals: most of them evaluate to itself,
but **symbols will do a lookup in current computation context** as a variable
name in other programming languages.
```
<vm:metaL> MODULE

<symbol:MODULE> #8b2b5473 @7f54949d8048

<module:metaL> #d80c934b @7f5494ffab38

<vm:metaL> #14ee5988 @7f5494ffa710
        ABOUT = <string:homoiconic metaprogramming system\n* powered by `metaL`> #0dfa5b4e @7f5494ffabe0
------------------------------------------------------------------
<vm:metaL>
```

### REPL cycle

Read-Eval-Print-Loop runs in three stages after every line in the source code
string were split by new line chars (besides multiline strings):
```py
>>> metaL(' -01 \n +2.30 ')

  <ast:>
    <op:-> #f70b8dac @7f01078ac080
      0: <integer:1> #47696a48 @7f01078ac1d0
    <op:+> #63257116 @7f01078ac320
      0: <number:2.3> #c4287bc0 @7f01078ac400
```
1. pure parsing: every line will be parsed into an AST (Abstract Syntax Tree)
   combined from the `metaL` objects
   ```
      <op:-> #f70b8dac @7f01078ac080
         0: <integer:1> #47696a48 @7f01078ac1d0
   ```
2. evaluation: object graph runs via `.eval()`/`.apply()` methods
   ```
      <integer:-1> #d85c1811 @7f905edd3e10
   ```
3. When you run `metaL` scripts via an interactive shell, every line will be
   printed as parsed-only AST and evaluated object, followed by the current VM
   state.
   ```
      <vm:metaL> #14ee5988 @7fc7328d7828
         ABOUT = <string:homoiconic metaprogramming system\n* powered by `metaL`> #0dfa5b4e @7fc7328d7cf8
         ...
         vm = <vm:metaL> #14ee5988 @7fc7328d7828 _/
   ```

### Variables/Slots

* Any `Symbol` evaluates as the value, stored in a named attribute of the
  *computation context*.
* The default *computation context* resides in the global `<vm:metaL>` object.
* Also, *any object can be treated as computation context* by passing it as a
  parameter for `.eval()`/`.apply()` methods.

The *computation context* here means any object, which holds **bindings**
between *names* and *values*. In mainstream programming languages, such bindings
are called "variable".

In `metaL` the term **variable** is planned to be used in another context
(closer to Prolog language), so we'll call these bindings as **slots** the same
as this `Object.slot` dict field is named.

For people already have some previous programming skills, multiple variable
variants in the `metaL` language can be confusing:
* **slot**: binding between the name and its value was defined as some object
  attribute
  ```py
  vm['x'] = Integer(123) ; vm
  ```
  ```
  <vm:metaL> #531e221d @7f611664f748
      vm = <vm:metaL> #531e221d @7f611664f748 _/
      x = <integer:123> #b5dc8722 @7f6115ec40b8
  ```
* **variable**: represents source code variables in target programming languages
* **unifying variable**: /planned/ Prolog-like variable works with backtracking
  inference/pattern matching

### `metaL` ingrained complexity: metaprogramming impact

As you can see above, even at such a basis point as variables `metaL` has more
complexity than mainstream languages especially such easy as Python. It can be
understood from the idea and nature of the `metaL` as it strictly targets on the
**metaprogramming**: *programs that write other programs*. When we speak about
some language such as Python: we are going to write some code, which solves your
single application tasks. In contrast, programming in `metaL` means: we should
write some code, which will *generate other program source code* in any other
mainstream language (Python, C++, Java,..).

In `metaL` we are not implementing the application, but we mostly should write
**generic code templates** for making a set of different applications resides in
some class. For example, somebody works in some narrow job areas such as Web
development. He was hired to write a lot of applications, which shares up to
50-95% of source code from project to project, and/or from customer to customer
(accounting software, logistics, small business web portals, webshops, etc. such
a like). These code patterns especially meaningful for freelance development,
when you have a lot of tiny clients, who want every time something special, but
mostly the same. And tadaam! every client requires from you to write this
supermegasite for his own language stack (Python/Django, Node.js, PHP legacy,
Java/Spring,..). And anyway, you must synchronize your code models between
backend (Python) and frontend (JavaScript) languages.

So, you spend your lifetime in rewriting notable amount of code, which is
sometimes similar and sometimes just the same, by copypasting it between
projects, doing some monkey patching to match models, syntax or names in your
app, writing API documentation,  propagating changes in this API and data scheme
between many parts of your app, moving code fixes and enhances between multiple
apps, etc. It does not look a good way to spend such a lot of time on mechanical
work in place of thinking and experimenting with your app models and ideas.

Also, we have here yet another big problem: programming languages Babylon. You
are forced to use some programming stack by your team and employer. Even if you
take some magic language tool like Python, Clojure/Lisp, or Haskell, in which
you can write as you think, you have no chances to push it into production use.
Nobody in your team doesn't want to learn yet another ancient or esoteric
language, and especially take hiring risks when you'll jump out or project
expands. Even if you are lucky enough to work in your favorite programing
language which is mainstream, or your team even lets you use something strange
like Lisp or Smalltalk, and you spent months or few years in writing of some
extra cool framework which helps you do anything fast and easy, BANG! you must
move to another language because of the next customer or management decision,
and you lost all of your jigs an polished clutches and start from scratch.

So, the `metaL` is an experiment in finding a workaround in such a class of
problems. The idea is about using some sort of [Model-Driven
Development](https://en.wikipedia.org/wiki/Model-driven_engineering) but not
using such stoned [OMG](https://www.omg.org/about/index.htm) (Oh My God!)
standards. Maybe it can be abbreviated as "Write Templates Freely" in place of.
`metaL` *uses (meta)language-based approach* in place of traditional and
dead-brained GUI monkey clicking. I'm not confronted against the GUI, it is just
the same order of magnitude more complex to implement than metalanguage
interpreter is more flexible and powerful. I mean the flexibility of interactive
development and power of reflection in Smalltalk systems, and self-appliance
magic in Lisp-like languages.
* generalize source code in arbitrary programming languages as typed data
  structures (attributed+ordered object tree/graph)
* provide Turing-complete (and handy!) interpreter works over these data
  structures to do structure self-modifications
* many data/program element types are able to recompile itself into 1+
  mainstream programming languages

If you look now in the one section above, you can understand the problem: even
simple programming term such as variable or function, must be representable *and
distinguishable* at least for `metaL` level, and for syntax of the **target
language** (into which you want to
[model-compile](https://en.wikipedia.org/wiki/Executable_UML#Model_compilation)
your software). Also, we can't forget about the **host language** in which your
`metaL` fork was implemented: its selection is governed by your preferences and
wishes, as at least for the first time you will be writing all
**transformations** in this programming language, not in `metaL`. Definitely,
you will not use some compile-only or low-level language such as ANSI C or Java
as a host language. It should be high-level, maybe without hard type checking
(debatable), extendable, must have a rich set of data structures in a language
core, and should support class-based OOP (due to `metaL` design). Some
candidates for a host language are Python (as widely known) and Clojure (as Lisp
dialect over JVM).

Also, you must not forget then `metaL` has two forms.

First, the pure *data-in-memory no-syntax language* available only from the host
language layer.
* Please note again: **data structures defined and manipulated in Python is the
  primary form of `metaL` programs**.
* **There is no data/program differentiation**: any program is a data structure,
  and every data structure is executable by `metaL` interpreter, both is the
  same.

Secondary, *script form* can be *optionally* used as single-line CLI commands
and for storing `metaL` programs/data in plain text files. This `metaL` language
form has more or less simple syntax, can be stored in files, edited in any
IDE/text editor, and shared via `git` or any other version control software and
tools. While `metaL` evolves, its scripts can maybe become the main form you are
working with (in complex with REPL in the running interactive system). But now
and a long time later, `metaL` script can't provide all methods required for
your knowledge graph definitions and transformations. Here, KG means structures
that describe your models, existing source code, generated source code, methods
of transformations, class/type taxonomy,... anything you want to remember and
process in software (and hardware?) [co]development. So, programming in `metaL`
means a *special method of programming in Python*, or any other host language,
if you want to implement your own `metaL` version in it (Haskell maybe? 8-).

Finally, we have to think about **four (!) languages** in every tiny
meta-project, **and model graph** in memory. It is even good if this languages
are different -- you can distinguish them at least syntactically. The worst-case
when you are trying to reimplement the `metaL` in itself (bootstrap),

@image html doc/tutorial.svg

I'm unconditionally sure that your brain already boils only reading these few
paragraphs. If you look at the `metaL` as yet another fun little language, just
skip it to next section and return after much practice later. Avoid the `metaL`
complexity by ignoring its targets. Play with scripting, or think in
`metaL`-in-Python, as a description of your program model, and running this
model interactively. This *model simulation* is a variant of `metaL` use, which
can be used for your model testing, requirements verification, or even in
production (in case if you host and target languages can be the same).

## `Object` graph

*This section is most important* to understand the `metaL` internals, please
don't skip it.

```py
# base object graph node
class Object:
    # construct object
    def __init__(self, V):
        # symbol name / scalar value (string, number,..)
        self.val = V
        # slots = attributes = dict = env
        self.slot = {}
        # nested AST = vector = stack = queue
        self.nest = []
        # global storage id
        self.gid = id(self)
```

The `metaL` language is built atop of
[object graph](https://en.wikipedia.org/wiki/Object_graph)
the same way as Lisp language is built over lists. Groups of objects inherited
from the base `Object` class form a network through their relationships with
each other via references -- in math terms it is oriented (directed) attributed
graph, *extended with an ability to store elements in order*. The difference
from the Lisp language model is all data elements are typed, and any subgraph
element can work as data containers simultaneously. There are no atoms, even
`Primitive` can have any attributes and any nested elements stored in order.

* `.val` scalar value in Python type, symbol name, string/number
* `.slot{}` named attributes, or slots -- some sort of variables, which holds
  binding between a name and some subgraph at the level of a given object (works
  like environment in Lisp)
* `.nest[]` ordered container, something like vector/list, which is strictly
  required for work with any source code was parsed into the AST
* `.gid` unique global id *needed for storing* data in key/value storage or
  database, *and to differ objects* looks like the same object (like two equal
  numbers reside in different places of some program)

If you have ever heard about compiler construction, you straightway see the
linkage between this unified data type, AST representation, and
[attribute grammars](https://en.wikipedia.org/wiki/Attribute_grammar).
Naturally, it is not a surprise because the `metaL` was created for and only for
working with arbitrary source code as a data structure. It has some ability to
be used as a general-purpose programming language itself, but mostly for
software models simulation in design time, not at production use.

Instances of the `Object` class is never used. This class must be inherited to
represent different data=program, but it can look like the universal data type,
which **can represent any knowledge**. If you want to implement some expert
system or logic programming engine over the `metaL`, this data model will stay
unchanged, but able to provide you any required behavior. Also, this model is
tightly close to the
[Frames concept](https://web.media.mit.edu/~minsky/papers/Frames/frames.html) in
AI.

@image html doc/taxonomy.svg

### Everything is an expression

Most popular programming languages devide code variants into two types of
elements: statements and expressions. Statements perform some action (e.g.
`if/else` blocks) and expressions which return values (e.g. `a + b`). In
`metaL`, everything is an expression which means that every object can be
evaluated, and be used where value is expected.

### Function is a first-class concept

Literally every single mainstream programming language these days introduced the
concept of lambdas. The "first-class" concept not only means that functions can
be passed as arguments, and returned as a result of other function: this ability
is available even in oldest C compilers. The most important thing is **function
can be created or modified in a runtime**.

## Operators

### ` tick = quote


Quoting operator differs from others as it blocks execution of all
subexpressions and returns them as-is:
```
<vm:metaL> `a

<op:`> #0f70d12e @7f36ef554400
    0: <symbol:a> #43870d7b @7f36ef5546d8

<symbol:a> #43870d7b @7f36ef5546d8
```
```
<vm:metaL> `(1+2)

<op:`> #89a1f3ef @7f445c6467b8
    0: <op:+> #4153b36f @7f445c64f7f0
        0: <integer:1> #47696a48 @7f445c64f860
        1: <integer:2> #2b7e8c83 @7f445c64f8d0

<op:+> #4153b36f @7f445c64f7f0
    0: <integer:1> #47696a48 @7f445c64f860
    1: <integer:2> #2b7e8c83 @7f445c64f8d0
```

The most frequently use of quoting is in slot assignment operations, as `metaL`
uses evaluable expressions for slot names identifying. So, every time you need
to define the slot (variable) name, you should use quoting to block the try of
resolving the name symbol.

### Slot assignment

#### Global assignment

By default slot named by a symbol will be allocated in global computation
context:
```
<vm:metaL> `a=1

<op:=> #8b9ce96c @7fddb6f07748
    0: <op:`> #0f70d12e @7fddb6efe7b8
        0: <symbol:a> #43870d7b @7fddb6f07470
    1: <integer:1> #47696a48 @7fddb6f078d0
```

First, ``a` evaluates as is to the `<symbol:a>`.
Next, the `=` operator uses `a` as the name of slot in the `<vm:metaL>` global context.

```
<integer:1> #47696a48 @7f87ee083908

<vm:metaL> #55b02009 @7f87ee7fdc50
    a = <integer:1> #47696a48 @7f87ee083908
```
Also, you can see that *assignment is an expression and returns a value*.

#### Object slot modification

With the **dot notation**, you can read and write slots that resides in arbitrary objects.

```
<vm:metaL> # define new module, available via global slot
<vm:metaL> `che = module:`modan

<op:=> #8b7b8b4e @7f1ff9e98d68
    0: <op:`> #1835c534 @7f1ff9e989e8
        0: <symbol:che> #a5384509 @7f1ff9e98cf8
    1: <op::> #14b78740 @7f1ff9e98eb8
        0: <symbol:module> #89706cbd @7f1ff9e98e48
        1: <op:`> #1268553f @7f1ff9e98ef0
            0: <symbol:modan> #132a9c3e @7f1ff9e98f98

<module:modan> #b249615e @7f1ff9e98dd8

<vm:metaL> #24c4e6ad @7f1ffa608e80
    che = <module:modan> #b249615e @7f1ff9e98dd8
```
Addressing to non-existent slot will be evaluated to `<undef:>` object.
```
<vm:metaL> che.doc

<op:.> #b6572576 @7f39540d9320
    0: <symbol:che> #a5384509 @7f39540d92b0
    1: <symbol:doc> #5894c1f0 @7f39540d9128

<undef:doc> #9c6f4403 @7f3954150908
    0: <module:modan> #b249615e @7f39540d91d0
```
