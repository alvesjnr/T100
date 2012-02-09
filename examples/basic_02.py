from t100.simulator import Simulator
from t100.components import *

"""
Example basic_02

Simulate for 1 hour
timestep = 1 second

Source frequency: 2 events each 5 minuts
Unlimited queue size
Event take 1 minut +- 30 seconds (linear) to be processed

take the average time for 100 simulations

  ()   ->  |||||  ->   |P|
source     queue      process
    
"""

if __name__=='__main__':
    execution_time_expression = lambda : 60+random.randint(-30,+30)

    q = Queue()
    s = Source(output=q, creation_tax=10.0/(60*5), execution_time_expression=execution_time_expression)
    p = Process(input=q)

    steps_number = 60*60

    simul = Simulator(components=[q,s,p])
    simul.run(untill=steps_number)
    q_size = len(simul.components['queue'][0])
    print q_size

    