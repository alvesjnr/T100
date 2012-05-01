# Antonio Ribeiro, UNIFEI - 2012
# T100 simulation framework
# Assyncronous proxy receiver example

import socket
import thread
import time


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
            data = conn.recv(2048)
            if data:
                self.receive(data)
            else:
                conn.close()
