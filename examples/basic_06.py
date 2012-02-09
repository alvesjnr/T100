from t100.simulator import Simulator
from t100.components import *

"""
Example basic_06
In a supermarket, estimate how many cashier would be necessary to avoid 
long lines for the frequency of 1~20 clients by each 5 minuts. Considere 
long line for line > 5 people

Simulate for 1 hour
timestep = 1 second


Two sources
Source 1 frequency: n/5 events each 5 minuts
Source 2 frequency: n events each 5 minuts

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

            AND GO ON ...
"""

if __name__=='__main__':

    steps_number = 60*60*5
    execution_time_expression = lambda : 60+random.randint(-30,+30)
    process_number = 1

    for f in range(20):
        frequency = f+1.0
        print '%i people per five minuts' % int(frequency)
        acc1 = acc2 = 0
        for i in range(20):
            q1 = Queue()
            q2 = Queue()
            s1 = Source(output=q1, creation_tax=frequency/5/(60*5), execution_time_expression=execution_time_expression)
            s2 = Source(output=q2, creation_tax=frequency/(60*5), execution_time_expression=execution_time_expression)
            p = []
            count = 0
            
            while process_number > count:
                p.append(Process(inputs=[q1,q2]))
                count += 1

            simul = Simulator(components=[q1,q2,s1,s2]+p)
            simul.run(untill=steps_number)
            q1_size = len(simul.components['queue'][0])
            q2_size = len(simul.components['queue'][1])


            acc1 += q1_size
            acc2 += q2_size
        
        print '#process: ', len(p)
        print 'high priority on line: ', acc1/20.
        print 'low priority on line :', acc2/20.
        print

        if acc2/20. > 5:
            process_number += 1

    