from proxy import Proxy

import sys

class Chat(Proxy):

    def receive(self, msg):
        print '\rhe: ' + msg
    
    def connect(self, port):
        self.his_port = port

    def run(self):
        while True:
            msg = raw_input('you: ')
            self.send(msg,('localhost', self.his_port))



if __name__=='__main__':
    
    ip = sys.argv[1]
    port = int(sys.argv[2])

    c = Chat(ip,port)

    his_port = input('#')

    c.connect(his_port)
    c.run()


