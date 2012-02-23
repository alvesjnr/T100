from distributed.proxy import Proxy

import pickle
import StringIO
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
        self.name = "%s:%s" % (self.ip,self.port)
        self.proxy = EnvProxy(env=self, ip=ip, port=port)
        self.verbose = verbose
        self.output_file = output_file
        self.__configure_simulation__(cfg)
    
    def __configure_simulation__(self,cfg):
        self.configurations = cfg

    def populate(self, components):
        self.number_of_components = len(components)
        components_per_node = self.number_of_components/self.configurations['number_of_nodes']
        for n,item in enumerate(components):
            if n < components_per_node:
                self.add_component(item)
            else:
                self.dispatch_component(item,n)

        self.simulator = Simulator(self.verbose,self.output_file)
    
    def dispatch_component(self, component, n):
        host_index = n%(self.number_of_components-1)+1
        ip,port = self.configurations['nodes'][host_index].split(':')
        port = int(port)
        if hasattr(component,'output'):
            #ver quem é o cara da output!
            #acho que o próprio component pode fazre isso!!!
            component.output=None
        self.migrate(component, (ip,port))

    
    def migrate(self,obj,destin):
        dumped_object = StringIO.StringIO()
        msg = Message('object',obj,self.address,destin)
        pickle.dump(msg, dumped_object)
        dumped_object.seek(0)
        self.send(dumped_object.read(), destin)
    
    def receive_migration(self,obj):
        pass

    def send(self,msg,destin):
        self.proxy.send(msg, destin)
    
    def simulate(self, untill=0, run_untill_queue_not_empty=False):
        self.simulator.run(untill, run_untill_queue_not_empty)


if __name__=='__main__':
    pass
