import sys
from t100.core import base_components as base
from t100.components import components as comp
from algorithms import step_algorithms

class Simulator(object):
    """"Simulator() works with base style components """
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

            if isinstance(component, base.Splitter):
                self.components['splitter'].append(component)
            elif isinstance(component, base.Queue):
                self.components['queue'].append(component)
            elif isinstance(component, base.Process):
                self.components['process'].append(component)
            elif isinstance(component, base.Source):
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


class DistributedSimulator(object):
    def __init__(self, components=[], verbose=False, output_file=sys.stdout):
        self.timestamp = 0
        self.components = {'source':[],
                           'splitter':[],
                           'process':[],
                           'queue':[],
                           'queuedprocess':[]}

        for component in components:

            if verbose: #Apply verbosity to every component
                component.verbose = True
                component.output_file = output_file

            if isinstance(component, comp.Splitter):
                self.components['splitter'].append(component)
            elif isinstance(component, comp.Queue):
                self.components['queue'].append(component)
            elif isinstance(component, comp.Process):
                self.components['process'].append(component)
            elif isinstance(component, comp.Source):
                self.components['source'].append(component)
            elif isinstance(component, comp.QueuedProcess):
                self.components['queuedprocess'].append(component)
        

    def add_component(self, component):
        self.components[str(type(component)).lower()].append(component)


    def run(self, untill=0, run_untill_queue_not_empty=False):
        acc = 0
        while untill > acc:
            self.step()
            untill -= 1
        
        if run_untill_queue_not_empty:
            # TODO
            # step_algorithms.run_process(self)
            pass
    
    def step(self):
        step_algorithms.distributed(self)