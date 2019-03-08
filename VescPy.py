import serial
import time



class VESC:

    def __init__(self):
        self.ardu = serial.Serial('COM3', 9600, timeout=.1)
        time.sleep(4)


        self.throttleValue = 90
        self.angleValue = 90

        self.throttleSmoothing = 100
        self.angleSmoothing = 100


        self.throttleBase = 90

        self.update()

        print(" Successful initialisation")

    def __del__(self):
        self.ardu.write(("T" + str(chr(90))).encode())
        self.ardu.write("SZ".encode())

        self.ardu.close()
        print(" Successful Destruction")

    def update(self):

        '''
        self.throttleDelta = self.throttleGoal-self.throttleValue
        self.angleDelta = self.angleGoal-self.angleValue

        self.throttleSign = abs(self.throttleDelta)/self.throttleDelta
        self.angleSign = abs(self.angleDelta)/self.angleDelta


        if (abs(self.throttleDelta) >self.smoothing):
            self.throttleValue += self.smoothing*self.throttleSign

        if (abs(self.angleDelta) > self.smoothing):
            self.angleValue += self.smoothing*self.angleSign


        '''



        self.ardu.write(("T"+str(chr(self.throttleValue))).encode())
        self.ardu.write(("S"+str(chr(self.angleValue))).encode())

        print("Throttle: ")
        print(self.throttleValue)
        print("EnCoding: ")
        print(("T"+str(chr(self.throttleValue))).encode('utf-8'))

    def setThrottle(self, Value, Delta=None):

        self.throttleValue = self.throttleBase+Value
        if (Delta):
            self.throttleSmoothing = Delta
            self.ardu.write(("t"+str(chr(self.throttleSmoothing))).encode())


    def setAngle(self, Value, Delta=None):

        self.angleValue = Value
        if (Delta):
            self.angleSmoothing = Delta
            self.ardu.write(("s"+str(chr(self.angleSmoothing))).encode())



