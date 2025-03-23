from S import *

class Class(Object):
    def __init__(self, name, sups=None, doc=None):
        super().__init__(name)
        self.sups = sups
        self.doc = f'\n/// @brief {doc}' if doc else None

    def gen(self, depth=0):
        public = ''
        if self.sups:
            public += ' : public '
            for s in self.sups: public += f'{s.val()}, '
            public = public[:-2]
        g = S(f'class {self.val()}{public} {{  //', '};', pfx=self.doc)
        for i in self.nest: g / i
        return g.gen()
