#!/usr/bin/python
print " corbin's game"

import pygame
import player
import wall
import cat
import goal
import mazegenerator
import time
import random
from pgu import gui
from gui7 import ColorDialog
from pygame.locals import *

timeout = 1000 # milliseconds
delay=8000
winwidth=1535
winheight=1007
num_walls=4
screen = pygame.display.set_mode((winwidth, winheight),SWSURFACE)
done = False
x=725
y=725
speed=48
all_sprites_list=None
player1=None
goal1=None
cat1=None
themap=None
initialized=False
level = 1
costs={}


pygame.key.set_repeat(200,200)
clock = pygame.time.Clock()
timer = pygame.time.get_ticks

class Question(gui.table.Table):
  def __init__(self,tmr,delay,**params):
    params.setdefault('cls','dialog')
    gui.table.Table.__init__(self,**params)
    self.timer=tmr
    self.delay=delay
    self.popuptime=tmr()+self.delay
    self.opened=False
    a=random.randint(4,10)
    b=random.randint(2,10)
    self.tr()
    self.td(gui.Label("%dX%d"%(a,b)),align=-1,cls=self.cls+'.bar')
    #clos = gui.button.Icon(self.cls+".bar.close")
    #self.td(clos,align=1,cls=self.cls+'.bar')
    self.tr()
    self.w = gui.Input(value='',size=18)
    self.w.connect("activate", self.checkAnswer, (self.w,a,b))
    self.td(self.w)

  def open(self,w,x,y):
    gui.table.Table.open(self,w,x,y)
    self.opened=True
    self.focus()
    self.focus(self.w)

  def checkAnswer(self,v):
    try:
      if int(v[0].value)==v[1]*v[2]:
        self.popuptime=self.timer()+self.delay
        self.opened=False
        self.close()
    except:
      pass
    v[0].value =""

app=gui.App()
c = gui.Container(align=-1,valign=-1)
app.init(c)

d = Question(timer,delay)

#pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('Comic Sans MS', 30)

def getMove(pos,parent,goal,cost=0):
  global costs,themap
  #print "try",pos
  #time.sleep(1)
  if pos not in costs:
    costs[pos]=cost,parent
  elif cost<costs[pos][0]:
    costs[pos]=cost,parent
  else: return False

  next=[]
  if pos[0]+1>=0 and pos[0]+1<len(themap) and themap[pos[0]+1][pos[1]]==0:
    next.append((pos[0]+1,pos[1]))
  if pos[1]+1>=0 and pos[1]+1<len(themap[0]) and themap[pos[0]][pos[1]+1]==0:
    next.append((pos[0],pos[1]+1))
  if pos[0]-1>=0 and pos[0]-1<len(themap) and themap[pos[0]-1][pos[1]]==0:
    next.append((pos[0]-1,pos[1]))
  if pos[1]-1>=0 and pos[1]-1<len(themap[0]) and themap[pos[0]][pos[1]-1]==0:
    next.append((pos[0],pos[1]-1))
  for p in next:
    getMove(p,pos,goal,cost+1)

def setup():
    global all_sprites_list,initialized
    all_sprites_list = pygame.sprite.Group()
    setMaze()
    setGoal()
    setPlayer()
    setCat()
    initialized=True

def setMaze():
    global themap,timeout,delay
    themap=mazegenerator.Generate(winwidth/48,winheight/48)
    # remove exactly 10 walls
    timeout = (30-level)*50
    delay=(30-level)*1000
    for _ in range(30-level):
        xx,yy=random.randint(1,len(themap[0])-2),random.randint(1,len(themap)-2)
        while(themap[yy][xx]==0):
            xx,yy=random.randint(1,len(themap[0])-2),random.randint(1,len(themap)-2)
        themap[yy][xx]=0
    for y in range(len(themap)):
      for x in range(len(themap[y])):
        if themap[y][x]==1: all_sprites_list.add(wall.wall(x,y))

def setPlayer():
    global x,y,themap,all_sprites_list,player1
    x,y=random.randint(0,len(themap[0])-1),random.randint(0,len(themap)-1)
    while(themap[y][x]==1):
        x,y=random.randint(0,len(themap[0])-1),random.randint(0,len(themap)-1)
    player1=player.player(x,y)
    all_sprites_list.add(player1)
    print "mouse",x,y

def setGoal():
    global gx,gy,themap,all_sprites_list,goal1
    gx,gy=random.randint(0,len(themap[0])-1),random.randint(0,len(themap)-1)
    while(themap[gy][gx]==1):
        gx,gy=random.randint(0,len(themap[0])-1),random.randint(0,len(themap)-1)
    goal1=goal.goal(gx,gy)
    all_sprites_list.add(goal1)

def setCat():
    global cx,cy,themap,all_sprites_list,cat1
    cx,cy=random.randint(0,len(themap[0])-1),random.randint(0,len(themap)-1)
    while(themap[cy][cx]==1):
        cx,cy=random.randint(0,len(themap[0])-1),random.randint(0,len(themap)-1)
    cat1=cat.cat(cx,cy)
    all_sprites_list.add(cat1)

deadline = timer() + timeout

lev = myfont.render('Level: %d'%level, False, (0, 0, 0))
while not done:
  if not d.opened and d.popuptime < timer():
    d = Question(timer,delay)
    d.open()
  
  if timer() > deadline:
    deadline=timer()+timeout
    costs={}
    getMove((cy,cx),None,(y,x))
    parent=costs[(y,x)][1]

    while parent != (cy,cx):
      if (cy,cx)==costs[parent][1]:
        break
      else: parent=costs[parent][1]
    cat1.rect.x=parent[1]*speed
    cat1.rect.y=parent[0]*speed
    cx,cy=cat1.coords()
    x,y=player1.coords()
    if cx==x and cy==y:
      break

  if not initialized:
    setup()
    lev = myfont.render('Level: %d'%level, False, (0, 0, 0))
  for event in pygame.event.get():
    p=player1.coords()
    g=goal1.coords()
    c=cat1.coords()
    

    if event.type == pygame.QUIT:
      done = True
    elif not d.opened:
      if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
        if themap[p[1]-1][p[0]] == 0:
          player1.rect.y=player1.rect.y-speed
      if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
        if themap[p[1]+1][p[0]] == 0:
          player1.rect.y=player1.rect.y+speed
      if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
        if themap[p[1]][p[0]-1] == 0:
          player1.rect.x=player1.rect.x-speed
      if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
        if themap[p[1]][p[0]+1] == 0:
          player1.rect.x=player1.rect.x+speed
      if p[0]==g[0] and g[1]==p[1]:
        initialized=False
        level+=1
    else:
      app.event(event)
  
  screen.fill((0, 0, 0))
  all_sprites_list.draw(screen)
  app.paint()
  screen.blit(lev,(0,0))
  pygame.display.flip()

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
  screen.fill((255, 0, 0))
  pygame.display.flip()
