import serial
data = serial.Serial('/dev/tty.RNBT-3490-RNI-SPP', 115200)

while True:
    print (data.readline())
