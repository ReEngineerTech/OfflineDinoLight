#!/usr/bin/env python3
# offlineDinoMain V0.5
# Author: Cameron Edmonds - Re: Engineer Tech channel on YouTube
# Date Revised: 12/19/2020
# Functional code that runs the offlineDino Smart Light on the rpi

import time
from rpi_ws281x import *
import argparse
from adafruit_debouncer import Debouncer
import os
import RPi.GPIO as GPIO
import board
import digitalio


GPIO.setmode(GPIO.BCM) 
 
# LED strip configuration:
LED_COUNT      = 69      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10     # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53 

# Buttons configuration: 
TOP_BTN_PIN        = 23      # GPIO pin connected to the the upper most button.
BOTTOM_BTN_PIN     = 24      # GPIO pin connected to the the lower most button.
GPIO.setup(TOP_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
GPIO.setup(BOTTOM_BTN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
switchTop = Debouncer(digitalio.DigitalInOut(board.D19))  #debounce for top button
switchBtm = Debouncer(digitalio.DigitalInOut(board.D20))  #debounce for bottom button


# Define functions for buttons
def setFlagTrue(channel):
    print('Flag Set to:')
    global changeMode 
    changeMode = True
    print(changeMode)

            
def escCheck():
    """Only move on if button is pushed."""
    global changeMode
    changeMode = False
    while True:
        if changeMode == True:
            changeMode = False
            break

# Define functions which set LEDs in solid states.
def colorSet(strip, color):
    """Set color across display."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)       
    strip.show()

def colorSetBody(strip, color):
    """Set color across body portion of display."""
    for i in range(strip.numPixels()-3):
        strip.setPixelColor(i, color)
    strip.show()

def colorSetEye(strip, color):
    """Set color across eye portion of display."""
    strip.setPixelColor(66, color)
    strip.setPixelColor(67, color)
    strip.setPixelColor(68, color)    
    strip.show()

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, wheel((i+j) % 255))
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
                

# Add function to execute when the button pressed event happens  
def Shutdown(channel):
    print('Shutdown')
    colorWipe(strip, Color(0, 0, 0))  # OFF wipe  
    time.sleep(3)
    os.system("sudo shutdown -h now")

#add button watchers    
GPIO.add_event_detect(TOP_BTN_PIN, GPIO.RISING, callback = Shutdown, bouncetime = 2000)
GPIO.add_event_detect(BOTTOM_BTN_PIN, GPIO.RISING, callback = setFlagTrue, bouncetime = 500)  

   
# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()
 
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
 
    print('Press Ctrl-C to quit.')
    
    changeMode = False

    try:
        while True: #Main Program loop
            while not changeMode: #Demo mode
                print('Color wipe animations.')
                colorWipe(strip, Color(255, 0, 0))  # Red wipe
                print(changeMode)
                if changeMode == True:
                    break
                colorWipe(strip, Color(0, 255, 0))  # Blue wipe
                print(changeMode)
                if changeMode == True:
                    break
                colorWipe(strip, Color(0, 0, 255))  # Green wipe
                print(changeMode)
                if changeMode == True:
                    break
                print('Theater chase animations.')
                theaterChase(strip, Color(127, 127, 127))  # White theater chase
                print(changeMode)
                if changeMode == True:
                    break
                theaterChase(strip, Color(127,   0,   0))  # Red theater chase
                print(changeMode)
                if changeMode == True:
                    break
                theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
                print(changeMode)
                if changeMode == True:
                    break
                print('Rainbow animations.')
                rainbow(strip)
                print(changeMode)
                if changeMode == True:
                    break
                rainbowCycle(strip)
                print(changeMode)
                if changeMode == True:
                    break
                theaterChaseRainbow(strip)


            print('Set lights to white.')
            colorSet(strip, Color(255, 255, 255))  # White set
            escCheck()    
            
            print('Set lights to red.')
            colorSet(strip, Color(255, 0, 0))  # Red set
            escCheck()    

            print('Set lights to yellow.')
            colorSet(strip, Color(255, 255, 0))  # Yellow set
            escCheck()

            print('Set lights to blue.')
            colorSet(strip, Color(0, 255, 0))  # Blue set
            escCheck()

            print('Set lights to teal.')
            colorSet(strip, Color(0, 255, 255))  # Teal set
            escCheck()

            print('Set lights to green.')
            colorSet(strip, Color(0, 0, 255))  # Green set
            escCheck()

            print('Set lights to pink.')
            colorSet(strip, Color(255, 0, 255))  # Pink set
            escCheck()


            print('Entering smart monitor mode...')
            changeMode = False
            print('Set lights to red.')
            colorSet(strip, Color(255, 0, 0))  # Red set
            ret = 1
            while ret:
                ret = os.system("ping -c 1 -W 3 192.168.1.1") # check ping to router
                time.sleep(2)
            print('Router detected')
            colorSet(strip, Color(255, 255, 0))  # Yellow set
            ret = 1
            while ret:
                ret = os.system("ping -c 1 -W 3 8.8.8.8") # check ping to DNS
                time.sleep(2)
            print('DNS detected')
            colorSet(strip, Color(0, 255, 0))  # Green set
            
            while not changeMode:
                retRouter = os.system("ping -c 1 -W 3 192.168.1.1") # check ping to router
                retDNS = os.system("ping -c 1 -W 3 8.8.8.8") # check ping to DNS
                
                print('dns ping ret =')
                print(retDNS)
                print('router ping ret =')
                print(retRouter)
                
                #set lights
                if retRouter != 0:
                    print('Router connection LOST')
                    colorSet(strip, Color(255, 0, 0))  # Red set
                elif retDNS != 0:
                    print('DNS connection LOST')
                    colorSet(strip, Color(255, 255, 0))  # Yellow set
                else:
                    colorSet(strip, Color(0, 255, 0))  # Green set
                
                print('Waiting 2 Min before next ping')
                for i in range(0,120): #wait for button press or 2 minutes to pass
                    if changeMode == True:
                        break
                    time.sleep(1)

                if changeMode == True:
                    changeMode = False
                    break

            print('Set lights to OFF.')
            colorSet(strip, Color(0, 0, 0))  # set to off
            escCheck()
            
    except KeyboardInterrupt:
        print('keeb interrupt')
        colorWipe(strip, Color(0,0,0), 10)