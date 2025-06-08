import serial

ser = serial.Serial(port = 'COM3', baudrate=9600)

while True:
    value=ser.readline()
    valueInInt=float(value)
    print(valueInInt)
