#Python progam to run a Cozir Sensor
import serial
import time
import matplotlib.pyplot as plt
import numpy as np
#%matplotlib inline



multiplier = 10 # 20% sensors requires a multiplier

ser = serial.Serial("/dev/ttyUSB0")
print ("Python progam to run a Cozir Sensor\n")
ser.write(str.encode("M 4\r\n"))
#ser.write("M 4\r\n") # set display mode to show only CO2
ser.write(str.encode("K 2\r\n")) # set  operating mode
# K sets the mode,  2 sets streaming instantaneous CO2 output
# \r\n is CR and LF
ser.flushInput()
time.sleep(1)
arrayco2 = []

while True:
    
    tarray= 60#60seg
    tmuestreo=0.2 #t muestreo 0.2seg
    #nmuestras= tarray*tmuestreo
    start= time.time()
    #for i in range(301):
    for i in range(50):
        ser.write(str.encode("Z\r\n"))
        resp = ser.read(10)
        resp = resp[:8]
        fltCo2 = float(resp[2:])
        CO2ppm= fltCo2 * multiplier
        arrayco2.append(CO2ppm)
        #print ("CO2 PPM = ", CO2ppm)
        time.sleep(0.2)#tiempo de muestreo
        #i=i+1
        print(i, CO2ppm)
        
    print(arrayco2, len(arrayco2))
    print("total time executing this loop", time.time() - start)
    break

#xvalues = np.array(range(0,len(arrayco2)))
arrayco2 = np.array(arrayco2)
#print(np.shape(xvalues),np.shape(arrayco2))
plt.figure()
plt.title('CO2 graph')
plt.xlabel('Samples')
plt.ylabel('CO2 level')
plt.ylim(0,500)
plt.plot(arrayco2,'.r')
#plt.plot(xvalues,arrayco2,'.b')
plt.savefig('prueba2.png')
#plt.ion()
    #arrayco2.append(CO2ppm)    
    #print(i)
    #print(arrayco2)
    
    