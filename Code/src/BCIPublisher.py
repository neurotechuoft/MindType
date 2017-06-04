import zmq
import random
import sys
import time

port = "5556"
if len(sys.argv) > 1:
    port =  sys.argv[1]
    int(port)

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("udp://*:%s" % port)

while True:
    topic = "Open_BCI"
    messagedata = random.randrange(1, 1000)
    print "%s %d" % (topic, messagedata)
    socket.send("%s %d" % (topic, messagedata))
    time.sleep(1)
