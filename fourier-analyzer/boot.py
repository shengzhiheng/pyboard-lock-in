# boot.py

# import packages for all python scripts
import machine, pyb, array, math, lcd160cr

# define ADC pin
adc = pyb.ADC(machine.Pin('X3', machine.Pin.IN))
lcd = lcd160cr.LCD160CR('X')

# define the on-board LEDs
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
lcd.write('Welcome.')
lcd.set_pos(0, 40)
lcd.write('Touch to read data')

red.on()
# wait 1000 ms for the switch to be pressed and hold.
pyb.delay(1000)
sw = pyb.Switch()()
# press the switch or screnn to activate as storage device
# leave unpressed to collect data
# this way the data file will not be affected by Windows
if (sw or lcd.is_touched()):
    # usb mode of storage device
    pyb.usb_mode('CDC+MSC')
    pyb.main('card-reader.py')
    lcd.erase()
    lcd.set_pos(0,0)
    lcd.write('Cardreader mode')
else:
    # in this mode, files will not be visible in Windows
    pyb.usb_mode('CDC+HID')
    pyb.main('fourier-analyzer.py')

red.off()
