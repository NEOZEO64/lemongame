import pygame
import socket
import sys

hostname = "151.217.116.19"
velocity = 3

# create Pygame Window
win = pygame.display.set_mode((500, 500)) # width / height

# connect to server with specified hostname
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((hostname, 5555)) # using port 55555
    pos = client.recv(2048).decode().split(",")
    startPos = (int(pos[0]),int(pos[1])) # get start position on first connection
except: # if no connection just quit
    print("No connection")
    sys.exit()


class Player():
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
    def show(self):
        # just draw rectangle 
        pygame.draw.rect(win, (self.color), (self.x,self.y,50,50))


p = Player(startPos[0],startPos[1],(0,0,255)) # make own player blue
p2 = Player(0,0,(255,0,0)) # other player is red
clock = pygame.time.Clock()
run = True

while run:
    # EVENTS
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # check if window should be closed
            run = False

    keys = pygame.key.get_pressed() # move player client on key presses
    if keys[pygame.K_LEFT]:
        p.x -= velocity
    if keys[pygame.K_RIGHT]:
        p.x += velocity
    if keys[pygame.K_UP]:
        p.y -= velocity
    if keys[pygame.K_DOWN]:
        p.y += velocity

    # OTHER PLAYERS
    try:
        client.send(str.encode("{},{}".format(p.x, p.y))) # send client position...
        response = client.recv(2048).decode().split(",") # to get server response..
        (p2.x, p2.y) = (int(response[0]), int(response[1])) # and update player 2 position
    except socket.error as e:
        print(e)

    # RENDER
    win.fill((255,255,255))
    p.show()
    p2.show()
    pygame.display.update()
    clock.tick(60)

pygame.quit()