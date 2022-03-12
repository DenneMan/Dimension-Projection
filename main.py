import pygame, sys
from matrix import *

screen = pygame.display.set_mode(SCREENSIZE)

size = 1

def UnitCube(x, y, z):
    tmp_list = []
    for i in range(2):
        for j in range(2):
            for k in range(2):
                tmp_list.append(vec3(i - 0.5 + x, j - 0.5 + y, k - 0.5 + z))
    return tmp_list

def UnitTeseract():
    tmp_list = []
    for x in range(2):
        for y in range(2):
            for z in range(2):
                for w in range(2):
                    tmp_list.append(vec4(x - 0.5, y - 0.5, z - 0.5, w - 0.5) * size)
    return tmp_list

def UnitPenteract():
    tmp_list = []
    for x in range(2):
        for y in range(2):
            for z in range(2):
                for w in range(2):
                    for v in range(2):
                        tmp_list.append(vec5(x - 0.5, y - 0.5, z - 0.5, w - 0.5, v - 0.5))
    return tmp_list

world = []

world.append(UnitTeseract())

rotation = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    mpos = pygame.mouse.get_pos()
    mpos = (mpos[0]/SCREENSIZE[0]*720, mpos[1]/SCREENSIZE[1]*180-90)
    if mpos[1] >= 90:
        mpos = (mpos[0], 90)
    if mpos[1] <= -90:
        mpos = (mpos[0], -90)

    screen.fill((0, 0, 0))
    for obj in world:
        for vertexA in obj:
            rotatedA = rotate(Z, W, vertexA, rotation)
            #rotatedA = rotate(X, V, vertexA, rotation)
            rotatedA = rotate(X, Z, rotatedA, -mpos[0])
            rotatedA = rotate(Y, Z, rotatedA, -mpos[1])
            rotatedA.draw(screen)
            for vertexB in obj:
                if(dist(vertexA, vertexB) == size):
                    rotatedB = rotate(Z, W, vertexB, rotation)
                    #rotatedB = rotate(X, V, vertexB, rotation)
                    rotatedB = rotate(X, Z, rotatedB, -mpos[0])
                    rotatedB = rotate(Y, Z, rotatedB, -mpos[1])
                    connect(rotatedA, rotatedB, screen)

    rotation += 0.3

    pygame.display.flip()
