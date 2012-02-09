from t100.simulator import Simulator
from t100.components import *

if __name__=='__main__':

    acc = 0
    for i in range(100):
        q = Queue()
        s = Source(output=q)
        p = Process(input=q)

        simul = Simulator(components=[q,s,p])
        simul.run(untill=1000)
        q_size = len(simul.components['queue'][0])
        acc += q_size
    
    print acc/100.0