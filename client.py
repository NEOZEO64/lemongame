import pygame
from pygame.locals import *
import gameUtils
import random

pygame.init()
windowSurface = pygame.display.set_mode((500, 500)) # create window

lemonPic = gameUtils.loadIMG("./Lemon.png", 128) # width 128

fps = 15
fpsClock = pygame.time.Clock()



BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

speed = 3 # speed for lemon moving


def getRandomID():
    return str(random.randrage(1000,10000))

class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.id = getRandomID()
    def show(self):
        # draw lemon!
        windowSurface.blit(lemonPic, (self.x,self.y))

players = []

players.append(Player(50,50))



def render():
    windowSurface.fill(RED)

    for i in range(len(players)):
        players[i].show()

    # put buffer to screen
    pygame.display.update()



# Spiel-Schleife
run = True

while run:
    # Informationen (Events) über das Pygame-Fenster abfragen
    for event in pygame.event.get():
        # Wenn die Information gerade ein beenden-Event ist:
        if event.type == QUIT:
            run = False

    keys = gameUtils.getKeys()
    if keys["w"]:
        players[0].y -= speed
    if keys["a"]:
        players[0].x -= speed
    if keys["s"]:
        players[0].y += speed
    if keys["d"]:
        players[0].x += speed
        
    render()

    fpsClock.tick(fps)