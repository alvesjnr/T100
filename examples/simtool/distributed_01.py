from t100.components.components import *
from t100.simtool.distributed_env import Environment

import random
import time
import sys


def creation_expression(timestamp):
    return 1.0/1000

def execution_expression(timestamp):
    return 10 + random.randint(-5,+5)

ip,port = 'localhost',11111

if  __name__=='__main__':
    
    process = QueuedProcess()
    source = Source(output=process,
                    creation_tax_expression=creation_expression,
                    execution_time_expression=execution_expression,)

    cfg = open('distributed_01.json').read()
    env = Environment(ip, port, cfg, verbose=True)
    env.populate([source,process])
    import pdb; pdb.set_trace()
    time.sleep(29999)
    #env.start_simulation(untill=1000)