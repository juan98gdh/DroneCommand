#
#   Hello World client in Python
#   Connects REQ socket to tcp://localhost:5555
#   Sends "Hello" to server, expects "World" back
#
import time
import zmq

context = zmq.Context()

#  Socket to talk to server
socket_send = context.socket(zmq.REQ)
socket_recv = context.socket(zmq.REP)
socket_send.connect("tcp://localhost:5555")
socket_recv.bind("tcp://localhost:8585")

#  Do 10 requests, waiting each time for a response
print("sending message hello")
socket_send.send_string("Hello")

#  Get the reply.
message = socket_send.recv()
print(f"Received reply [ {message} ]")

#  Wait for next request from client
message = socket_recv.recv()
print(f"Received request: {message}")
#  Do some 'work'
time.sleep(1)
#  Send reply back to client
socket_recv.send(b"World")
