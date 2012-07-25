from t100.core.simulator import Simulator
from t100.core.base_components import *

def creation_tax_expression(timestamp):
    # 2 events each five minuts
    return 2.0/(60*5)

def execution_time_expression(timestamp):
    # execution takes 60 seconds +- 30
    return 60+random.randint(-30,+30)


if __name__=='__main__':

    acc = 0
    for i in range(100):
        q = Queue()
        s = Source(output=q, creation_tax_expression=creation_tax_expression, execution_time_expression=execution_time_expression)
        p = Process(inputs=[q])

        steps_number = 60*60 #1 second each timestamp, running for 60 minuts

        simul = Simulator(components=[q,s,p], verbose=True)
        simul.run(untill=steps_number)
        q_size = len(simul.components['queue'][0])
        acc += q_size
    
    print acc/100.

    