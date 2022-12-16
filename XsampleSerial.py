import uart_comm
"""
ser1 = serial.Serial(port='/dev/ttyACM0',baudrate = 230400,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
counter=0
def writeCMDser ():
    ser1.write("rgb,__red\n".encode('utf-8'))
    time.sleep(4)
    ser1.write("rgb,green\n".encode('utf-8'))
    time.sleep(4)
    ser1.write("rgb,_blue\n".encode('utf-8'))
    time.sleep(4)
    ser1.write("rgb,yello\n".encode('utf-8'))
    time.sleep(4)
    ser1.write("rgb,magen\n".encode('utf-8'))
    time.sleep(4)
    ser1.write("rgb,_cyan\n".encode('utf-8'))
    time.sleep(4)
    ser1.write("rgb,white\n".encode('utf-8'))
    time.sleep(4)
    ser1.write("rgb,__off\n".encode('utf-8'))
    time.sleep(4)
while counter < 1:
    writeCMDser ()
    counter += 1
"""
#uart_comm.Available()
uart_comm.writeCMDser("rgb,__off\n")