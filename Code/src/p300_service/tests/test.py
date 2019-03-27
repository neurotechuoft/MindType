from socketIO_client import SocketIO

# p300 server running on localhost:8002
socket_client = SocketIO('localhost', 8002)
socket_client.connect()

uuid = 1123
timestamp = 677700
p300 = 1

socket_client.emit("predict", (uuid, timestamp))
socket_client.wait_for_callbacks(seconds=1)
