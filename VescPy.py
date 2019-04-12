import serial
import time
from threading import Timer


class VESC:

    def __init__(self):
        self.ardu = serial.Serial('COM3', 9600, timeout=.1)
        time.sleep(4)




        self.throttleValue = 0
        self.throttleNeutral= 1500

        self.angleValue = 90

        self.throttleSmoothing = 1
        self.angleSmoothing = 1



        self.update()

        self.threadStack = Timer(2.0, self.update())

        print(" Successful initialisation")

    def __del__(self):

        if self.threadStack.is_alive():
            self.threadStack.cancel()

        self.ardu.write(self.buildPacket('T', self.throttleNeutral))
        self.ardu.write(self.buildPacket('S', 90))

        self.ardu.close()
        print("Successful Destruction")

    def update(self):

        #if self.threadStack.is_alive():
        #    self.threadStack.cancel()

        self.throttleChange = self.throttleNeutral+self.throttleValue

        self.ardu.write(self.buildPacket('T', self.throttleChange))
        self.ardu.write(self.buildPacket('S', self.angleValue))

        print("Throttle: ")
        print(self.throttleChange)

    def accelerate(self, Value):

        if self.threadStack.is_alive():
            self.threadStack.cancel()

        if (int(self.readThrottle())-self.throttleNeutral) > 0 and Value < 0:
            self.directionChange(Value)
            self.waitTime = 2.0
        else:
            self.waitTime = 2.0

        #self.threadStack = Timer(self.waitTime, self.update())
        self.throttleValue = Value
        self.threadStack.start()

    '''def reverse(self, Value):

        self.threadStack.cancel()
        self.threadStack = Timer(2.0, self.update())

        if self.throttleValue > 0:
            self.throttleValue = 0
            self.update()
            
            while (self.readThrottle() != self.throttleValue):
                pass
            self.throttleValue = Value
            self.threadStack.start()
            
        else:
            self.throttleValue = Value
            self.threadStack.start()

    '''

    def setThrottle(self, Value, Delta=None):

        self.throttleValue = Value - self.throttleNeutral

        self.ardu.write(self.buildPacket('T', Value))
        if (Delta):
            self.throttleSmoothing = Delta
            self.ardu.write(self.buildPacket('t', self.throttleSmoothing))



    def setAngle(self, Value, Delta=None):

        self.angleValue = Value
        if (Delta):
            self.angleSmoothing = Delta
            self.ardu.write(self.buildPacket('s', self.angleSmoothing))


    def readThrottle(self):

        self.ardu.write('R00'.encode())
        return self.ardu.readline().decode()

    def readAngle(self):

        self.ardu.write('r00'.encode())
        return self.ardu.readline().decode()

    def buildPacket(self, char, value):

        self.Low = (value >> 8) & 0xFF
        self.High = value & 0xFF

        self.Packet = bytes([ord(char), self.Low, self.High])

        return self.Packet


    def directionChange(self, Value):

        self.throttleValue = Value
        self.update()
        time.sleep(.25)
        self.throttleValue = 0
        self.update()
        time.sleep(.25)
