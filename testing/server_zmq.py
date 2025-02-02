#
#   Hello World server in Python
#   Binds REP socket to tcp://*:5555
#   Expects b"Hello" from client, replies with b"World"
#

import time
import zmq

context = zmq.Context()
socket_recv = context.socket(zmq.REP)
socket_send = context.socket(zmq.REQ)
socket_recv.bind("tcp://localhost:5555")
socket_send.connect("tcp://localhost:8585")


#  Wait for next request from client
message = socket_recv.recv()
print(f"Received request: {message}")
#  Do some 'work'
time.sleep(1)
#  Send reply back to client
socket_recv.send(b"World")

print("sending message hello")
socket_send.send_string("Hello")

#  Get the reply.
message = socket_send.recv()
print(f"Received reply [ {message} ]")
