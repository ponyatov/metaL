import re
from Object import Object

## source code block
class S(Object):
    ## @param[in] pfx prefix line
    ## @paramp[in] sfx suffix line
    def __init__(self, value=None, pfx=None, sfx=None):
        super().__init__(value)
        self.pfx = pfx
        self.sfx = sfx

    ## generate code
    def gen(self, depth=0):
        ret = ''
        def pad(depth): return ' '*4*depth
        if self.pfx is not None:
            ret += f'{pad(depth)}{self.pfx}\n'
        if self.value is not None:
            ret += f'{pad(depth)}{self.val()}\n'
        for i in self.nest:
            ret += i.gen(depth + 1)
        if self.sfx is not None:
            ret += f'{pad(depth)}{self.sfx}\n'
        # ret = re.sub(r'^\n{',r'{',ret)
        return ret
