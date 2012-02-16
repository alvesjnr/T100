from t100.core.simulator import Simulator
from t100.core.components import *

"""
Example basic_03

Simulate for 1 hour
timestep = 1 second

Two sources
Source 1 frequency: 2 events each 5 minuts
Source 2 frequency: 3 events each 5 minuts

Unlimited queue size
Event take 1 minut +- 30 seconds (linear) to be processed

take the average time for 100 simulations
 
  ()   ----+
source 1   |
  ()   ----+->  |||||  ->   |P| 
source 2        queue      process  
    
"""

if __name__=='__main__':
    execution_time_expression = lambda : 60+random.randint(-30,+30)

    acc = 0
    for i in range(100):
        q = Queue()
        s1 = Source(output=q, creation_tax=2.0/(60*5), execution_time_expression=execution_time_expression)
        s2 = Source(output=q, creation_tax=3.0/(60*5), execution_time_expression=execution_time_expression)
        p = Process(inputs=[q])

        steps_number = 60*60

        simul = Simulator(components=[q,s1,s2,p])
        simul.run(untill=steps_number)
        q_size = len(simul.components['queue'][0])
        acc += q_size
    
    print acc/100.

    