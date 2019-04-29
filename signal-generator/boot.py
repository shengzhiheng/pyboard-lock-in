#boot.py 
#import packages for all python scripts 
import machine, pyb, array, math, lcd160cr, random, utime 

dac = pyb.DAC(2, bits=12) 
dacref = pyb.DAC(1, bits=12) 
lcd = lcd160cr.LCD160CR('X') 

#define the on-board LEDs 
red = pyb.LED(1) 
green = pyb.LED(2) 
yellow = pyb.LED(3) 
blue = pyb.LED(4) 

lcd.set_orient(lcd160cr.LANDSCAPE) 
lcd.erase() 
lcd.set_pos(0, 0) 
lcd.set_text_color(lcd.rgb(255, 255, 255), lcd.rgb(0, 0, 0)) 
lcd.set_pen(lcd.rgb(0, 255, 255), lcd.rgb(0, 0, 0)) 
lcd.set_font(3,0) 
lcd.write('INITIALIZED.\n') 
lcd.set_pos(0, 20) 
lcd.write('Welcome.\n') 

red.on() 
#wait 1000 ms for the switch to be pressed and hold. 
pyb.delay(1000) 
switchvalue = pyb.Switch()() 
#press the switch to activate as storage device 
#leave unpressed to collect data 
#this way the data file will not be affected by windows 
if (switchvalue or lcd.is_touched()): 
#usb mode of storage device 
pyb.usb_mode('CDC+MSC') 
pyb.main('card-reader.py') 
#cardreader.py can be empty 
lcd.erase() 
lcd.set_pos(0,0) 
lcd.write('Cardreader mode') 
else: 
#in this mode, files will not be visible in windows 
pyb.usb_mode('CDC+HID') 
pyb.main('signal-generator.py') 
red.off() 
