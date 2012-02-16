print 

try:
    from t100.core.simulator import Simulator
    from t100.core.components import *
except ImportError:
    print 'Alert!'
    print 't100 is not correctly installed on your computer'
    print 'Please, review your installations procedures'
else:
    print 'This  script just check if t100 is correctly installed on your computer'
    print 'If you can read it, thats all okay'

print