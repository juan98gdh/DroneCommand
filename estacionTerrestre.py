'Chat Room Connection - Client-To-Client'
import threading
import socket
import signal
import sys
# host = '127.0.0.1'
# port = 8787


def signal_handler(sig, frame):
    print('\n[+] Exit with succcess...')
    with open('directions.txt', 'r') as fr:
        lines = fr.readlines()
        with open('directions.txt', 'w') as fw:
            for line in lines:
                if not line.__contains__(f"et{selfId}"):
                    fw.write(line)
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

drone_dict = {}
selfId = input("ET id > ")
host = input("host > ")
port = int(input("port > "))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

f = open("directions.txt", "a")
f.write(f"et{selfId}:{host}:{port}\n")
f.close()


# def broadcast(message):
#     for drone in drones:
#         drone.send(message)

# Function to handle clients'connections


def handle_drone(drone):
    while True:
        try:
            msg = drone.recv(1024)
            if not msg:
                drone.close()
                for key, value in drone_dict.items():
                    if drone == value:
                        eraseKey = key
                        print(f"Closing connection to drone {key}")
                del drone_dict[eraseKey]
                break
        except ():
            break
# Main function to receive the clients connection


def send():
    while True:
        print('Connected Drones (id):\n')
        for k in drone_dict.keys():
            print('[+] ' + k)
        drone_id = input("\ndrone id > ")
        if drone_id == 'r' or drone_id == 'reload':
            print(chr(27) + "[2J")
        elif drone_id not in drone_dict.keys():
            print("\n Id invalido\n")
        else:
            drone_dict[drone_id].send(input("Comando > ").encode('utf-8'))
            drone_response = drone_dict[drone_id].recv(4096)
            if not drone_response:
                drone_dict[drone_id].close()
                print(f"[-] Drone {drone_id} Disconnected (connection closed)")
                del drone_dict[drone_id]
            else:
                print('\n\t[+] ' + drone_response.decode('utf-8') + '\n')


def receive():
    while True:
        drone, address = server.accept()
        drone_id = drone.recv(1024)
        drone_dict[drone_id.decode('utf-8')] = drone
        did = drone_id.decode('utf - 8')
        print(f'\nThe drone: {did} connected')
        # broadcast(f'{alias} has connected to the chat room'.encode('utf-8'))
        # thread = threading.Thread(target=handle_drone, args=(drone,))
        # thread.start()


print(f'[+] et{selfId} listening on {host}:{port} ...')
recv = threading.Thread(target=receive)
recv.start()

send_drone = threading.Thread(target=send)
send_drone.start()
