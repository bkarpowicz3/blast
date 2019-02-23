import serial
data = serial.Serial('COM10', 115200)

while True:
    print (data.readline())
