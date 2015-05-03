#
# ESE 519 - Final Project
# A Realtime Home Infotainment System
# Team Members: Aditya Deshpande, Nishank Shinde, Cheng Cheng
# game.py
#

import pygame, sys
from pygame.locals import *
import math
import time
from serial import Serial
import re

pygame.init()

windowSurface = pygame.display.set_mode((800,700),0,32)
pygame.display.set_caption("Game")

# Declare colours
BLACK  = (0,0,0)
WHITE  = (255,255,255)
RED    = (255,0,0)
GREEN  = (0,255,0)
BLUE   = (0,0,255)
YELLOW = (255, 255, 0)
GREY   = (20,20,20)


# Initialize display
windowSurface.fill(GREY)

startAngle = 0
endAngle = startAngle + math.pi/4

oldStartAngle = startAngle
oldEndAngle = endAngle

# Ball's initial x-y coordinates
centerx = 400
centery = 150

oldcenterx = centerx
oldcentery = centery

# Velocity of the ball and time interval between successive steps
velocityx = 1
velocityy = 1
dt = 10

pygame.draw.circle(windowSurface, RED, (400, 350), 90, 5)
pygame.draw.circle(windowSurface, RED, (400,350), 330, 5)
pygame.display.update()

# Initialze font for the score
basicFont = pygame.font.SysFont(None, 40)
score = 0


# Returns the distance from the center
def distanceFromCenter(x, y):
  distSq = (x - 400)*(x-400) + (y - 350)*(y-350)
  dist = math.sqrt(distSq)
  return dist

# Reflect the vector about the normal
def reflectVector(vx, vy, cx, cy, N):
  nx = (400-cx) / N
  ny = (350-cy) / N
  
  scalarProd = nx*vx + ny*vy
  vx = vx - 2 * scalarProd * nx
  vy = vy - 2 * scalarProd * ny

  return vx,vy

# Update the score on a hit
def updateScore():
  global basicFont
  global score
  global windowSurface

  score = score + 1
  text = basicFont.render(`score`, True, YELLOW,GREY)
  textRect = text.get_rect()
  textRect.centerx = windowSurface.get_rect().centerx + 300
  textRect.centery = windowSurface.get_rect().centery - 300
  windowSurface.blit(text, textRect)
  
# Return true if the laser has hit the ball
def hit(angle):
  ballAngle = -math.atan2((centery-350), (centerx - 400))
  if ballAngle < 0:
    ballAngle = 2 * math.pi + ballAngle

  angle = angle * 180 / math.pi
  ballAngle = ballAngle * 180 / math.pi
  
  if abs(ballAngle - angle) < 10:
    return True
  else:
    return False
  

flag = 0
oldpx = 0
oldpy = 0
oldqx = 0
oldqy = 0

values = [0,0,0,0,0]
shoot = False

# Main Loop
while True:

  pygame.draw.arc(windowSurface, GREY, [295, 245, 210, 210], oldStartAngle, oldEndAngle,5)
  pygame.draw.arc(windowSurface, GREEN, [295, 245, 210, 210], startAngle, endAngle,5)
  
  pygame.draw.circle(windowSurface, GREY, (oldcenterx, oldcentery), 20, 0)
  pygame.draw.circle(windowSurface, BLUE, (int(centerx), int(centery)), 20, 0)
  pygame.display.update()
  time.sleep(0.01)
  pygame.draw.line(windowSurface, GREY, (int(oldpx), int(oldpy)), (int(oldqx), int(oldqy)), 2)
  
  fgame = open('game.txt','r')
  inStr = fgame.readline()
  fgame.close()
  
  oldval = values[1]
  if (inStr != '' and len(inStr) == 19):
    params = inStr[:19].split(',')
    if (len(params[0]) == 4 and len(params[1]) == 4 and len(params[2]) == 4 and len(params[3]) == 4 and params[0] == '0x13'):  
      print params
      # For Trigger
      if re.match('0x[0-9a-zA-Z]',params[1]):
        try:
          values[1] = int(params[1],16)
        except:
          print "Could not convert to integer"

      # For IMU input
      if re.match('0x[0-9a-zA-Z]', params[2]):
        try:
          values[2] = int(params[2], 16)
        except:
          print "Could not convert to integer"

  # Did the user shoot?
  if (values[1] == 1 and oldval != values[1]):
    shoot = True  
  
  oldcenterx = int(centerx)
  oldcentery = int(centery)
  
  oldStartAngle = startAngle
  oldEndAngle = endAngle
  
  # Reflect the ball if it hits the boundary
  dist = distanceFromCenter(centerx, centery)
  if (dist < 270 and dist > 130):
    flag = 1
  if (dist > 275 or dist < 125):
    if (flag == 1):
      velocityx, velocityy = reflectVector(velocityx, velocityy, centerx, centery, dist)
      flag = 0

  # Update the ball's position
  centerx = oldcenterx + velocityx*dt
  centery = oldcentery + velocityy*dt
  
  #Update the shooting arc's position
  startAngle = startAngle + 0.1
  if (startAngle > 2 * math.pi):
    startAngle = startAngle - 2 * math.pi

  endAngle = startAngle + math.pi/4
  
  # If the user shot, render the  laser and check for a hit  
  if shoot == True:
    print "shoot"
    currentAngle = (startAngle + endAngle) / 2
    

    px = 400 + 105 * math.cos(currentAngle)
    py = 350 - 105 * math.sin(currentAngle)
  
    qx = 400 + 305 * math.cos(currentAngle)
    qy = 350 - 305 * math.sin(currentAngle)
    pygame.draw.line(windowSurface, YELLOW, (int(px), int(py)),(int(qx), int(qy)), 2)
    oldpx = px
    oldpy = py

    oldqx = qx
    oldqy = qy
    
    if hit(currentAngle):
      updateScore()

    shoot = False
    
  
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.quit()
      sys.exit()
    
    if event.type == KEYDOWN:
      # Keyboard press for shooting - for Debugging
      if event.key == K_w:
        currentAngle = (startAngle + endAngle) / 2
        px = 400 + 105 * math.cos(currentAngle)
        py = 350 - 105 * math.sin(currentAngle)

        qx = 400 + 305 * math.cos(currentAngle)
        qy = 350 - 305 * math.sin(currentAngle)

        pygame.draw.line(windowSurface, YELLOW, (int(px), int(py)), (int(qx), int(qy)), 2)
        oldpx = px
        oldpy = py

        oldqx = qx
        oldqy = qy

        if hit(currentAngle):
          updateScore()

        shoot = False

      if event.key == K_a:
        pygame.quit()
        sys.exit()
      
       
