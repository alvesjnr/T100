from t100.core.simulator import Simulator
from t100.core.components import *

"""
Example inter_03
for informations about this examples, see docs/examples/inter_03

"""

if __name__=='__main__':

    steps_number = 60*60
    
    execution_time_expression = lambda : 60+random.randint(-30,+30)
    delta_t_expression = lambda : 30+random.randint(1,10)

    s = Source(output=q, 
               creation_tax=2.0/(60*5), 
               execution_time_expression=execution_time_expression,)
    ps = ProcessSource(output=q, #process source 
                execution_time_expression=execution_time_expression,
                delta_t_expression=delta_t_expression, verbose=True)
    p = Process(inputs=[q], source=ps, output_ratio=0.1)
    p.output = p

    simul = Simulator(components=[q,s,p], verbose=True)
    simul.run(untill=steps_number, run_untill_queue_not_empty=True)

 
    