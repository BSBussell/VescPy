import serial
import time



class VESC:

    def __init__(self):
        self.ardu = serial.Serial('COM3', 9600, timeout=.1)
        time.sleep(4)

        self.throttleGoal = 0
        self.angleGoal = 90

        self.throttleValue = self.throttleGoal
        self.angleValue = self.angleGoal

        self.smoothing = 1


        self.update()

        print(" Successful initialisation")

    def update(self):

        if (self.throttleValue < self.throttleGoal):
            self.throttleValue += self.smoothing
        elif (self.throttleValue > self.throttleGoal):
            self.throttleValue -= self.smoothing

        if (self.angleValue < self.angleGoal):
            self.angleValue += self.smoothing
        elif (self.angleValue > self.angleGoal):
            self.angleValue -= self.smoothing

        print(self.throttleValue)
        print(self.throttleGoals)
        self.ardu.write(("T"+str(chr(self.throttleValue))).encode())
        self.ardu.write(("S"+str(chr(self.angleValue))).encode())

    def setThrottle(self, Value):

        self.throttleGoal = Value

    def setAngle(self, Value):

        self.angleGoal = Value



