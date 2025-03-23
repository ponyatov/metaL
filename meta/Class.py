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
        g / (S('public:') / f'{self.val()}();')
        if self.val() == 'Object':
            g / f'virtual ~{self.val()}();'
        return g.gen()

    def cpp(self):
        g = G(f'/// {self.head()}', pfx='')
        if self.val() == 'Object':
            (g / f'{self.val()} *{self.val()}::pool = nullptr;')
            (g / (S(f'{self.val()}::{self.val()}() {{  //', '}')
                  / 'ref = 0;'
                  / 'prev = pool;' / 'pool = this;'))
            (g / (S(f'{self.val()}::~{self.val()}() {{  //', '}')
                  / ''))
        else:
            (g / (S(f'{self.val()}::{self.val()}():{self.sups[0].val()}() {{  //', '}')))
        return g
