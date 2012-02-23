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
    
    def set_output_file(self, file):
        self.output_file = file


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

    def __init__(self,number_of_outputs, select_output_expression=None, verbose=False, output_file=sys.stdout):
        super(Splitter, self).__init__(verbose, output_file)
        self.outputs = {}
        self.number_of_outputs = number_of_outputs
        self.select_output_expression = select_output_expression if select_output_expression else self.__random_output__

        for i in range(number_of_outputs):
            self.outputs[i] = {'element':None}
    
    def __random_output__(self,*args,**kwargs):        
        return random.randint(0,self.number_of_outputs)

    def link_output(self, output_number, queue, verbose=False, output_file=sys.stdout):
        self.outputs[output_number]['element'] = queue
    
    def insert(self, event):
        
        output_number = self.select_output_expression(self.timestamp, event)

        element = self.outputs[output_number]['element']
        element.insert(event)


class Source(__Component__):
    extra_params = ['execution_time_expression', 'delta_t_expression']

    component='S'

    def __init__(self, output, creation_tax_expression, timestamp=0, verbose=False, output_file=sys.stdout, **kwargs):
        super(Source, self).__init__(verbose, output_file)
        self.id = self.component + self.__get_serial_number__()
        self.timestamp = timestamp
        self.output = output
        self.output_id = output.id
        self.creation_tax_expression = creation_tax_expression

        for key in kwargs:
            if key in self.extra_params:
                setattr(self,key,kwargs[key])
    
    def generate(self):

        creation_tax = self.creation_tax_expression(self.timestamp)

        if random.random() < creation_tax:
            
            execution_time = self.execution_time_expression(self.timestamp)
            
            if hasattr(self, 'delta_t_expression'):
                timestamp = self.timestamp + self.delta_t_expression(self.timestamp)
            else:
                timestamp = self.timestamp
            
            event = Event(timestamp=timestamp, execution_time=execution_time)

            if self.verbose: 
                #log type A: an event born      
                self.__log__('A %s %s %s' % (self.timestamp, event, self))

            self.output.insert(event)



def output_ratio_dummy(*args,**kwargs):
    return 0

class Process(__Component__):

    component = 'P'


    def __init__(self, inputs=[], timestamp=0, source=None, output_ratio_expression=None, verbose=False, output_file=sys.stdout):
        super(Process, self).__init__(verbose, output_file)
        self.id = self.component + self.__get_serial_number__()
        self.inputs = inputs
        self.inputs_id = [input.id for input in inputs]
        self.timestamp = timestamp
        self.source = source
        self.output_ratio_expression = output_ratio_expression if output_ratio_expression else output_ratio_dummy
    
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

        if self.source and random.random() < self.output_ratio_expression(self.timestamp):
            self.source.generate(event)
        

class ProcessSource(Source):

    def __init__(self, reschedule=False, *args, **kwargs):
        super(ProcessSource, self).__init__(*args,**kwargs)
        self.reschedule = reschedule

    def generate(self, old_event):

        execution_time = self.execution_time_expression()
        
        if hasattr(self, 'delta_t_expression'):
            timestamp = self.timestamp + self.delta_t_expression(self.timestamp)
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
