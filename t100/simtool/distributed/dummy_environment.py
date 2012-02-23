 # This  script creates a dummy environment that just wait for incomming components
 
if __name__=='__main__':
    ip = sys.argv[1]
    port = sys.argv[2]
    env = Environment(ip,port)
    env.wait_for_action()