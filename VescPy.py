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

        self.directionChangeThread = Timer(1.0, self.directionChange, [0])

        print(" Successful initialisation")

    def __del__(self):

        if self.directionChangeThread.is_alive():
            self.directionChangeThread.cancel()

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


    def accelerate(self, Value):

        if self.directionChangeThread.is_alive():
            self.directionChangeThread.cancel()

        self.waitTime = 2.0
        if (int(self.readThrottle())-self.throttleNeutral) >= 0 and Value < 0:
            self.directionChangeThread = Timer(0.01, self.directionChange, [Value])
            self.directionChangeThread.start()
        else:
            self.throttleValue = Value
            self.update()



    def setThrottle(self, Value: int, Delta=None):

        self.throttleValue = Value - self.throttleNeutral

        self.ardu.write(self.buildPacket('T', Value))
        if (Delta):
            self.throttleSmoothing = Delta
            self.ardu.write(self.buildPacket('t', self.throttleSmoothing))



    def setAngle(self, Value: int, Delta=None):

        self.angleValue = Value

        if (Delta):
            self.angleSmoothing = Delta
            self.ardu.write(self.buildPacket('s', self.angleSmoothing))


    def readThrottle(self) -> int:

        self.ardu.write('R00'.encode())
        return int(self.ardu.readline().decode())

    def readAngle(self):

        self.ardu.write('r00'.encode())
        return self.ardu.readline().decode()

    def buildPacket(self, char, value):

        self.Low = (value >> 8) & 0xFF
        self.High = value & 0xFF

        self.Packet = bytes([ord(char), self.Low, self.High])

        return self.Packet


    def directionChange(self, Value):

        self.throttleValue = -120
        self.update()
        time.sleep(.25)
        self.throttleValue = 0
        self.update()
        time.sleep(.25)
        self.throttleValue = Value
        self.update()

