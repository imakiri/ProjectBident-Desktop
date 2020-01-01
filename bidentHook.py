import sys
import os
import time
import math
import subprocess
from Pyro4 import *
from Pyro4.core import *
from Pyro4.naming import *
        
if __name__ == '__main__':
    os.system(f"python {os.path.dirname(os.path.realpath(__file__))}\\bidentServer.py")
    # try:
    #     s = Proxy("PYRO:Bident@localhost:4560")
    #     s.launch()
    # except ConnectionError:
    #     os.system(f"python {os.path.dirname(os.path.realpath(__file__))}\\bidentCore.py")
    #     time.sleep(1)
    #     s = Proxy("PYRO:Bident@localhost:4560")
    #     s.launch()
