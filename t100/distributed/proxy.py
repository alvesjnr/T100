# Echo server program
import socket
import thread
import time

STATUS = ['active', 'away', 'transit', 'inactive']
		
class Proxy(object):

    def __init__(self, ip, port, name=None):
        self.components = []
        self.ip = ip
        self.port = port
        thread.start_new_thread(self.__receiver__, (ip,port))

    def __receiver__(self, ip, port):
        HOST = ip                # Symbolic name meaning all available interfaces
        PORT = port              # Arbitrary non-privileged port

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        while 1:
            s.listen(1)
            conn, addr = s.accept()
            data = conn.recv(1024)
            if data:
                self.receive(data)
            else:
                conn.close()

    def register(self, component):
        self.components.append({component.id:{'component':component,
                                              'status':'inactive',
                                              'addres':(self.ip,self.port)}
                               })
    
    def modify_component_status(self, component, status):
        self.components[component.id]['status'] = status
    
    def modify_component_address(self, component, addres):
        self.components[component.id]['addres'] = addres

    def receive(self, msg):
        """receive a message from the external world"""

    def send(self, msg, destin):
        """Send a message to external world"""
        HOST,PORT = self.resolve(destin)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(msg)
        s.close()    

    def resolve(self, destin):
        #TODO!!!
        return destin


if __name__=='__main__':
    import time
    class TestProxy(Proxy):
        def receive(self, msg):
            print 'I received: '+msg

    p = TestProxy('localhost', 5557)
    while 1:
        print 'heartbit'
        time.sleep(2)
