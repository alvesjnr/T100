from t100.core.base_components import *

def trivial(simulator):
    """This is the most simple algorithms for stepping a simulation"""
    
    timestamp = simulator.timestamp + 1
    simulator.timestamp = timestamp
    
    for source in simulator.components['source']:
        source.generate()
        source.timestamp = timestamp

    for process in simulator.components['process']:
        if process.timestamp <= timestamp:
            process.timestamp = timestamp
            process.next()
    
    for queue in simulator.components['queue']:
        queue.timestamp = timestamp


def run_process(simulator):
    """Run all process till all queues get empty"""
        
    while True:
    
        timestamp = simulator.timestamp + 1
        simulator.timestamp = timestamp

        for process in simulator.components['process']:
            if process.timestamp <= timestamp:
                process.timestamp = timestamp
                process.next()   
        
        events_on_queue = sum([len(q) for q in simulator.components['queue']])
    
        if not events_on_queue:
            break


def distributed(simulator):
    """ runs distributed simulation """

    timestamp = simulator.timestamp + 1
    simulator.timestamp = timestamp
    
    for source in simulator.components['source']:
        source.generate()
        source.timestamp = timestamp

    for qprocess in simulator.components['queuedprocess']:
        if qprocess.timestamp <= timestamp:
            qprocess.timestamp = timestamp
            qprocess.processer.next()
        qprocess.queue.timestamp = timestamp
    
    for queue in simulator.components['queue']:
        queue.timestamp = timestamp
