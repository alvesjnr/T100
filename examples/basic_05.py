from t100.simulator import Simulator
from t100.components import *

"""
Example basic_05
Calculating the impact of adding one more process

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
 
First scenery:
  ()   ------>  |||||---+
source 1        queue   |
  ()   ------>  ||||| --+->   |P| 
source 2        queue        process  

Second scenery:
  ()   ------>  |||||---+
source 1        queue   |
  ()   ------>  ||||| --+-->   |P| 
source 2        queue   |    process 1
                        +-->   |P|
                             process 2
"""

if __name__=='__main__':
    execution_time_expression = lambda : 60+random.randint(-30,+30)

    acc1 = acc2 = 0
    for i in range(100):
        q1 = Queue()
        q2 = Queue()
        s1 = Source(output=q1, creation_tax=1.0/(60*5), execution_time_expression=execution_time_expression)
        s2 = Source(output=q2, creation_tax=5.0/(60*5), execution_time_expression=execution_time_expression)
        p = Process(inputs=[q1,q2])

        steps_number = 60*60

        simul = Simulator(components=[q1,q2,s1,s2,p])
        simul.run(untill=steps_number)
        q1_size = len(simul.components['queue'][0])
        q2_size = len(simul.components['queue'][1])

        acc1 += q1_size
        acc2 += q2_size
    
    print acc1/100.
    print acc2/100.

    acc1 = acc2 = 0
    for i in range(100):
        q1 = Queue()
        q2 = Queue()
        s1 = Source(output=q1, creation_tax=1.0/(60*5), execution_time_expression=execution_time_expression)
        s2 = Source(output=q2, creation_tax=5.0/(60*5), execution_time_expression=execution_time_expression)
        p1 = Process(inputs=[q1,q2])
        p2 = Process(inputs=[q1,q2])

        steps_number = 60*60

        simul = Simulator(components=[q1,q2,s1,s2,p1,p2])
        simul.run(untill=steps_number)
        q1_size = len(simul.components['queue'][0])
        q2_size = len(simul.components['queue'][1])

        acc1 += q1_size
        acc2 += q2_size
    
    print acc1/100.
    print acc2/100.

    