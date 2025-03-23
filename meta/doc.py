from IO import *

doc = Dir('doc')

eds = File('EDS.md'); doc / eds
(eds
 / r'# EDS {#EDS}'
 / r'## Executable Data Structure'
 / r'### Object Graph'
 )

forth = File('FORTH.md'); doc / forth
(forth
 / r'# FORTH {#FORTH}'
 / r'## the most simple postfix language')

doc.sync()
