#
# ESE 519 - Final Project
# Team Members: Aditya Deshpande, Nishank Shinde, Cheng Cheng
# A Real Time Home Infotainment system
# localUI.py
#

import pygame,sys
from pygame.locals import *
from serial import Serial
import time
import urllib2
import re


pygame.init()

windowSurface = pygame.display.set_mode((1500,900),0,32)
pygame.display.set_caption("AHRIS")
clock = pygame.time.Clock()

# Color declarations
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0,255,0)
BLUE  = (0,0, 255)

LIGHT_RED  = (253, 165, 165)
LIGHT_BLUE = (119, 206, 249)
ORANGE     = (249, 158, 119)
DARK_GREEN = (93, 154, 53)
VIOLET = (188, 108, 249)

# Font declarations
basicFont = pygame.font.SysFont("comicsansms", 40)
ahrisFont = pygame.font.SysFont("comicsansms", 50)

centerx = windowSurface.get_rect().centerx
centery = windowSurface.get_rect().centery

# Initialization of the UI
ahrisCenter = (centerx, centery - 400)
tempCenter = (centerx - 500, centery - 300)
humidCenter = (centerx - 250, centery - 300)
lightCenter = (centerx, centery - 200)
noiseCenter = (centerx + 250, centery - 300)
pulseCenter = (centerx + 500, centery - 300)

ahrisText = ahrisFont.render("AHRIS", True, BLACK)
ahrisRect = ahrisText.get_rect()
ahrisRect.centerx = ahrisCenter[0]
ahrisRect.centery = ahrisCenter[1]

tempText = basicFont.render("Temperature", True, WHITE)
tempRect = tempText.get_rect()
tempRect.centerx = tempCenter[0]
tempRect.centery = tempCenter[1] -25

humidText = basicFont.render("Humidity", True, WHITE)
humidRect = humidText.get_rect()
humidRect.centerx = humidCenter[0]
humidRect.centery = humidCenter[1] - 25

lightText = basicFont.render("Light", True, WHITE)
lightRect = lightText.get_rect()
lightRect.centerx = lightCenter[0]
lightRect.centery = lightCenter[1] - 25

noiseText = basicFont.render("Noise", True, WHITE)
noiseRect = noiseText.get_rect()
noiseRect.centerx = noiseCenter[0]
noiseRect.centery = noiseCenter[1] - 25

pulseText = basicFont.render("Pulse rate", True, WHITE)
pulseRect = pulseText.get_rect()
pulseRect.centerx = pulseCenter[0]
pulseRect.centery = pulseCenter[1] - 25

 
windowSurface.fill(WHITE)

pygame.draw.circle(windowSurface, LIGHT_RED, tempCenter, 100,0)
pygame.draw.circle(windowSurface, LIGHT_BLUE, humidCenter, 100, 0)
pygame.draw.circle(windowSurface, ORANGE, lightCenter, 100, 0)
pygame.draw.circle(windowSurface, DARK_GREEN, noiseCenter, 100, 0)
pygame.draw.circle(windowSurface, VIOLET, pulseCenter, 100, 0)


windowSurface.blit(ahrisText, ahrisRect)
windowSurface.blit(tempText, tempRect)
windowSurface.blit(humidText, humidRect)
windowSurface.blit(lightText, lightRect)
windowSurface.blit(noiseText, noiseRect)
windowSurface.blit(pulseText, pulseRect)

pygame.display.update()


# Update the displayed temperature on the UI
def updateTemperature(t):
  global basicFont
  global tempCenter
  global windowSurface

  tempValText = basicFont.render(str(t), True, WHITE, LIGHT_RED)
  tempValRect = tempValText.get_rect()
  tempValRect.centerx = tempCenter[0]
  tempValRect.centery = tempCenter[1] + 25
  windowSurface.blit(tempValText, tempValRect)

# Update the displayed humidity on the UI
def updateHumidity(h):
  global basicFont
  global humidCenter
  global windowSurface

  humidValText = basicFont.render(str(h), True, WHITE, LIGHT_BLUE)
  humidValRect = humidValText.get_rect()
  humidValRect.centerx = humidCenter[0]
  humidValRect.centery = humidCenter[1] + 25
  windowSurface.blit(humidValText, humidValRect)

# Update the displayed Light level on the UI
def updateLight(l):
  global basicFont
  global lightCenter
  global windowSurface

  lightValText = basicFont.render(str(l), True, WHITE, ORANGE)
  lightValRect = lightValText.get_rect()
  lightValRect.centerx = lightCenter[0]
  lightValRect.centery = lightCenter[1] + 25
  windowSurface.blit(lightValText, lightValRect)


# Update the displayed noise Level on the UI
def updateNoise(n):
  global basicFont
  global noiseCenter
  global windowSurface

  noiseValText = basicFont.render(str(n), True, WHITE, DARK_GREEN)
  noiseValRect = noiseValText.get_rect()
  noiseValRect.centerx = noiseCenter[0]
  noiseValRect.centery = noiseCenter[1] + 25
  windowSurface.blit(noiseValText, noiseValRect)

# Update the displayed Pulse rate on the UI
def updatePulse(p):
  global basicFont
  global pulseCenter
  global windowSurface

  pulseValText = basicFont.render(str(p), True, WHITE, VIOLET)
  pulseValRect = pulseValText.get_rect()
  pulseValRect.centerx = pulseCenter[0]
  pulseValRect.centery = pulseCenter[1] + 25
  windowSurface.blit(pulseValText, pulseValRect)


values = [0,0,0,0,0]

# Continuously read and update values in a loop  
while True:
  fparam = open('parameters.txt','r')
  inStr = fparam.readline() 
  
  fanLevel = ''
  lightLevel = ''
  if (inStr != '' and len(inStr) >= 29):
    params = inStr[:29].split(',')
    print params
    if (len(params[0]) == 4 and len(params[1]) == 4 and len(params[2]) == 4 and len(params[3]) == 4 and len(params[4]) == 4 and params[0] == '0x12'):
      for i in range(5):
        if i < len(params) and re.match('0x[0-9a-zA-Z][0-9a-zA-Z]', params[i+1]):
          try:
            values[i] = int(params[i+1],16)
          except:
            continue



      updateTemperature(values[0])
      updateNoise(values[1])
      updateLight(values[2])
      updateHumidity(values[3])
      updatePulse(values[4])
    
      pygame.display.update()

  time.sleep(0.2)
 
   
  for event in pygame.event.get():
    if event.type == QUIT or event.type == KEYDOWN:
      fparam.close()
      pygame.quit()
      sys.exit() 
