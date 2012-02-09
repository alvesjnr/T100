from t100.components import *

def trivial(simulator):
    """This is the most simple algorithms for stepping a simulation"""
    
    timestamp = simulator.timestamp + 1
    simulator.timestamp = timestamp
    
    for source in simulator.components['source']:
        source.timestamp = timestamp
        source.generate()

    for process in simulator.components['process']:
        if process.timestamp <= timestamp:
            process.timestamp = timestamp
            process.next()

def run_process(simulator):
    """This is the most simple algorithms for stepping a simulation"""
        
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