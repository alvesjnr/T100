import sys
from base_components import *
from algorithms import step_algorithms

class Simulator(object):
    def __init__(self, components=[], verbose=False, output_file=sys.stdout):
        self.timestamp = 0
        self.components = {'source':[],
                           'splitter':[],
                           'process':[],
                           'queue':[]}

        for component in components:

            if verbose: #Apply verbosity to every component
                component.verbose = True
                component.output_file = output_file

            if isinstance(component, Splitter):
                self.components['splitter'].append(component)
            elif isinstance(component, Queue):
                self.components['queue'].append(component)
            elif isinstance(component, Process):
                self.components['process'].append(component)
            elif isinstance(component, Source):
                self.components['source'].append(component)
        
    def add_component(self, component):
        self.components[str(type(component)).lower()].append(component)

    def run(self, untill=0, run_untill_queue_not_empty=False):
        acc = 0
        while untill > acc:
            self.step()
            untill -= 1
        
        if run_untill_queue_not_empty:
            step_algorithms.run_process(self)
    
    def step(self):
        step_algorithms.trivial(self)
