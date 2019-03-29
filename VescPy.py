import serial
import time



class VESC:

    def __init__(self):
        self.ardu = serial.Serial('COM3', 9600, timeout=.1)
        time.sleep(4)


        self.throttleValue = 1500
        self.angleValue = 90

        self.throttleSmoothing = 1
        self.angleSmoothing = 1


        self.throttleBase = 1500

        self.update()

        print(" Successful initialisation")

    def __del__(self):
        self.ardu.write(self.buildPacket('T',1500))
        self.ardu.write(self.buildPacket('S',90))

        self.ardu.close()
        print(" Successful Destruction")

    def update(self):



        self.ardu.write(self.buildPacket('T',self.throttleValue))
        self.ardu.write(self.buildPacket('S',self.angleValue))

        print("Throttle: ")
        print(self.throttleValue)
        print("EnCoding: ")
        print(("T"+str(chr(self.throttleValue))).encode('utf-8'))

    def setThrottle(self, Value, Delta=None):

        self.throttleValue = Value
        if (Delta):
            self.throttleSmoothing = Delta
            self.ardu.write(self.buildPacket('t', self.throttleSmoothing))


    def setAngle(self, Value, Delta=None):

        self.angleValue = Value
        if (Delta):
            self.angleSmoothing = Delta
            self.ardu.write(self.buildPacket('s', self.angleSmoothing))


    def readThrottle(self):

        return self.ardu.write('R00')

    def readAngle(self):

        return self.ardu.write('r00')

    def buildPacket(self, char, value):

        self.Low = (value >> 8) & 0xFF
        self.High = value & 0xFF

        self.Packet = bytes([ord(char), self.Low, self.High])

        return self.Packet