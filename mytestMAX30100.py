import max30102
import hrcalc
import time

m = max30102.MAX30102()

#hr2 = 0
#sp2 = 0

while True:
    red, ir = m.read_sequential()
    
    print(hrcalc.calc_hr_and_spo2(ir, red))

        