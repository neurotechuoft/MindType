import sys
import zmq

port = "5556"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

if len(sys.argv) > 2:
    port1 = sys.argv[2]
    int(port1)

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)

print "Collecting updates from weather server..."
socket.connect("udp://localhost:%s" % port)

if len(sys.argv) > 2:
    socket.connect("udp://localhost:%s" % port1)

topicfilter = "Open_BCI"
socket.setsockopt(zmq.SUBSCRIBE, topicfilter)

data_list = []
while True:
    data = socket.recv()
    topic, messagedata = data.split()
    data_list.append(int(messagedata))
    