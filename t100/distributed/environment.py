from proxy import Proxy

import pickle
import StringIO
import time

class Dummy(object):
    def __init__(self):
        self.k = 0;
    def next(self):
        self.k += 1
        print self.k


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

    def __init__(self, ip, port, name):
        self.proxy = EnvProxy(env=self, ip=ip, port=port, name=name)
    
    def migrate(self,obj,destin):
        dumped_object = StringIO.StringIO()
        msg = Message('object',obj,None,destin)
        pickle.dump(msg, dumped_object)
        dumped_object.seek(0)
        self.send(dumped_object.read(), destin)
    
    def receive_migration(self,obj):
        obj.next()

    def send(self,msg, destin):
        self.proxy.send(msg, destin)
    



if __name__=='__main__':
    e = Environment('127.0.0.1', 6545, 'cow')
    d = Dummy()
    d.next()
    time.sleep(1)
    d.next()
    time.sleep(1)
    e.migrate(d,('127.0.0.1', 6549))

