#datalogger.py
#reads data from pin X3 (defined in boot.py)

#opens file to store the magnitude of all iterations
result = open('/sd/Spectrum.csv','w')
result.write('Frequency, Number, Magnitude, Phase\n')
num = 12 #no of frequencies to sample
rep = 5 #no of iterations for each of the frequencies
avg = 0
mag = 0
phs = 0

length = 1000 #length of the data array, 1000 for faster analysis
start = 200 #start frequency of the lock-in signal, 1000Hz
step = 200 #frequency step
rate = 10 #points per period
lcd.erase()
lcd.set_pos(0,0)
lcd.write('Repetitions: ')
lcd.line(0,125,200,125)
lcd.line(0,58,0,125)

for j in range(num):
        f = start + j * step
        
        lcd.set_pos(0,20)
        lcd.write('Frequency: ')
        lcd.write(str(start + (j-1) * step))
        lcd.set_pos(0,40)
        lcd.write('Magnitude: ')
        lcd.write(str(round(avg,4)))

        #perform multiple repetitions for this frequency to generate
        value = 0 #helper variable to calculate mean

        for k in range(rep):
                lcd.set_pos(110,0)
                lcd.write(str(j * rep + k + 1))

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

                #delete buffer to reduce memory usage
                del buf

                #calculate the average strength in each channel as a form of extreme low pass filter
                signalavg = signalsum / length
                signalorthavg = signalorthsum / length
                #pythagorean sum of the two channels
                mag = math.sqrt(signalavg**2 + signalorthavg**2)
                phs = math.atan(signalavg / signalorthavg)*180/math.pi
                ch1 = signalavg
                ch2 = signalorthavg
                result.write('{},{},{},{}\n'.format(f,k,mag,phs))
                yellow.off()
                value += mag
                #write all above values into the file

        avg = value / rep
        result.write('{},Average,{}\n'.format(f,avg))
        #draw four pixels
        lcd.dot(round(j*160/num) + 5,round((1.2-avg)*100))
        lcd.dot(round(j*160/num) + 6,round((1.2-avg)*100))
        lcd.dot(round(j*160/num) + 5,round((1.2-avg)*100)+1)
        lcd.dot(round(j*160/num) + 6,round((1.2-avg)*100)+1)

#calculate a final average of magnitude of all repetitions
result.close()

lcd.rect_interior(0, 0, 200, 55)
lcd.set_pos(0,0)
lcd.write("Finished")
lcd.set_pos(0,20)
lcd.write('Freq: ')
lcd.write(str(start))
lcd.write('-')
lcd.write(str(start + num * step))
lcd.set_pos(0,40)
lcd.write('Step: ')
lcd.write(str(step))
