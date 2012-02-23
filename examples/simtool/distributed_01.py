from t100.components.components import *
from t100.simtool.distributed_env import Environment

import random
import sys


def creation_expression(timestamp):
    return 1.0/1000

def execution_expression(timestamp):
    return 10 + random.randint(-5,+5)

ip,port = 'localhost',9909

if  __name__=='__main__':
    
    queue = Queue()
    process = Process()
    source = Source(output=None,
                    creation_tax_expression=creation_expression,
                    execution_time_expression=execution_expression,)

    cfg = open('distributed_01.json').read()
    env = Environment(ip, port, cfg)
    env.populate([source,queue,process])