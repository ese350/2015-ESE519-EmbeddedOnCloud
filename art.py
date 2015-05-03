#
# ESE 519 - Final Project
# A Real time Home Infotainment system
# Team members: Aditya Deshpande, Cheng Cheng, Nishank Shinde
# art.py
#

import pygame
from pygame.locals import *
from serial import Serial
import re
import Queue
import time

# Initialize the art module's display
pygame.init()

artScreen = pygame.display.set_mode((800,800),0,32)
pygame.display.set_caption("Art Module")

GREY  = (55,55,55)
WHITE = (255,255,255)

colors = ((255,0,0), (0,255,0), (0,0,255), (255, 125, 0), (0,125, 255), (125, 0, 255))
colorIdx = 0

artScreen.fill(GREY)

done = False
colorChange = False
clock = pygame.time.Clock()

# Queue for the Moving average filter
xVals = [0,0,0,0,0,0,0,0]
yVals = [0,0,0,0,0,0,0,0]


values = [0,0,0,0]
preVal = [400,400]
currVal = [0,0]
pointerColor = WHITE

while not done:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      done = True
    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
      artScreen.fill((GREY))

  f1 = open('game.txt','r')
  inStr = f1.readline()
  f1.close()
  
  if (inStr != '' and len(inStr) >= 19):
    params = inStr[:19].split(',')
    if (len(params[0]) == 4 and len(params[1]) == 4 and len(params[2]) == 4 and len(params[3]) == 4 and params[0] == '0x13'):

      if re.match('0x[0-9a-zA-Z]',params[1]):
        try:
          values[1] = int(params[1],16)
        except:
          print "Error: converting values[1] to int"

      if re.match('0x[0-9a-zA-Z]',params[2]):
        try:
          values[2] = int(params[2],16)
          xVals.append(values[2])
          xVals.pop(0)
        except:
          print "Error: converting values[2] to int"

      if re.match('0x[0-9a-zA-Z]',params[3]):
        try:
          values[3] = int(params[3],16)
          yVals.append(values[3])
          yVals.pop(0)
        except:
          print "Error: converting values[3] to int"


  # Does the user want to draw. Does the user want to change color?
  draw = False
  if (values[1] >= 1):
    if (values[1] == 2):
      if (colorChange ==  False):
        colorIdx = (colorIdx + 1) % 6
        colorChange = True
    else:
      colorChange = False
     
    color =  colors[colorIdx]
    draw = True 
  
        
  print "x: %d | y: %d" %(4 * values[2],4 * values[3])
  
  x_val = (xVals[-1] * 0.8 + xVals[-2] * 0.7 + xVals[-3] * 0.5 + xVals[-4] * 0.4 + xVals[-5] * 0.3 + xVals[-6] * 0.2) / (0.8 + 0.7 + 0.5 + 0.4 + 0.3 + 0.2)
  y_val = (yVals[-1] * 0.8 + yVals[-2] * 0.7 + yVals[-3] * 0.5 + yVals[-4] * 0.4 + yVals[-5] * 0.3 + yVals[-6] * 0.2) / (0.8 + 0.7 + 0.5 + 0.4 + 0.3 + 0.2)
  currVal[0] = int(800 - (4 * x_val))
  currVal[1] = int(800 - (4 * y_val))  
  
  # Correct the pixel corresponding to the pointer's previous position to its original colour
  try:      
    pygame.draw.circle(artScreen, originalColor, (preVal[0], preVal[1]),1,0)
  except:
    print "Error: undoing pointer"

  # If the user has signaled to draw             
  if draw == True:
    pygame.draw.circle(artScreen, color, (currVal[0], currVal[1]), 15, 0)
  
  # Housekeeping to get the original colour at the pointer's position      
  try:
    pixColor = artScreen.get_at((currVal[0], currVal[1]))
    originalColor = (pixColor[0], pixColor[1], pixColor[2])
  except:
    print "Error: getting original color"
  
  # Draw the pointer 
  pygame.draw.circle(artScreen, pointerColor, (currVal[0], currVal[1]), 1, 0)
  if draw == True:
    pygame.draw.line(artScreen, color, (preVal[0],preVal[1]), (currVal[0], currVal[1]), 30)
  preVal[0] =  currVal[0]
  preVal[1] = currVal[1]
  pygame.display.update()
  clock.tick(60)
  time.sleep(0.2)
