# signal-generator.py

log = open('/sd/random.csv','w') 
log.write('Signal,Noise,Combined\n') 

# create a buffer containing a sine-wave, using half-word samples 
# upper limit set to 1800 to avoid saturation on the DAC pin 
ref = array.array('H', 1800 + int(1799 * math.sin(2 * math.pi * i / 128)) for i in range(128)) 
buf = array.array('H', 0 for i in range(128)) 

#signal: from 0 to 1, noise from 0 to 1-signal 
signal = 0 
noise = 1 
for i in range(len(buf)): 
r = random.random() 
buf[i] = int(1800*(signal+noise) + (ref[i]-1800) * signal + (r-0.5) * 3599 * noise) 
log.write('{},{},{}\n'.format(ref[i]*signal/3600,r*noise,buf[i]/3600)) 
log.close() 

f = 1000 
# DAC 2 means pin X6 
lcd.erase() 
lcd.set_pos(0,0) 
lcd.write('Outputting.\n') 
lcd.set_pos(0,20) 
lcd.write('Signal = '+str(signal)) 
lcd.set_pos(0,40) 
lcd.write('Noise = '+str(noise)) 

dac.write_timed(buf, f*len(buf), mode=pyb.DAC.CIRCULAR) 
dacref.write_timed(ref, f*len(ref), mode=pyb.DAC.CIRCULAR) 
