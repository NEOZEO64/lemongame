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

try:
    s.bind((ip, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

# player_positions[player_id] = (X, Y)
player_positions = []

def threaded_client(conn, player):
    global player_positions
    
    while True:
        raw = conn.recv(2048).decode()
        
        if raw:
            print("[Client {}]: Received: {}".format(player, raw))
            data = raw.split(",")

            while len(player_positions) <= player:
                player_positions.append(None)
        
            player_positions[player] = (int(data[0]), int(data[1]))
            print("[Client {}]: Position: X{} Y{}".format(player, player_positions[player][0], player_positions[player][1]))
        
            reply = ""
            for (i, pos) in enumerate(player_positions):
                if not i == player:
                    reply += "{},{};".format(pos[0], pos[1])
            print("[Client {}]: Sending: {}".format(player, reply))
            if reply == "":
                conn.sendall(str.encode("no!"))
            else:
                conn.sendall(str.encode(reply))
    global player_count
    player_count -= 1
    player_positions[player] = None
    print("Lost connection, {} remaining player(s)".format(player_count))
    conn.close()

player_count = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, player_count))
    player_count += 1
