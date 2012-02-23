
from t100.core.simulator import Simulator

import sys

class Environment(object):
    def __init__(self, verbose=False, output_file=sys.stdout):
        self.verbose = verbose
        self.output_file = output_file
    
    def populate(self,components):
        self.simulator = Simulator(components, self.verbose, self.output_file)
        self.components = self.simulator.components
    
    def simulate(self, untill=0, run_untill_queue_not_empty=False):
        self.simulator.run(untill, run_untill_queue_not_empty)