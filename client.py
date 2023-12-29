import pygame
from pygame.locals import *
import gameUtils


# Pygame starten
pygame.init()

# Fenster erstellen
windowSurface = pygame.display.set_mode((1024, 600), pygame.FULLSCREEN)

# Bild laden (load image) mit Breite 60
shipPic = gameUtils.loadIMG("Res/body_03.png", 60)



shipWidth = shipPic.get_width()
shipHeight = shipPic.get_height()
print(shipHeight)


# Farben in Variablen speichern
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Hintergrund weiß zeichnen
windowSurface.fill(WHITE)

# Roten Kreis zeichen (Position: X=300, Y=50 mit Radius 20)
pygame.draw.circle(windowSurface, RED, (0, 0), 500, 0)

# Blauen Kreis zeichen (Position: X=300, Y=50 mit Radius 20)
pygame.draw.circle(windowSurface, BLUE, (300, 50), 20, 0)

# Bild zeichnen! (An Position X=60, Y=200)
windowSurface.blit(shipPic, (60,200))

# Alles gezeichnete tatsächlich anzeigen
pygame.display.update()

run = True

# Spiel-Schleife
while run:
    # Informationen (Events) über das Pygame-Fenster abfragen
    for event in pygame.event.get():
        # Wenn die Information gerade ein beenden-Event ist:
        if event.type == QUIT:
            run = False
