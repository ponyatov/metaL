from IO import *

cf = (File('.clang-format')
      / r'BasedOnStyle: Google'
      / r'IndentWidth:  4'
      / r'TabWidth:     4'
      / r'UseTab:       Never'
      / r'ColumnLimit:  80'
      / r'UseCRLF:      false'
      / r''
      / r'SortIncludes: false'
      / r''
      / r'AllowShortBlocksOnASingleLine: Always'
      / r'AllowShortFunctionsOnASingleLine: All'
      )
cf.sync()

prc = File('.prettierrc')
prc / (S(None, '{', '}')
       / r'"tabWidth"    : 4,'
       / r'"useTabs"     : false,'
       / r'"endOfLine"   : "lf",'
       / r'"singleQuote" : true,'
       / r'"semi"        : true,'
       / r'"printWidth"  : 80'
       )
prc.sync()
