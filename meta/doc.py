from IO import *

doc = Dir('doc')

eds = File('EDS.md'); doc / eds
(eds
 / r'## Executable Data Structure {#EDS}'
 / r'# EDS'
 / r'### Object Graph'
 )

forth = File('FORTH.md'); doc / forth
(forth
 / r'## The most simple postfix language {#FORTH}'
 / r'# FORTH')

doc.sync()
