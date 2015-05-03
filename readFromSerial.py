#
# ESE 519 - Final Project
# A Real Time Home Infotainment System
# Team Members: Aditya Deshpande, Nishank Shinde, Cheng Cheng
# readFromSerial.py
# Daemon to collect data sent to the Pi from different nodes
#

import pygame,sys
from pygame.locals import *
from serial import Serial
import time
import thread
import urllib2
import re


actions  = ["update_temperature", "update_noise_level", "update_light_intensity", "update_humidity", "update_pulse_rate"]
url      = "https://apricot-pudding-2161.herokuapp.com"
user     = "Aditya"


# Initialization of Parameters and the seria port
serialPort = 0
fanLevel = 0
lightLevel = 0

# Open a serial port to receive data from the mbed
def openPort():
  global serialPort
  serialPort = Serial("/dev/ttyACM0", 9600, timeout=2, writeTimeout=0)
  if (serialPort.isOpen() == False):
    serialPort.open()
  return serialPort


# Update the parameter corresponding to given index
def updateParameters(paramIdx, val):
  global fanLevel
  global lightLevel
  command = url + "/" + actions[paramIdx] + "/" + user + "/" + `val`
  try:
    reply = urllib2.urlopen(command).read()
    fanElement   = re.search('(?<=<div id="FanLevel">)[0-9]+(?=</div>)', reply)
    lightElement = re.search('(?<=<div id="LightLevel">)[0-9]+(?=</div>)', reply)
    fanLevel     = fanElement.group(0)
    lightLevel   = lightElement.group(0)

  except:
    print "Error: could not update parameters"


# Start of the program

openPort()
serialPort.flushInput()
values = [0,0,0,0,0]

SENS_LEN = 29           # Length of the data from the sensor node
GLOV_LEN = 19           # Length of the data from the glove

SENS_ADDR = '0x12'      # Source address of the sensor node
GLOV_ADDR = '0x13'      # Source address of the glove

# Continuosly poll the serial port for data
# Validate the data
# Update the parameters and the game/art relevant data  
while True:

  inStr = serialPort.read(serialPort.inWaiting())
  
  # Data from the sensor node
  if (inStr != '' and len(inStr) >= SENS_LEN):
    params = inStr[:SENS_LEN].split(',')
    
    if (len(params[0]) == 4 and len(params[1]) == 4 and len(params[2]) == 4 and len(params[3]) == 4 and len(params[4]) == 4 and params[0] == SENS_ADDR):
      f1 = open('parameters.txt','w')
      f1.truncate()
      f1.write(inStr[:SENS_LEN])
      f1.close()
      #print params
      for i in range(5):
        if i < len(params) and re.match('0x[0-9a-zA-Z][0-9a-zA-Z]', params[i+1]):
          try:
            values[i] = int(params[i+1],16)
          except:
            continue

      try:
        for i in range(len(actions)):
          # Update Data on the server
          thread.start_new_thread(updateParameters, (i, values[i]))
          
      except:
        continue
      
      # Relay fan and light control values from the web server to the communication module
      val = int(fanLevel)*10 + int(lightLevel)
      serialPort.write(chr(val))
      serialPort.flush()
  
  # Data from the glove  
  elif (inStr != '' and len(inStr) == GLOV_LEN):
    params = inStr[:GLOV_LEN].split(',')
    if (len(params[0]) == 4 and len(params[1]) == 4 and len(params[2]) == 4 and len(params[3]) == 4 and params[0] == GLOV_ADDR):
      f2 = open('game.txt','w')
      f2.truncate()
      f2.write(inStr[:GLOV_LEN])
      f2.close()
          
  
  time.sleep(.05)
   
  