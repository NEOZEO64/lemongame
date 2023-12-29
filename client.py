import pygame
from pygame.locals import *
import gameUtils

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


class Player:
    def __init__(self,x,y):
        self.x = x
        self.y = y
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
        players[0].y -= 1
    if keys["a"]:
        players[0].x -= 1
    if keys["s"]:
        players[0].y += 1
    if keys["d"]:
        players[0].x += 1
        
    render()

    fpsClock.tick(fps)