# Python client
# written on 29.12.2023 on Chaos Communication Congress 37c3
import sys, socket, pygame, gameUtils, random, threading

# get hostname and port from command line
if len(sys.argv) <= 2 or sys.argv[1] == "--help":
    print("Syntax: python client.py <server ip> <port>")
    exit()
hostname = sys.argv[1]
port = int(sys.argv[2])

print("Connecting to {}:{}".format(hostname, port))

# game configs
#velocity = 3
velX = 0
velY = 0
acceleration = 1
friction = 0.95

fps = 30 # frames per second
width = 500
height = 500
playerWidth = 64
playerHeight = 64

x = random.randrange(0, width-playerWidth)  # start position
y = random.randrange(0, height-playerHeight)

# create pygame window
win = pygame.display.set_mode((width, height)) # width / height
lemonPic = gameUtils.loadIMG("../img/Lemon.png", playerWidth, playerHeight)
clock = pygame.time.Clock()
otherPlayers = [] # contains tuples (<x>,<y>) of other player positons
run = True

class Explosion:
    ws = [ # widths
        80 # type 0
    ]
    
    animations = []

    tempAnimation = []
    for i in range(1,9):
        tempAnimation.append(gameUtils.loadIMG("../img/Explosion_{}.png".format(i), ws[0]))
    animations.append(tempAnimation)

    numbers = [len(animation) for animation in animations] # animation pic length

    hs = [i[0].get_height() for i in animations]# heights

    objs = []

    def __init__(self,x,y, type):
        self.cx = x # center
        self.cy = y
        self.type = type
        self.x = self.cx-Explosion.ws[self.type]/2
        self.y = self.cy-Explosion.hs[self.type]/2
        self.speed = 0.5
        self.state = 0
        
    def move(self): # returns if animation done
        self.state += self.speed

        if self.state >= Explosion.numbers[self.type]:
            return True
        return False
        
    def show(self):
        win.blit(self.animations[self.type][int(self.state)], (self.x, self.y))
        #window.blit(self.animations[self.type][int(self.state)], (self.x, self.y))


def getOtherPlayers():
    global otherPlayers, run

    # connect to server with specified hostname
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(3)
    try:
        client.connect((hostname, port))
        
        client.send(str.encode("{},{}".format(int(x), int(y))))
        print("Joined, message:", client.recv(2048).decode())
    except: # if no connection just quit
        print("Connection refused")
        run = False
    

    while run:
        try: 
            client.send(str.encode("{},{}".format(int(x), int(y)))) # send client position...
            msg = client.recv(2048).decode() # to get server response

            nowPlayers = []
            if msg != "you are alone": # if there are players
                coordsTup = msg[:-1].split(";") # then split player coordinates
                if coordsTup != ['']: 
                    for tup in coordsTup:
                        tup = tup.split(",")
                        nowPlayers.append((int(tup[0]), int(tup[1])))
            for i in range(len(nowPlayers)-len(otherPlayers)):
                Explosion.objs.append(Explosion(nowPlayers[i][0]+playerWidth/2,nowPlayers[i][1]+playerHeight/2,0)) # 0 for type
            if len(nowPlayers) != len(otherPlayers):
                print(otherPlayers)
            otherPlayers = nowPlayers
        except socket.error as e:
            print(e)
            run = False

otherPlayerThread = threading.Thread(target=getOtherPlayers)
otherPlayerThread.start()

while run:
    # move player client on key presses
    pygame.event.get()
    keys = pygame.key.get_pressed() 
    if keys[pygame.K_LEFT]:
        velX -= acceleration
    if keys[pygame.K_RIGHT]:
        velX += acceleration
    if keys[pygame.K_UP]:
        velY -= acceleration
    if keys[pygame.K_DOWN]:
        velY += acceleration

    velX *= friction
    velY *= friction

    x += velX
    y += velY

    

    # quit game by move out of window
    if x < -playerWidth or x > width or y < -playerHeight or y > height:
        run = False

    # handle explosions
    i = 0
    while i < len(Explosion.objs):
        if Explosion.objs[i].move() == True:
            del Explosion.objs[i]
        else:
            i += 1

    # RENDER
    win.fill((140,100,255)) # draw background white
    for i in range(len(otherPlayers)):
        win.blit(lemonPic, otherPlayers[i]) # draw other players
    win.blit(lemonPic, (x,y)) # draw player

    for e in Explosion.objs:
        e.show()

    pygame.display.update()
    clock.tick(fps) # for 30 fps

pygame.quit()
sys.exit()
