from distributed.proxy import Proxy
from t100.core.simulator import DistributedSimulator as Simulator
from t100.components.components import DummyConector

import StringIO
import pickle
import json
import time
import sys

class Message(object):
    def __init__(self,type,content=None,origin=None,destin=None,meta=None):
        self.type = type
        self.content = content
        self.origin = origin
        self.destin = destin
        self.meta = meta
    
    def dumped(self):
        dumped_object = StringIO.StringIO()
        pickle.dump(self, dumped_object)
        dumped_object.seek(0)
        return dumped_object.read()


class EnvProxy(Proxy):
    """ This overwritted class customize a basic proxy to works
        as we want on a environment
    """
    def __init__(self, env, *args, **kwargs):
        super(EnvProxy,self).__init__(*args, **kwargs)
        self.env = env
        self.components_catalog = {}    #catalog with ALL components in simulation system
        self.nodes = []

    def receive(self,msg):
        msg = pickle.loads(msg)
        print msg.type
        if msg.type == 'event':
            self.env.dummy_insert_input(msg.content, msg.origin, msg.destin)
        elif msg.type == 'object':
            self.env.receive_migration(msg.content)
        elif msg.type == 'EOP': # end of populate
            self.env.prepare_simulation()
        elif msg.type == 'START':
            self.env.start_simulation(untill=msg.content['untill'],
                                      run_untill_queue_not_empty=msg.content['run_untill_queue_not_empty'])
        elif msg.type == 'RST': # reset
            self.env.reset_environment()
            self.components_catalog = {}
        elif msg.type == 'CFG':
            self.env.update_components_profile(msg)
    
    def sendall(self,msg):
        for node in self.nodes:
            if node != self.env.address:
                self.send(msg,node)


class Environment(object):
    def __init__(self, ip, port, cfg=None, verbose=False, output_file=sys.stdout):
        self.address = (ip,port)
        self.name = "%s:%s" % (ip,port)
        self.proxy = EnvProxy(env=self, ip=ip, port=port)
        self.verbose = verbose
        self.output_file = output_file
        self.main_node = False
        
        self.reset_environment()

        if cfg:
            self.__configure_simulation__(cfg)
        
        self.proxy.sendall(Message('RST').dumped())
    
    def __configure_simulation__(self,cfg):
        self.main_node = True
        self.configurations = json.loads(cfg)
        for node in self.configurations['nodes']:
            ip,port = node.split(':')
            self.proxy.nodes.append((ip,int(port)))


    def populate(self, components):
        self.number_of_components = len(components)
        components_per_node = self.number_of_components / self.configurations['number_of_nodes']
        for n,item in enumerate(components):
            if n < components_per_node:
                self.add_component(item)
            else:
                self.dispatch_component(item,n)
        
        for node in self.configurations['nodes']:
            if node != self.name:
                ip,port = node.split(':')
                port = int(port)
                self.send(Message('EOP').dumped(),(ip,port)) #end of populate
                self.prepare_simulation()


    def prepare_simulation(self):
        self.reconnect_components()
        self.update_components_profile()
        components = [value for key,value in self.components.items()]
        self.simulator = Simulator(components, self.verbose, self.output_file)


    def update_components_profile(self, msg=None):
        if self.main_node and msg is None:
            nodes = [address.split(':') for address in self.configurations['nodes']]
            nodes = map(lambda a : (a[0],int(a[1])), nodes)
            components_catalog = dict((key,self.address) for key in self.components)
            msg = Message('CFG',{'nodes':nodes,
                                 'components':components_catalog}
                                 ,nodes[1], self.name, 1).dumped()
            self.send(msg, nodes[1])
        
        elif self.main_node and msg:
            self.proxy.components_catalog = msg.content['components']

        elif msg:
            self.proxy.nodes = msg.content['nodes'][::]
            self.proxy.components_catalog = msg.content['components']
            self.proxy.components_catalog.update( dict((key,self.address) for key in self.components) )
            next_node = msg.meta+1
        
            if next_node == len(self.proxy.nodes):
                next_node = 0
        
            msg = Message('CFG',{'nodes':self.proxy.nodes,
                                 'components': self.proxy.components_catalog},self.proxy.nodes[next_node], self.name, next_node).dumped()
            self.send(msg, self.proxy.nodes[next_node])
        


            
    def reconnect_components(self):
        for key in self.components:
            self.connect_component(self.components[key])

    
    def connect_component(self, component):
        if hasattr(component,'output'):
            if component.output_id in self.components:
                component.output = self.components[component.output_id]
            else:
                d = DummyConector(self.dummy_insert_output, component.id)
                component.output = d
        if hasattr(component,'insert'):
            self.external_inputs[component.id] = component.insert

    
    def add_component(self, component):
        self.components[component.id] = component
    

    def dispatch_component(self, component, n):
        host_index = (self.number_of_components - (self.number_of_components/self.configurations['number_of_nodes']))%n+1
        ip,port = self.configurations['nodes'][host_index].split(':')
        port = int(port)
        if hasattr(component,'output'):
            component.output=None

        self.migrate(component, (ip,port))
    

    def migrate(self,obj,destin):
        obj.set_output_file(None)
        dumped_object = StringIO.StringIO()
        msg = Message('object',obj,self.address,destin)
        pickle.dump(msg, dumped_object)
        dumped_object.seek(0)
        self.send(dumped_object.read(), destin)
    
    
    def receive_migration(self,obj):
        print obj
        self.components[obj.id] = obj
        if self.simulating:
            self.connect_component(obj)

    
    def dummy_insert_output(self, event, sender_id, receiver_id):
        # connects in-place components to SEND events to external word
        event.output_file=None
        msg = Message('event', event, sender_id, receiver_id)
        dumped_object = StringIO.StringIO()
        pickle.dump(msg, dumped_object)
        dumped_object.seek(0)
        self.send(dumped_object.read(), self.proxy.components_catalog[receiver_id])
    

    def dummy_insert_input(self, event, sender_id, receiver_id):
        # connects in-place components to RECEIVE events from external word
        insert_function = self.external_inputs[receiver_id]
        insert_function(event)

    
    def send(self,msg,destin):
        self.proxy.send(msg, destin)
    
    
    def start_simulation(self, untill=0, run_untill_queue_not_empty=False):
        self.simulating = True
        if self.main_node:
            self.proxy.sendall(Message('START', {'untill':untill, 
                                                 'run_untill_queue_not_empty':run_untill_queue_not_empty}
                                      ).dumped())
        self.simulator.run(untill,run_untill_queue_not_empty)
    
    
    def reset_environment(self):
        self.components = {}
        self.external_inputs = {}
        self.simulating = False
        self.message_buffer = []


    def loop(self):
        while True:
            time.sleep(10)


if __name__=='__main__':
    pass
