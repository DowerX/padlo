import pygame as pg

pg.init()

clock = pg.time.Clock()

class Lap:
    def __init__(self, w, l, x, y):
        self.x = x
        self.y = y
        self.w = w
        self.l = l
    
    def rect(self, x=0, y=0):
        return (self.x+x, self.y+y, self.l, self.w)

def scale_rect(r, s):
    return [ x*s for i, x in enumerate(r) ]

def offset_poly(p, o):
    return [ (x+o[0],y+o[1]) for (x,y) in p ]

def scale_poly(p,s):
    return [ (x*s,y*s) for (x,y) in p ]

def load_room(path):
    with open(path) as f:
        return [ [float(x), float(y)] for [x, y] in [ l.strip().split() for l in f.readlines() if not "#" in l] ]

screen = pg.display.set_mode([1280,720])

szoba = load_room("szoba.txt")

abs_szoba = []
c = [0,0]
for i in szoba:
    c[0] += i[0]
    c[1] += i[1]
    abs_szoba.append((c[0], c[1]))
szoba = abs_szoba

movement = [0,0]
movementP = [0,0]
offset = [0,0]
offsetP = [0,0]
speed = 40
scale = 1

magassag = 60
szelesseg = 29.5
eltolas = 30

lapok = []
yoffset = 0
for x in range(20):
    yoffset = eltolas * (x%2)
    for y in range(20):
        lapok.append(Lap(magassag, szelesseg, x*szelesseg, y*magassag+yoffset))


pg.mouse.get_rel()
running = True
while running:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()

    if keys[pg.K_w]:
        movement[1] = -1
    elif keys[pg.K_s]:
        movement[1] = 1
    else:
        movement[1] = 0
    
    if keys[pg.K_d]:
        movement[0] = 1
    elif keys[pg.K_a]:
        movement[0] = -1
    else:
        movement[0] = 0

    if keys[pg.K_UP]:
        movementP[1] = -1
    elif keys[pg.K_DOWN]:
        movementP[1] = 1
    else:
        movementP[1] = 0
    
    if keys[pg.K_RIGHT]:
        movementP[0] = 1
    elif keys[pg.K_LEFT]:
        movementP[0] = -1
    else:
        movementP[0] = 0

    if keys[pg.K_KP_PLUS]:
        scale += 0.5/fps
    if keys[pg.K_KP_MINUS]:
        scale -= 0.5/fps

    if keys[pg.K_SPACE]:
        print("Padló eltolása:", offsetP)

    if keys[pg.K_i]:
        offsetP = [ float(x) for x in input("Eltolás: ").split() ]

    mouse = pg.mouse.get_pressed()
    a = pg.mouse.get_rel()
    if mouse[0]:
        offset[0] += a[0]
        offset[1] += a[1]
    elif mouse[2]:
        offsetP[0] += a[0]
        offsetP[1] += a[1]

    fps = max(1, clock.get_fps())

    offset = [offset[0]+(movement[0]*speed/fps), offset[1]+(movement[1]*speed/fps)]
    offsetP = [offsetP[0]+(movementP[0]*speed/fps), offsetP[1]+(movementP[1]*speed/fps)]

    screen.fill((255,255,255))
    pg.draw.polygon(screen, (0,0,255), scale_poly(offset_poly(szoba, offset), scale), 2)
    for l in lapok:
        pg.draw.rect(screen, (161, 161, 161), scale_rect(l.rect(offset[0]+offsetP[0], offset[1]+offsetP[1]), scale), 1)
    pg.display.flip()
    clock.tick(60)

pg.quit()