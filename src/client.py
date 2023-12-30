# Python client
# written on 29.12.2023 on Chaos Communication Congress 37c3
import sys, socket, pygame, gameUtils, random

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

x = random.randrange(0, width-playerWidth)  # start position
y = random.randrange(0, height-playerHeight)

# connect to server with specified hostname
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((hostname, port))
    print("Start socket")
    client.send(str.encode("{},{}".format(x, y)))
    print("Message on join:", client.recv(2048).decode())
except: # if no connection just quit
    print("No connection")
    sys.exit()
print("Joined server")

# create pygame window
win = pygame.display.set_mode((width, height)) # width / height
lemonPic = gameUtils.loadIMG("../img/Lemon.png", playerWidth, playerHeight)
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

    # quit game by move out of window
    if x < -playerWidth or x > width or y < -playerHeight or y > height:
        run = False

    win.fill((255,100,100)) # draw background white
    win.blit(lemonPic, (x,y)) # draw player

    # managing other players
    try:
        client.send(str.encode("{},{}".format(x, y))) # send client position...
        msg = client.recv(2048).decode() # to get server response
        
        if msg != "no!": # if there are players
            coordsTup = msg[:-1].split(";") # then split player coordinates
            if coordsTup != ['']: 
                for tup in coordsTup:
                    print(tup)
                    tup = tup.split(",")
                    win.blit(lemonPic, (int(tup[0]), int(tup[1])))
    except socket.error as e:
        print(e)

    pygame.display.update()
    clock.tick(fps) # for 30 fps

pygame.quit()