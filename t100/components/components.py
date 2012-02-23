from t100.core import base_components as bc

class DummyConector(object):
    """ Makes a connection between an component and an evironment
    """
    def __init__(self, output):
        self.output = output

    def insert(self, event):
        self.output.insert(event)

class Source(bc.Source):
    """ Source accept two parameters:
            creation_tax_expression: is an expression that returns the probability 
                of an event be created in a time t
            execution_time_expression: is an expression that return the timestamp
                of the created event
    """

class Splitter(bc.Splitter):
    
    """ Split accept two parameters:
            number_of_outputs: its name explains itself
            select_output_expression: An expression that select which output will be
                selected. This expression receive two parameters: timestamp and event
    """

class Queue(bc.Queue):
    """ Queue accept one parameter:
            max_size
    """

class Process(bc.Process):
    """ Process accept three parameters:
            number_of_outputs: its name explains itself
            select_output_expression: An expression that select which output will be
                selected. This expression receive two parameters: timestamp and event
    """


class QueuedProcess(bc.__Component__):
    component = 'QP'

    def __init__(self, output=None, reschedule=False):
         self.id = self.component + self.__get_serial_number__()
         self.queue = bc.Queue()
         self.processer = bc.Process(inputs=[self.queue])
         #self.output_source = bc.ProcessSource()
    
    def insert(self, event):
        self.queue.insert(event)

    def set_output_file(self, file):
        self.queue.set_output_file(file)
        self.processer.set_output_file(file)

class MultiQueuedMultiProcess(bc.__Component__):
    component = 'MQMP'

    def __init__(self,input_number, process_number, ):
        self.id = self.component + self.__get_serial_number__()

