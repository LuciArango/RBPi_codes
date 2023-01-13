import calculopetco2
import breathingConditions
import RPi.GPIO as GPIO
import numpy
import serial.tools.list_ports
#import busio
import time
import serial
#import adafruit_sgp30
#import matplotlib.pyplot as plt

## Control de variables para lectura de sensor de CO2
multiplier = 10 # 20% sensors requires a multiplier
ports = []
#micro = serial.Serial()
#serco2 = serial.Serial()
#serco2 = serial.Serial("/dev/ttyUSB0")
co2port = 'ttyUSB0'
GPIO.setmode(GPIO.BOARD)
#GPIO.setup(23, GPIO.OUT)
GPIO.setwarnings(False)#led de prueba
#ser = serial.Serial("/dev/ttyUSB0")
print ("Python progam to run a Cozir Sensor\n")

## Variables de frecuencia de verificacion de estado del paciente
#t1 = 10*600 ##verificacion cada 10 minutos
#t1 = 60 #tiempo de prueba

def Available():
    global starT
    global end_T
    global comm1
    starT = time.process_time()
    for port in serial.tools.list_ports.comports():
        ports.append(port.name)
    print(ports)
    #print([port.device for port in serial.tools.list_ports.comports()])
    print ('listo:')
    if co2port in ports:
        #serco2 = serial.Serial("/dev/ttyUSB0")
        print ("ok")
        #micro = serial.Serial(port='/dev/ttyACM0',baudrate = 230400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
        GPIO.output(17, GPIO.HIGH)#led de prueba de conexi[on serial
        time.sleep(1)
        GPIO.output(17, GPIO.LOW)
        serco2.write(str.encode("M 4\r\n"))
        #ser.write("M 4\r\n") # set display mode to show only CO2
        serco2.write(str.encode("K 2\r\n")) # set  operating mode
        # K sets the mode,  2 sets streaming instantaneous CO2 output
        # \r\n is CR and LF
        serco2.flushInput()
        time.sleep(1)
        #time.sleep(1)
        #comm1.write("rgb,__red\n".encode('utf-8'))
        #time.sleep(4)
        end_T = time.process_time()#time.time_ns()
        print("Time taken", end_T-starT, "ns")
        return True
    
    else:
        print ("Nope")
        end_T = time.process_time()
        return False

def Temporizador(Tempo, t1):
              
    if  Tempo > t1:
        Tempo_fin = time.process_time()
        print('Tiempo de muestreo', Tempo_fin-Tempo_inicio)
        #GPIO.output(23, GPIO.HIGH)
        #time.sleep(1)
        #GPIO.output(23, GPIO.LOW)
        
        
        #Tempo = 0
        return True
        
    else:
        Tempo_inicio = time.process_time() 
        Tempo = Tempo+1
        time.sleep(1)
        return False
       
    
while True:
          
###Leemos el sensor de CO2
    """
    arrayco2 = []
    if Available():
        startco2= time.time()
        #for i in range(301):
        for i in range(50):
            serco2.write(str.encode("Z\r\n"))
            resp = serco2.read(10)
            resp = resp[:8]
            fltCo2 = float(resp[2:])
            CO2ppm= fltCo2 * multiplier
            arrayco2.append(CO2ppm)
            #print ("CO2 PPM = ", CO2ppm)
            time.sleep(0.2)#tiempo de muestreo
            #i=i+1
            print(i, CO2ppm)
        print("total time executing this loop", time.time() - startco2)
                
    else:
        print("Verificar comunicacion serial del sensor de CO2")
        #CO2_level= input("Enter CO2 level: ")
           
    print(arrayco2) ##array con valores de CO2 medidos por el sensor
    """
    
    #Temporizador(0, t1)

    arrayco2 = []
    Tempo_user =0
    t1_user=61
    if Temporizador(Tempo_user, t1_user):
        #startco2= time.time()
        print('Temporizador funcionando')
        #GPIO.output(23, GPIO.HIGH)
        #time.sleep(1)
        #GPIO.output(18, GPIO.LOW)
        #for i in range(301):
        """
        for i in range(50):
            serco2.write(str.encode("Z\r\n"))
            resp = serco2.read(10)
            resp = resp[:8]
            fltCo2 = float(resp[2:])
            CO2ppm= fltCo2 * multiplier
            arrayco2.append(CO2ppm)
            #print ("CO2 PPM = ", CO2ppm)
            time.sleep(0.2)#tiempo de muestreo
            #i=i+1
            print(i, CO2ppm)
        print("total time executing this loop", time.time() - startco2)
                
    else:
        print("Verificar comunicacion serial del sensor de CO2")
        #CO2_level= input("Enter CO2 level: ")
           
    print(arrayco2)
    
    """
### Medicion de PETCO2 (llamamos el modulo)
    
    #CO2_level, Fulltime = calculopetco2.PetCo2segtst_df(arrayco2)
    #print(CO2_level)
### Medicion sensor de SPO2
    
    #O2_level= input("Enter O2 level: ")
   # print(O2_level)
    
### Identificamos la condicion del paciente