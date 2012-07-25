from t100.core.simulator import Simulator
from t100.core.base_components import *

"""
Example basic_04

Simulate for 1 hour
timestep = 1 second

Two sources
Source 1 frequency: 1 events each 5 minuts
Source 2 frequency: 5 events each 5 minuts

Tqo queues
priority: queue1 > queue2

Unlimited queue size
Event take 1 minut +- 30 seconds (linear) to be processed

take the average time for 100 simulations
 
  ()   ------>  |||||---+
source 1        queue   |
  ()   ------>  |||||  -+->   |P| 
source 2        queue        process  
    
"""

def creation_tax_expression_1(timestamp):
    # 1 events each five minuts
    return 1.0/(60*5)

def creation_tax_expression_2(timestamp):
    # 5 events each five minuts
    return 5.0/(60*5)

def execution_time_expression(timestamp):
    # execution takes 60 seconds +- 30
    return 60+random.randint(-30,+30)

if __name__=='__main__':

    steps_number = 60*60

    acc1 = acc2 = 0
    for i in range(100):
        q1 = Queue()
        q2 = Queue()
        s1 = Source(output=q1, creation_tax_expression=creation_tax_expression_1, execution_time_expression=execution_time_expression)
        s2 = Source(output=q2, creation_tax_expression=creation_tax_expression_2, execution_time_expression=execution_time_expression)
        p = Process(inputs=[q1,q2])

        simul = Simulator(components=[q1,q2,s1,s2,p])
        simul.run(untill=steps_number)
        q1_size = len(simul.components['queue'][0])
        q2_size = len(simul.components['queue'][1])

        acc1 += q1_size
        acc2 += q2_size
    
    print acc1/100.
    print acc2/100.

    