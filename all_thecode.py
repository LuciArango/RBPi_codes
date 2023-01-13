import numpy as np
import skfuzzy as fuzz
import skfuzzy as control
import RPi.GPIO as GPIO
import time
import board
import busio
import serial
#import adafruit_sgp30
import pandas as pd
from pylab import *
import scipy.signal as signal
from scipy.signal import savgol_filter
from scipy.signal import find_peaks
import numpy.ma as ma
import random


###First step : Reading the sensors

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

while True:
    
    O2_level= input("Enter O2 level: ")
    
    ser.write(str.encode("Z\r\n"))
    resp = ser.read(10)#cambiarlo segun no. de muestras por 1 min
    resp = resp[:8]

    fltCo2 = float(resp[2:])
    print ("CO2 PPM = ", fltCo2  * multiplier)
    time.sleep(1)
    
    
    #print(CO2_level)
    print(O2_level)
    
