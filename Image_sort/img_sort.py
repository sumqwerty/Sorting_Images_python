import cv2 as cv
import pygame as pg
import numpy as np
import random
from os import path

pg.init()

pixsz = 4

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

data_dir = path.join(path.dirname(__file__),'data')
img = cv.imread(path.join(data_dir,"OpnS.png"), 1)
HEIGHT, WIDTH, CHNL = img.shape

gameDisplay = pg.display.set_mode((WIDTH,HEIGHT))

singleAxis = False
shfAxis = 'Y'


objlist = []
Xval = []
Yval = []

################################################################SORTING##########################################################################

def refill(): 
    gameDisplay.fill((255,233,35))
    alocateValues()
    draw() 
    pg.display.update() 
    #pg.time.delay(20)

def mergesort(array, l, r):
    mid = (l+r)//2
    if l<r:
        mergesort(array,l,mid)
        mergesort(array,mid+1,r)
        merge(array,l,mid,mid+1,r)

def merge(array, x1, y1, x2, y2): 
    i = x1 
    j = x2 
    temp =[] 
    pg.event.pump() 
    while i<= y1 and j<= y2:
        refill()
        if array[i]<array[j]:
            temp.append(array[i]) 
            i+= 1
        else: 
            temp.append(array[j]) 
            j+= 1
    while i<= y1:
        refill()
        temp.append(array[i]) 
        i+= 1
    while j<= y2:
        refill()
        temp.append(array[j])
        j+= 1
    j = 0	

    for i in range(x1, y2 + 1): 
        pg.event.pump() 
        array[i]= temp[j] 
        j+= 1
        refill()

#################################################################################################################################################


class Pix:
    def __init__(self, xpos_, ypos_, pixelsz_, color_):
        self.xpos = xpos_
        self.ypos = ypos_
        self.color = color_
        self.pixelsz = pixelsz_

    def setPos(self, xpos_, ypos_):
        self.xpos = xpos_
        self.ypos = ypos_

    def setCol(self,color_):   
        self.color = color_
    
    def drw(self):
        pg.draw.rect(gameDisplay, self.color, (self.xpos, self.ypos, self.pixelsz, self.pixelsz))
        #pg.draw.circle(gameDisplay, self.color, (self.xpos, self.ypos), int(self.pixelsz/2))

def setup():
    global pixsz, arr_clr
    
    for i in range(0, WIDTH, pixsz):
        Xval.append(i)

    for i in range(0, HEIGHT, pixsz):
        Yval.append(i)

    arr_clr =[(0, 204, 102)]*len(Xval)

    for x in range(0, len(Xval)):
        for y in range(0, len(Yval)):
            col = tuple(np.flipud(img[Yval[y],Xval[x]]))
            obj = Pix(Xval[x],Yval[y],pixsz,col)
            objlist.append(obj)
            #pg.draw.rect(gameDisplay, col, (Xval[x],Yval[y],pixsz,pixsz))


def alocateValues():
    xp = 0
    yp = 0
    for obj in objlist:
        obj.setPos(Xval[xp],Yval[yp])
        yp += 1
        if(yp >= len(Yval)):
            yp = 0
            xp += 1


def jumbleX():
    global singleAxis, shfAxis
    shfAxis = 'X'
    singleAxis = True
    random.shuffle(Xval)
    alocateValues()

def jumbleY():
    global singleAxis, shfAxis
    shfAxis = 'Y'
    singleAxis = True
    random.shuffle(Yval)
    alocateValues()
    
def sorting():
    Xval.sort()
    Yval.sort()
    alocateValues()

def shuffle():
    global singleAxis
    singleAxis = False
    random.shuffle(Xval)
    random.shuffle(Yval)
    alocateValues()

def draw():
    for obj in objlist:
        obj.drw()


def main():
    global pixsz
    
    running = True
    while running:
        #print(singleAxis)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_j:
                    print("shuffle")
                    shuffle()

                elif event.key == pg.K_m: ## to sort visually
                    if not singleAxis:
                        #print("1")
                        if WIDTH < HEIGHT:
                            mergesort(Xval, 0, len(Xval)-1)
                            mergesort(Yval, 0, len(Yval)-1)
                        else:
                            mergesort(Yval, 0, len(Yval)-1)
                            mergesort(Xval, 0, len(Xval)-1)
                    elif shfAxis == 'Y':
                        #print("2")
                        mergesort(Yval, 0, len(Yval)-1)
                    else:
                        #print("3")
                        mergesort(Xval, 0, len(Xval)-1)
                        
                        
                elif event.key == pg.K_s: ## to sort non visually 
                    sorting()
                    
                elif event.key == pg.K_x: ## jumbling X axis
                    jumbleX()

                elif event.key == pg.K_y: ## jumbling Y axis 
                    jumbleY()

        gameDisplay.fill(BLACK)

        #print(len(Xval))
        
        draw()
            
        pg.display.update()

        
##        for x in range(0, len(Xval)):
##            for y in range(0, len(Yval)):
##                col = tuple(np.flipud(img[Yval[y],Xval[x]]))
##                pg.draw.rect(gameDisplay, col, (Xval[x],Yval[y],pixsz,pixsz))

        
setup()
main()
