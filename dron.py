import threading
import socket
import time
import sys
import signal


def signal_handler(sig, frame):
    print('\n[+] Exit with succcess...')
    sys.exit(0)


with open('directions.txt', 'r') as dir:
    lines = dir.readlines()
    print('\nConnecction list:\n')
    for line in lines:
        info = line.split(':')
        print(f"[+] {info[0]}\n\tHost: {info[1]}\n\tPort: {info[2]}")

print('\n')

id = input('Drone id > ')
host = input("host > ")
port = int(input("port > "))

drone = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
drone.connect((host, port))
signal.signal(signal.SIGINT, signal_handler)

# Dos hilos, uno para revibir mensajes y otro para mandar
global status
global telemetry


def drone_receive():
    global status
    global telemetry
    while True:
        try:
            message = drone.recv(1024).decode('utf-8')
            if message == "LINK":
                drone.send("link complete".encode('utf-8'))
                # send_thread = threading.Thread(target=drone_send)
                # send_thread.start()
                print(message)
            elif message == "UNLINK":
                drone.send(f"drone {id} Unlink complete".encode('utf-8'))
            elif message == "CONNECT":
                drone.send(f"drone {id} Connected".encode('utf-8'))
            elif message == "DISCONNECT":
                drone.send(f"drone {id} Disconnected".encode('utf-8'))
            elif message == "FLY":
                status = "FLYING"
                drone.send(f"drone {id} started flying".encode('utf-8'))
            elif message == "LAND":
                status = "LANDED"
                drone.send(f"drone {id} landing".encode('utf-8'))
            elif message == "TELEMETRY":
                drone.send(telemetry.encode('utf-8'))
            else:
                print(message)
        except ():
            print('Error!')
            drone.close()
            break


drone.sendall(id.encode('utf-8'))

receive_thread = threading.Thread(target=drone_receive)
receive_thread.start()

status = 'LANDED'
batery = 100
while True:
    time.sleep(4)
    if status == 'FLYING':
        batery -= 1
    message = f'TELEMETRY dron {id}: \n\t[+] Batery: {batery}%\n\t[+] Status: {status}'
    telemetry = message
    print(message)
