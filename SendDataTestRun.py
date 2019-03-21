import serial
data = serial.Serial('COM3', 115200)
while True:
    print(data.readline())
# 