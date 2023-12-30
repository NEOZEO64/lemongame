import socket
from _thread import *
import sys


if len(sys.argv) <= 1 or sys.argv[1] == "--help":
    print("Syntax: python server.py <server ip> <port>")
    exit()
    
ip = sys.argv[1]
port = int(sys.argv[2])
print("Server: {}\nPort: {}".format(ip, port))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((ip, port))
s.listen(2)
print("Server started, waiting for a connection")

# player_positions[player_id] = (X, Y)
player_positions = []

def threaded_client(conn, player):
    global player_positions

    while len(player_positions) <= player:
        player_positions.append(None)
    
    while True:
        rx = conn.recv(2048).decode()
        
        if rx:
            print("[Client {}] RX: \"{}\"".format(player, rx))
            player_pos = rx.split(",")
        
            player_positions[player] = (int(player_pos[0]), int(player_pos[1]))
        
            reply = ""
            for (i, pos) in enumerate(player_positions):
                if not i == player and pos != None:
                    reply += "{},{};".format(pos[0], pos[1])

            if reply == "":
                reply = "you are alone"

            conn.sendall(str.encode(reply))
            print("[Client {}] TX: \"{}\"".format(player, reply))
        else:
            break
    global player_count
    player_count -= 1
    player_positions[player] = None
    print("[Player {}] Lost connection, {} remaining player(s)".format(player, player_count))
    conn.close()

player_count = 0
while True:
    conn, addr = s.accept()
    print("Connected to ", addr)

    start_new_thread(threaded_client, (conn, player_count))
    player_count += 1
