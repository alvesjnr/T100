from components import *

class Simulator(object):
    def __init__(self, components=[]):
        self.timestamp = 0
        self.components = {'source':[],
                           'splitter':[],
                           'process':[],
                           'queue':[]}

        for component in components:
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

    def run(self, untill=0):
        acc = 0
        while untill > acc:
            self.step()
            print acc
            acc += 1
    
    def step(self):
        pass
