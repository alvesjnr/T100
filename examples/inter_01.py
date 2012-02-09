from t100.simulator import Simulator
from t100.components import *

import sys

"""
Example inter_01
This example introduces refeed (send a event to itself)

Simulate for 1 hour
timestep = 1 second

One source
Source frequency: 3 events each 5 minuts

Unlimited queue size
Event take 1 minut +- 30 seconds (linear) to be processed

take the average time for 20 simulations

            10%
         v---------+
() ->  |||| ->|P|--+
source queue  process

10 per cent of the processed events generate a new event for a time t = timestamp + 30 += 10 seconds

"""

if __name__=='__main__':

    steps_number = 60*60
    
    execution_time_expression = lambda : 60+random.randint(-30,+30)
    delta_t_expression = lambda : 30+random.randint(1,10)


    q = Queue()
    s = Source(output=q, 
               creation_tax=2.0/(60*5), 
               execution_time_expression=execution_time_expression,
               verbose=True, output_file=sys.stdout)
    ps = ProcessSource(output=q, #process source 
                execution_time_expression=execution_time_expression,
                delta_t_expression=delta_t_expression,)
    p = Process(inputs=[q], source=ps, output_ratio=0.1, verbose=True, output_file=sys.stdout)
    p.output = p

    simul = Simulator(components=[q,s,p])
    simul.run(untill=steps_number, run_untill_queue_not_empty=True)

     