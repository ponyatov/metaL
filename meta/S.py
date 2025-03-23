from Object import Object

## source code block
class S(Object):
    ## @param[in] pfx prefix line
    ## @paramp[in] sfx suffix line
    def __init__(self, start=None, end=None, pfx=None, sfx=None):
        super().__init__(start)
        self.start = start; self.end = end
        self.pfx = pfx; self.sfx = sfx

    ## generate code
    def gen(self, depth=0):
        ret = ''
        def pad(depth): return ' ' * 4 * depth
        if self.pfx is not None:
            ret += f'{pad(depth)}{self.pfx}\n'
        if self.start is not None:
            ret += f'{pad(depth)}{self.start}\n' if self.start else '\n'
        for i in self.nest:
            ret += i.gen(depth + 1)
        if self.end is not None:
            ret += f'{pad(depth)}{self.end}\n' if self.end else '\n'
        if self.sfx is not None:
            ret += f'{pad(depth)}{self.sfx}\n'
        return ret
