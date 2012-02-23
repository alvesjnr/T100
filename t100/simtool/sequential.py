from t100.core.simulator import Simulator

import sys

class Environment(object):
    def __init__(self,  components=[], verbose=False, output_file=sys.stdout):
        self.simulator = Simulator(components, verbose, output_file)
        self.components = self.simulator.components
    
    def simulate(self, untill=0, run_untill_queue_not_empty=False):
        self.simulator.run(untill, run_untill_queue_not_empty)