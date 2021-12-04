# PicoGame.py by YouMakeTech
# A class to easily write games for the Raspberry Pi Pico RetroGaming System
from machine import Pin, PWM, I2C, Timer
from ssd1306 import SSD1306_I2C
from framebuf import FrameBuffer, MONO_HLSB
import time
import random

class PicoGame:
    def __init__(self):
        self.SCREEN_WIDTH = 128
        self.SCREEN_HEIGHT = 64
        self.up_ = Pin(2, Pin.IN, Pin.PULL_UP)
        self.down_ = Pin(3, Pin.IN, Pin.PULL_UP)
        self.left_ = Pin(4, Pin.IN, Pin.PULL_UP)
        self.right_ = Pin(5, Pin.IN, Pin.PULL_UP)
        self.button1_ = Pin(6, Pin.IN, Pin.PULL_UP)
        self.button2_ = Pin(7, Pin.IN, Pin.PULL_UP)
        self.buzzer = PWM(Pin(18))
        
        self.i2c = I2C(1, sda=Pin(14), scl=Pin(15), freq=400000)
        self.oled = SSD1306_I2C(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.i2c)
        
        self.fb=[] # Array of FrameBuffer objects for sprites
        self.w=[]
        self.h=[]
    
    def show(self):
        self.oled.show()
        
    def fill(self, color = 1):
        self.oled.fill(color)

    def pixel(self, x,y,color = 1):
        self.oled.pixel(x, y, color)
        
    def text(self, s, x, y, color = 1):
        self.oled.text(s, x, y, color)
        
    def centerText(self, s, color = 1):
        x = int(self.SCREEN_WIDTH/2)- int(len(s)/2 * 8)
        y = int(self.SCREEN_HEIGHT/2) - 8
        self.text(s, x, y, color)
        
    def topRightCornerText(self, s, color = 1):
        x = self.SCREEN_WIDTH - int(len(s) * 8)
        y = 0
        self.text(s, x, y, color)
        
    def line(self, x1, y1, x2, y2, color = 1):
        self.oled.line(x1, y1, x2, y2, color)
    
    def rect(self, x, y, w, h, color = 1):
        self.oled.rect(x, y, w, h, color)
        
    def fillRect(self, x, y, w, h, color = 1):
        self.oled.fill_rect(x, y, w, h, color)
        
    def addSprite(self, buffer, w, h):
        fb = FrameBuffer(buffer, w, h, MONO_HLSB)
        self.fb.append(fb)
        self.w.append(w)
        self.h.append(h)
       
    def sprite(self, n, x, y):
        self.oled.blit(self.fb[n], x, y)
        
    def spriteWidth(self,n):
        return self.w[n]
    
    def spriteHeight(self,n):
        return self.h[n]
        
    def buttonUp(self):
        return self.up_.value()==0
    
    def buttonDown(self):
        return self.down_.value()==0
    
    def buttonLeft(self):
        return self.left_.value()==0
    
    def buttonRight(self):
        return self.right_.value()==0
    
    def button1(self):
        return self.button1_.value()==0
    
    def button2(self):
        return self.button2_.value()==0
    
    def anyButton(self):
        # returns True if any button is pressed
        buttonPressed=False
        if self.buttonUp():
            buttonPressed = True
        if self.buttonDown():
            buttonPressed = True
        if self.buttonLeft():
            buttonPressed = True
        if self.buttonRight():
            buttonPressed = True
        if self.button1():
            buttonPressed = True
        if self.button2():
            buttonPressed = True
        return buttonPressed
    
    def sound(self, freq, duty_u16 = 2000):
        # Make a sound at the selected frequency in Hz
        if freq>0:
            self.buzzer.freq(freq)
            self.buzzer.duty_u16(duty_u16)
        else:
            self.buzzer.duty_u16(0)
   