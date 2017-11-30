# A single script that spawns a simple http.server, and
# a zeromq-based server that relays data to a websocket
# that the client browser can connect to.

import os
from subprocess import Popen, PIPE, STDOUT

cwd = os.path.dirname(os.path.realpath(__file__))
print('Current working directory : {}'.format(cwd))
p1 = Popen(['python3 -m http.server'],
           stdout=None, stderr=None,
           shell=True, cwd=cwd)
p2 = Popen('python3 server.py',
           stdout=None, stderr=None,
           shell=True, cwd=cwd)

try:
    p1.wait()
    p2.wait()
except KeyboardInterrupt:
    p1.terminate()
    p2.terminate()
