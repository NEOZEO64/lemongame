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
player_positions = [(0, 0), (0, 0), (0, 0)]

def threaded_client(conn, player):
    # conn.send(str.encode(make_pos(player_positions[player])))
    global player_positions
    
    while True:
        # try:
        raw = conn.recv(2048).decode()
        print("[Client {}]: Received: {}".format(player, raw))
        data = raw.split(",")

        # if len(player_positions) < player - 1:
        #     player_positions.append((1, 1))
        
        player_positions[player] = (int(data[0]), int(data[1]))
        print("[Client {}]: Position: X{} Y{}".format(player, player_positions[player][0], player_positions[player][1]))
        
        if not data:
            conn.sendall(str.encode("no!"))
            break
        else:
            reply = ""
            for (i, pos) in enumerate(player_positions):
                if not i == player:
                    reply += "{},{};".format(pos[0], pos[1])
            print("[Client {}]: Sending : ", player, reply)
            conn.sendall(str.encode(reply))
        # except:
        #     print("exception!!!")
        #     break
    global player_count
    player_count -= 1
    player_positions.pop(player)
    print("Lost connection, {} remaining player(s)".format(player_count))
    conn.close()

player_count = 0
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    start_new_thread(threaded_client, (conn, player_count))
    player_count += 1
