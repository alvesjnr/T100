import random

class SimulationError(Exception):
    def __init__(self, message=None):
        self.message = message


class QueueError(Exception):
    def __init__(self, message=None):
        self.message=message


class Event(object):
    timestamp = 0

    def __init__(self, timestamp=0):
        self.timestamp = timestamp
    
    def __repr__(self):
        return '%s with timestamp %i' % (self.__class__, self.timestamp)
    

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
        return self.queue[0]


class Splitter(object):
    outputs = {}

    def __init__(self,number_of_outputs):
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
    timestamp = 0
    output = None

    def __init__(self, output):
        self.output = output

    def generate(self):

        if random.random() > 0.5:
            delta_t = random.randint(1,10)
            self.output.insert(Event(timestamp=self.timestamp+delta_t))


if __name__=='__main__':

    q1 = Queue()
    q2 = Queue()
    s = Splitter(2)

    s.link_output(0, q1)
    s.link_output(1, q2)

    source = Source(s)

    source.generate()
    source.generate()
    source.generate()
    source.generate()
    
    print q1.queue
    print q2.queue
