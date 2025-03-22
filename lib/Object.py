## executable object graph item
class Object:

    def __init__(self, value):
        ## scalar value
        self.value = value
        ## nested elements (object subtree)
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

from S import *
