# PicoMenu.py by Vincent Mistler (YouMakeTech)
from machine import Pin, PWM, I2C, Timer
from ssd1306 import SSD1306_I2C
import time

SCREEN_WIDTH=128                       # size of the screen
SCREEN_HEIGHT=64

up = Pin(2, Pin.IN, Pin.PULL_UP)
down = Pin(3, Pin.IN, Pin.PULL_UP)
left = Pin(4, Pin.IN, Pin.PULL_UP)
right = Pin(5, Pin.IN, Pin.PULL_UP)
button1 = Pin(6, Pin.IN, Pin.PULL_UP)
button2 = Pin(7, Pin.IN, Pin.PULL_UP)

# Buzzer connected to GP18
buzzer = PWM(Pin(18))

# OLED Screen connected to GP14 (SDA) and GP15 (SCL)
i2c = machine.I2C(1, sda = Pin(14), scl = Pin(15), freq = 400000)
oled = SSD1306_I2C(SCREEN_WIDTH, SCREEN_HEIGHT, i2c)

GAMELIST=["Brickout","Pong","Snake","Space Invaders","Tetris"]

current = 0
gameSelected = -1

while gameSelected < 0:
    oled.fill(0)
    for row in range(0, len(GAMELIST)):
        if row == current:
            oled.fill_rect(0, row*8, SCREEN_WIDTH, 7, 1)
            color = 0
        else:
            color = 1
        
        oled.text(GAMELIST[row], int(SCREEN_WIDTH/2)-int(len(GAMELIST[row])/2 * 8), row*8,color)
    
    oled.show()
    
    time.sleep(0.2)
    
    buttonPressed = False
    
    while not buttonPressed:
        if (down.value() == 0 or right.value() == 0) and current < len(GAMELIST) - 1:
            current += 1
            buttonPressed = True
        elif (up.value() == 0 or left.value() == 0) and current > 0:
            current -= 1
            buttonPressed = True
        elif button1.value()==0 or button2.value()==0:
            buttonPressed = True
            gameSelected = current

    # Make a sound
    buzzer.freq(1000)
    buzzer.duty_u16(2000)
    time.sleep(0.100)
    buzzer.duty_u16(0)
    
# Start the selected game
if gameSelected > 0:
    oled.fill(0)
    oled.show()
