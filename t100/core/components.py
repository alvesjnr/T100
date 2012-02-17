from errors import *

import sys
import random
import time


class __Component__(object):
    """ Base class which takes care about logging"""
    serial_number = 0
        
    def __init__(self,verbose=False, output_file=sys.stdout ):
        self.verbose = verbose
        self.output_file = output_file
    
    def __log__(self, message):
        f = self.output_file
        f.write(message + '\n')
    
    @classmethod
    def __get_serial_number__(cls):
        cls.serial_number += 1
        return str(cls.serial_number)

    def __repr__(self):
        return str(self.id)


class Event(__Component__):

    component='E'
    
    def __init__(self, timestamp=0, execution_time=None, verbose=False, output_file=sys.stdout, explicit_id=None):
        super(Event, self).__init__(verbose, output_file)

        self.timestamp = timestamp
        self.locked=False
        
        if explicit_id:
            self.id = explicit_id
        else:
            self.id = self.component + self.__get_serial_number__()

        if execution_time:
            self.execution_time = execution_time
        else:
            self.__execution_behavior__()

    def __repr__(self):
        return '(%s, %i)' % (self.id, self.timestamp)
     
    def __run__(self, parent):
        #just a placeholder, a placebo, must be overwrited
        parent.timestamp += int(self.execution_time)
    
    def __execution_behavior__(self):
        #just a placeholder, a placebo, must be overwrited
        self.execution_time = random.randint(1,10)  



class Queue(__Component__):

    component='Q'
    
    def __init__(self, max_capacity=None, verbose=False, output_file=sys.stdout, timestamp=0):
        super(Queue, self).__init__(verbose, output_file)
        self.id = self.component + self.__get_serial_number__()
        self.timestamp = timestamp
        self.queue = []
        self.max_capacity = max_capacity

    def insert(self, event):
        if self.max_capacity and len(self.queue) == self.max_capacity:
            raise SimulationError("Queue %s reached maximum capacity" % (event))
        if not isinstance(event,Event):
            raise QueueError("Inserting non event object on queue")
        
        if self.verbose:
            #Log type B: an event enter on a queue
            self.__log__('B %s %s %s' % (self.timestamp, event, self))
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



class Splitter(__Component__):

    def __init__(self,number_of_outputs, verbose=False, output_file=sys.stdout):
        super(Splitter, self).__init__(verbose, output_file)
        self.outputs = {}
        self.number_of_outputs = number_of_outputs

        for i in range(number_of_outputs):
            self.outputs[i] = {'element':None}
    
    def link_output(self, output_number, queue, verbose=False, output_file=sys.stdout):
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
    



class Source(__Component__):
    extra_params = ['execution_time_expression', 'creation_tax', 'delta_t_expression']

    component='S'

    def __init__(self, output, timestamp=0, verbose=False, output_file=sys.stdout, **kwargs):
        super(Source, self).__init__(verbose, output_file)
        self.id = self.component + self.__get_serial_number__()
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
            
            if hasattr(self, 'delta_t_expression'):
                timestamp = self.timestamp + self.delta_t_expression()
            else:
                timestamp = self.timestamp
            
            event = Event(timestamp=timestamp, execution_time=execution_time)

            if self.verbose: 
                #log type A: an event born      
                self.__log__('A %s %s %s' % (self.timestamp, event, self))

            self.output.insert(event)



class Process(__Component__):

    component = 'P'

    def __init__(self, inputs=[], timestamp=0, source=None, output_ratio=0.0, verbose=False, output_file=sys.stdout):
        super(Process, self).__init__(verbose, output_file)
        self.id = self.component + self.__get_serial_number__()
        self.inputs = inputs
        self.timestamp = timestamp
        self.source = source
        self.output_ratio = output_ratio
    
    def next(self):
        for i in self.inputs:
            if i.youngest_event() <= self.timestamp:
                event = i.remove()
                if event:           
                    if self.verbose:
                        self.__log__('C %s %s %s %s' % (self.timestamp, event, i, self))
                        self.execute_event(event)
                        self.__log__('D %s %s %s' % (self.timestamp, event, self))
                    else:
                        self.execute_event(event)
                    break

    def execute_event(self, event):
        event.__run__(self)

        if self.source and random.random() < self.output_ratio:
            self.source.generate(event)
        

class ProcessSource(Source):

    def __init__(self, reschedule=False, *args, **kwargs):
        super(ProcessSource, self).__init__(*args,**kwargs)
        self.reschedule = reschedule

    def generate(self, old_event):

        if hasattr(self, 'execution_time_expression'):
            execution_time = self.execution_time_expression()
        else:
            execution_time = random.randint(1,5)
        
        if hasattr(self, 'delta_t_expression'):
            timestamp = self.timestamp + self.delta_t_expression()
        else:
            timestamp = self.timestamp
        
        if self.reschedule:
            event_id = old_event.id
        else:
            event_id = None
        event = Event(timestamp=timestamp, execution_time=execution_time, explicit_id=event_id)

        if self.verbose:
            if self.reschedule:
                self.__log__('F %s %s' % (timestamp, event))
            else:
                self.__log__('E %s %s %s %s' % (timestamp, event, self, old_event))
        
        self.output.insert(event)
