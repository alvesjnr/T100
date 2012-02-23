from t100.core.simulator import Simulator
from t100.core.base_components import *

if __name__=='__main__':

    acc = 0
    for i in range(100):
        q = Queue()
        s = Source(output=q)
        p = Process(inputs=[q])

        simul = Simulator(components=[q,s,p])
        simul.run(untill=1000)
        q_size = len(simul.components['queue'][0])
        acc += q_size
    
    print acc/100.0
