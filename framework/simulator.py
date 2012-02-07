
class Simulator(object):
    def __init__(self, components=[]):
        self.timestamp = 0
        self.components = {'source':[],
                           'splitter':[],
                           'process':[],
                           'queue':[]}

        for component in components:
            if isinstance(component, Splitter):
                self.elements['splitter'].append(component)
            elif isinstance(component, Queue):
                self.elements['queue'].append(component)
            elif isinstance(component, Process):
                self.elements['process'].append(component)
            elif isinstance(component, Source):
                self.elements['source'].append(component)
        
    def add_component(self, component):
        self.components[str(type(component)).lower()].append(component)

    def run(self, untill=0):
        while untill:
            self.step()
            untill -= 1
    
    def step(self):
        
