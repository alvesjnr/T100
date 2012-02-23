 # This  script creates a dummy environment that just wait for incomming components
from t100.simtool.distributed_env import Environment
import sys 

if __name__=='__main__':
    ip = sys.argv[1]
    port = int(sys.argv[2])
    env = Environment(ip,port)
    env.loop()