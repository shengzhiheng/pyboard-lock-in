#datalogger.py
#reads data from pin X3 (defined in boot.py)

#select magnitude and phase mode or two channels mode

lcd.erase()
lcd.set_pos(25,40)
lcd.write('Mag')
lcd.set_pos(25,60)
lcd.write('and')
lcd.set_pos(25,80)
lcd.write('Phase')
lcd.set_pos(110,50)
lcd.write('Two')
lcd.set_pos(110,70)
lcd.write('Chs')
lcd.line(80,0,80,120)

chs=False
touch = lcd.get_touch()
while(touch[0]==0):
touch = lcd.get_touch()
pyb.delay(50)
touch = lcd.get_touch()

if (int(touch[1])>=80):
chs=True

#opens file to store the magnitude of all iterations
result = open('/sd/Average.csv','w')
result.write('Channel1, Channel2, Magnitude\n')
value = 0 #helper variable for analyzing the magnitude
rep = 20 #no of iterations the program will run to produce a reliable average
mag = 0
phs = 0
ch1 = 0
ch2 = 0

length = 1000 #length of the data array, 1000 for faster analysis
f = 1000 #frequency of the lock-in signal, 1000Hz
rate = 10 #points per period
lcd.erase()
lcd.set_pos(0,0)
lcd.write('Collecting')
lcd.line(0,125,200,125)
lcd.line(0,58,0,125)
for j in range(rep):

lcd.set_pos(110, 0)
#lcd.write('Iteration ')
lcd.write(str(j+1))
lcd.write('/')
lcd.write(str(rep))

if chs:
 lcd.set_pos(0, 20)
 lcd.write('Ch1: ')
 lcd.write(str(round(ch1,4)))

 lcd.set_pos(0, 40)
 lcd.write('Ch2: ')
 lcd.write(str(round(ch2,4)))
 
else:
 lcd.set_pos(0, 20)
 lcd.write('Magnitude: ')
 lcd.write(str(round(mag,4)))

 lcd.set_pos(0, 40)
 lcd.write('Phase: ')
 lcd.write(str(round(phs,4)))

#create buffer arrays and timer
green.on()
buf = array.array('i', (0 for i in range(length)))
#timer will collect data at frequency of f*rate
timer = pyb.Timer(6, freq = (f * rate))
green.off()

#read data from ADC pins into buffer
blue.on()
adc.read_timed(buf,timer)

#normalization of the collected buffer array
#normalized array has mean of 0 and amplitude of 1
mean = math.ceil(sum(buf) / length)
buf = [(buf[i] - mean) for i in range(length)]
top = max(buf)
bottom = min(buf)
amp = max(top,-bottom)
buf =[buf[i] / amp for i in range(length)]
blue.off()

#define sine function with phase
def sine(phase, i): 
 return math.sin(2 * math.pi * i / rate + phase)

#define reference function
def ref(i):
 return sine(0, i)
#mix the original and reference signals
def mixed(i):
 return buf[i] * ref(i)

#define another reference function in quadrature
def reforth(i):
 return sine(math.pi / 2, i)
#mix original and quadrature reference signal
def mixedorth(i):
 return buf[i] * reforth(i)

#start processing the buffer array
yellow.on()
signalsum = 0
signalorthsum = 0
#log the buffer array, as well as reference and mixed signals
for i in range(length):
 #calculate each value in the for loop before writing into file
 #to avoid too much storage in memory
 reftemp = ref(i)
 mixedtemp = mixed(i)
 reforthtemp = reforth(i)
 mixedorthtemp = mixedorth(i)
 signalsum += mixedtemp
 signalorthsum += mixedorthtemp
 #write all above values into the file

#delete buffer to reduce memory usage
del buf

#calculate the average strength in each channel
#as a form of extreme low pass filter
signalavg = signalsum / length
signalorthavg = signalorthsum / length
#pythagorean sum of the two channels
mag = math.sqrt(signalavg**2 + signalorthavg**2)
phs = math.atan(signalavg / signalorthavg)*180/math.pi
ch1 = signalavg
ch2 = signalorthavg
result.write('{},{},{}\n'.format(signalavg,signalorthavg,mag))
yellow.off()
value += mag

#draw four pixels
lcd.dot(round(j*160/rep) + 5,round((1-mag)*120))
lcd.dot(round(j*160/rep) + 6,round((1-mag)*120))
lcd.dot(round(j*160/rep) + 5,round((1-mag)*120)+1)
lcd.dot(round(j*160/rep) + 6,round((1-mag)*120)+1)


#calculate a final average of magnitude of all repetitions
result.write('\n ,Average,{}'.format(value/rep))
result.close()

lcd.rect_interior(0, 0, 200, 60)
lcd.set_pos(0,0)
lcd.write("Finished")
lcd.set_pos(0,20)
lcd.write('Average: ')
lcd.write(str(round(value/rep,3)))
lcd.set_pos(0,40)
lcd.write('Press RST')
lcd.set_pen(lcd.rgb(0, 255, 0), lcd.rgb(0, 255, 0))
lcd.line(0,round((1-value/rep)*120)+1,200,round((1-value/rep)*120)+1)
