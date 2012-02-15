# Echo server program
import socket
import thread
import time

class Event(object):
    def do(self, text=''):
        print 'Doing!'+text

def print_oi(blah):
	while True:
		print 'oi'
		time.sleep(1)
		
class Proxy(object):

    def __init__(self, ip, port, name=None):
        self.components = []
        thread.start_new_thread(self.__receiver__, (ip,port))


    def __receiver__(self, ip, port):
        HOST = ip                 # Symbolic name meaning all available interfaces
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
        self.components.append({'component':component,
                                'status':'inactive'})

    def receive(self, msg):
        """Overrite to use"""

    def send(self, msg, destin):
        HOST,PORT = self.resolve(destin)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall(msg)
        s.close()    

    def resolve(self, destin):
        pass
    


d = {'d1':Event(), 'd2':Event()}

if __name__=='__main__':
    Proxy(d)