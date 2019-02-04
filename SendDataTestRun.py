import serial
data = serial.Serial('/dev/tty.usbmodem14101', 115200)

while True:
    print (data.readline())
