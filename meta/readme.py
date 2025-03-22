
from meta import *

def readme():
    with open('README.md', 'w') as f:
        print(f'''#  `{MODULE}`
##  {TITLE}
### {SUBTITLE}

(c) {AUTHOR} <<{EMAIL}>> {YEAR} {LICENSE}

github: {GITHUB}''', file=f)


readme()
