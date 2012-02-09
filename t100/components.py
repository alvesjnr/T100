import random
import time

class SimulationError(Exception):
    def __init__(self, message=None):
        self.message = message


class QueueError(Exception):
    def __init__(self, message=None):
        self.message=message


class Event(object):
    
    def __init__(self, timestamp=0, execution_time=None,):
        self.timestamp = timestamp
        self.locked=False
        if execution_time:
            self.execution_time = execution_time
        else:
            self.__execution_behavior__()
    
    def __repr__(self):
        return '%s with timestamp %i>' % (str(self.__class__)[:-1], self.timestamp)
     
    def __run__(self, parent):
        #just a placeholder, a placebo, must be overwrited
        parent.timestamp += int(self.execution_time)
    
    def __execution_behavior__(self):
        self.execution_time = random.randint(1,10)


class Queue(object):
    
    def __init__(self, max_capacity=None):
        self.queue = []
        self.max_capacity = max_capacity

    def insert(self, event):
        if self.max_capacity and len(self.queue) == self.max_capacity:
            raise SimulationError("Queue %s reached maximum capacity" % (event))
        if not isinstance(event,Event):
            raise QueueError("Inserting non event object on queue")
        
        self.queue.append(event)
        self.queue.sort(key=lambda event: event.timestamp)
    
    def remove(self):
        if len(self.queue) == 0:
            return None
        else:
            return self.queue.pop(0)
    
    def youngest_event(self):
        if len(self.queue) > 0:
            return self.queue[0].timestamp
        else:
            return None
    
    def __len__(self):
        return len(self.queue)


class Splitter(object):
    
    def __init__(self,number_of_outputs):
        self.outputs = {}
        self.number_of_outputs = number_of_outputs

        for i in range(number_of_outputs):
            self.outputs[i] = {'element':None}
    
    def link_output(self, output_number, queue):
        self.outputs[output_number]['element'] = queue
    
    def insert(self, event):
        if not isinstance(event, Event):
            raise SplitterError("Inserting non event object on splitter")
        
        output_number = self.__get_splitter_output__()

        if output_number is None:
            """As __get_splitter_output__ was not implemented, uses default function"""
            output_number = random.randint(0, len(self.outputs)-1) #TODO: must exist another way
        
        element = self.outputs[output_number]['element']
        element.insert(event)
    
    def __get_splitter_output__(self):
        """Not yet implemented"""


class Source(object):
    extra_params = ['execution_time_expression', 'creation_tax']
    def __init__(self, output, timestamp=0, **kwargs):
        self.timestamp = timestamp
        self.output = output

        for key in kwargs:
            if key in self.extra_params:
                setattr(self,key,kwargs[key])

    def generate(self):

        if hasattr(self, 'creation_tax'):
            creation_tax = self.creation_tax
        else:
            creation_tax = 0.5

        if random.random() < creation_tax:
            if hasattr(self, 'execution_time_expression'):
                execution_time = self.execution_time_expression()
            else:
                execution_time = random.randint(1,5)
            self.output.insert(Event(timestamp=self.timestamp, execution_time=execution_time))
            print 't=%s, creating event with execution_time=%s' % (self.timestamp, execution_time)


class Process(object):
    def __init__(self, input=None, timestamp=0):
        self.input = input
        self.timestamp = timestamp
    
    def next(self):

        if self.input and self.input.youngest_event() <= self.timestamp:
            event = self.input.remove()
            if event:           
                self.execute_event(event)

    def execute_event(self, event):
        event.__run__(self)

