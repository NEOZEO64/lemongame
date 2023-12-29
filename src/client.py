# Python client
# written on 29.12.2023 on Chaos Communication Congress 37c3
import sys, socket, pygame, gameUtils

# try connecting to server, otherwise quit
if len(sys.argv) <= 2 or sys.argv[1] == "--help":
    print("Syntax: python client.py <server ip> <port>")
    exit()
hostname = sys.argv[1]
port = int(sys.argv[2])

# game configs
velocity = 3
fps = 30 # frames per second
width = 500
height = 500
playerWidth = 64
playerHeight = 64

# connect to server with specified hostname
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((hostname, port))
    pos = client.recv(2048).decode().split(",")
    (x,y) = (int(pos[0]), int(pos[1])) # get start position on connection
except: # if no connection just quit
    print("No connection")
    sys.exit()

# create pygame window
win = pygame.display.set_mode((width, height)) # width / height
lemonPic = gameUtils.loadIMG("../img/Lemon.png", playerWidth, playerHeight) # width 128  
clock = pygame.time.Clock()
run = True

while run:
    # move player client on key presses
    pygame.event.get()
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT]:
        x -= velocity
    if keys[pygame.K_RIGHT]:
        x += velocity
    if keys[pygame.K_UP]:
        y -= velocity
    if keys[pygame.K_DOWN]:
        y += velocity

    # quit game by going out of window
    if x < -playerWidth or x > width or y < -playerHeight or y > height:
        run = False

    win.fill((255,255,255))
    win.blit(lemonPic, (x,y))

    # managing other players
    try:
        client.send(str.encode("{},{}".format(x, y))) # send client position...
        coordsTup = client.recv(2048).decode().split(";") # to get server response
        for tup in coordsTup:
            tup = tup.split(",")
            win.blit(lemonPic, (int(tup[0], int(tup[1]))))
    except socket.error as e:
        print(e)

    pygame.display.update()
    clock.tick(fps) # for 30 fps

pygame.quit()
socket.close()