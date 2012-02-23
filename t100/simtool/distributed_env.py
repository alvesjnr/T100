from distributed.proxy import Proxy
from t100.core.simulator import Simulator

import StringIO
import pickle
import json
import time
import sys

class Message(object):
    def __init__(self,type,content,origin,destin):
        self.type = type
        self.content = content
        self.origin = origin
        self.destin = destin


class EnvProxy(Proxy):
    """ This overwritted class customize a basic proxy to works
        as we want on a environment
    """
    def __init__(self, env, *args, **kwargs):
        super(EnvProxy,self).__init__(*args, **kwargs)
        self.env = env

    def receive(self,msg):
        msg = pickle.loads(msg)
        if msg.type == 'object':
            self.env.receive_migration(msg.content)


class Environment(object):
    def __init__(self, ip, port, cfg=None, verbose=False, output_file=sys.stdout):
        self.address = (ip,port)
        self.name = "%s:%s" % (ip,port)
        self.proxy = EnvProxy(env=self, ip=ip, port=port)
        self.verbose = verbose
        self.output_file = output_file
        self.components = {}

        if cfg:
            self.__configure_simulation__(cfg)
    
    def __configure_simulation__(self,cfg):
        self.configurations = json.loads(cfg)


    def populate(self, components):
        self.number_of_components = len(components)
        components_per_node = self.number_of_components / self.configurations['number_of_nodes']
        for n,item in enumerate(components):
            if n < components_per_node:
                self.add_component(item)
            else:
                self.dispatch_component(item,n)
        
        for node in self.configurations['nodes']:
            # send messages for nodes, for component conections, update profiles, add output file etc.
            pass
        
        self.reconnect_components()
        self.update_components_profile()
        components = [value for key,value in self.components]
        self.simulator = Simulator(components, self.verbose, self.output_file)


    def update_components_profile(self):
        # atualiza informacoes referente aos processos existentes no host
        pass
            
    def reconnect_components(self):
        # refaz todas as conexoes necesssrias quebradas pela separacao
        pass
    
    def add_component(self, component):
        self.components[component.id] = component
    
    def dispatch_component(self, component, n):
        host_index = (self.number_of_components - (self.number_of_components/self.configurations['number_of_nodes']))%n+1
        ip,port = self.configurations['nodes'][host_index].split(':')
        port = int(port)
        if hasattr(component,'output'):
            #ver quem e o cara da output!
            #acho que o proprio component pode fazre isso!!!
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
        pass

    def send(self,msg,destin):
        self.proxy.send(msg, destin)
    
    def simulate(self, untill=0, run_untill_queue_not_empty=False):
        self.simulator.run(untill, run_untill_queue_not_empty)
    
    def reset_environment(self):
        pass
    
    def loop(self):
        while True:
            time.sleep(10)


if __name__=='__main__':
    pass
