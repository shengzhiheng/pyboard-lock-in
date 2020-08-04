import pyb
from machine import Pin #import libraries

red = pyb.LED(1) #Four LED on the pyboard
green = pyb.LED(2)
yellow = pyb.LED(3) #yellow and blue LED have adjustable intensity
blue = pyb.LED(4)
sw = pyb.Switch() #USR switch on the board
acc = pyb.Accel() #built-in accelerometer

red.on()    #turn on or off red LED
red.off()

while True:
    pyb.delay(100) #sleep function, input is in milliseconds
    blue.toggle() #change the state of the LED

p = Pin('X5', Pin.OUT) #declare pin X5 to be output, applicable to all pins
dac = pyb.DAC(p, bits = 8) #create a DAC object from X5
# values range from 0-255 for 8 bits, and 0-4095 for 12 bits
dac.write(255) #max voltage for this DAC
dac.write(0) #min voltage for the DAC
