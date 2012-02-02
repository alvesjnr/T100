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
    queue = []

    def __init__(self, max_capacity=None):

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
    outputs = []

    def __init__(self,number_of_outputs):
        self.number_of_outputs = number_of_outputs
    
    def link_output(queue, output_number):
        self.output[output_number]['queue'] = queue
    
    def insert(self, event):

        if not isinstance(event, Event):
            raise SplitterError("Inserting non event object on splitter")
        
        output_number = self.__get_splitter_output__()

        if output_number is None:
            """As __get_splitter_output__ was not implemented, uses default function"""
            output_number = random.randint(0, len(self.outputs)-1) #TODO: must exist another way
        
        q = outputs[output_number]['queue']
        q.insert(event)


class Source(object):
    