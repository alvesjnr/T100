from t100.simulator import Simulator
from t100.components import *

if __name__=='__main__':
    q = Queue()
    s = Source(output=q)
    p = Process(input=q)

    simul = Simulator(components=[q,s,p])

    simul.run(untill=10)
