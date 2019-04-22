# Benjamin S. Bussell
# March 6th, 2019

import serial
import time
from threading import Thread

'''

Class: VESC
A Class for connecting to the Arduino without having to worry about byte shifts
or weird Anomalies that might cause the XL5 Speed Controller to only reverse upon
a series of random inputs that take you weeks to figure out causing you to rewrite your entire program

'''


class VESC:

    '''
        Function: initialisation
            Connect to the Arduino and runs initialisation of the Arduino Creates threads and variables
            then updates to make sure everything is peachy. It takes about 4 seconds for the arduino to finsish initalization
            so the time.sleep function tries to prevent anything from messing with the arduino's initalisation, might be slow
            but it'll stop you from having to worry about waiting for it to finish.
            The Throttle Values works by setting a neutral hopefully calibrated to be 1500ms if its not run the obviously names file
            and follow instructions.
            I haven't messed with smoothing much since final release and neither should you.
    '''

    def __init__(self, debug = False):

        self.debug = debug

        try:
            # This port should be the one on the right side of your computer. Hopefully your using the right one.
            # TODO: Make function for finding active serial ports that'll work

            self.ardu = serial.Serial('COM3', 9600, timeout=.1)

        except(FileNotFoundError, serial.SerialException):

            print("No Open Serial Port Could be found entering debug mode")
            self.debug = True
            #return

        # Everytime I try making this work as a time for a seperate timer it breaks everything else.
        time.sleep(4)

        # Throttle Shit
        self.throttleValue = 0
        self.throttleNeutral = 1500

        # Angle Shit
        self.angleValue = 90

        # Shit
        self.throttleSmoothing = 1
        self.angleSmoothing = 1

        # Make sure all values are set to the correct position by setting them to the correct position.
        self.update()

        # A Seperate thread for queuing complex direction Changes.
        self.directionChangeThread = Thread(target=self.directionChange, args=(0,))

        # If nothing catches fire you'll get here.
        print(" Successful initialisation")

    # If you unplug it, it goes to neutral, done easy solution.
    def __del__(self):

        # kill anything in the queue
        if self.directionChangeThread.is_alive():
            self.directionChangeThread.join()

        # As long as it's properly calibrates
        # self.buildPacket is explained in the update function bellow.
        if (self.debug == False):
            self.ardu.write(self.buildPacket('T', self.throttleNeutral))
            self.ardu.write(self.buildPacket('S', 90))

        # Close Port so no longer connected.
        self.ardu.close()

        print("Successful Destruction")

    '''
        Function: self.update()
            This function applies the throttle value to the neutral, and then sends those values to the Arduino.
            Only really called by lower level programs like the calibrator.
    '''

    def update(self):

        # Get Full Value of throttle by adding the neutral to the value
        self.throttleChange = self.throttleNeutral + self.throttleValue

        # These two lines pretty much do the same thing. They send data in a readable format to the Arduino
        # self.buildPacket() takes two arguments one is a character the other is a number. It then converts this
        # into bytes that can be read by the Arduino.
        # self.ardu.write() simply "writes" these bytes to the XL5
        if (self.debug == False):
            self.ardu.write(self.buildPacket('T', self.throttleChange))
            self.ardu.write(self.buildPacket('S', self.angleValue))
        #else:
            #print("Throttle: ", self.throttleChange)
            #print("Angle:", self.angleValue)

    '''
        Function: self.accelerate( Speed)
            This function automatically handles most throttle input issues for you and works by allowing you
            to send the speed to the ESC where positive is forward and negative is reverse You do not need to and should
            not manually call the update function after running this code.
            Good testing values are 120 and -120
    '''

    def accelerate(self, Value: int):


        # This is pretty much a check to see if the throttle is going from acceleration
        # To full reverse
        if (self.readThrottle() - self.throttleNeutral) >= 0 > Value:
            # Calls the weird steps required to register reverse and makes sure they don't
            # Freeze up the program by calling them on a separate thread.
            self.directionChangeThread = Thread(target=self.directionChange, args=(Value,))
            self.directionChangeThread.start()
        else:
            # Should be self explanatory
            self.throttleValue = Value
            self.update()

    '''
        Function: self.setThrottle( Value, Delta: Optional)
            Literally sets the throttle to the value you say. Also if you include the parameter Delta, you can change 
            the smoothing
            BUT DON'T DO THAT UNTIL I'VE TESTED IT I HAVE NO IDEA WHAT WILL HAPPEN
    '''

    def setThrottle(self, Value: int, Delta=None):

        # To ensure compabitability with the rewrite this code adjust the value send by the neutral so you don't
        # Have to worry about that
        self.throttleValue = Value - self.throttleNeutral

        # I did this for a reason I can't remember and when I take it out the code breaks
        if (self.debug == False):
            self.ardu.write(self.buildPacket('T', Value))
        #else:
            #print("Throttle Set: ", Value)

        # Sends and sets Delta when you need it but DON'T
        if (Delta):
            self.throttleSmoothing = Delta
            self.ardu.write(self.buildPacket('t', self.throttleSmoothing))

    '''
        Function: self.setAngle( Value, Delta: Optional)
            Sets the angle for the wheels to turn. 90 is straight ahead 0 is left and 180 is right. Same Principle with
            Delta applies here
    '''
    def setAngle(self, Value: int, Delta=None):

        # Self Explanatory
        self.angleValue = Value
        # TODO: Smoother Angle Changes Testing
        if (Delta):
            self.angleSmoothing = Delta
            self.ardu.write(self.buildPacket('s', self.angleSmoothing))

    '''
        Function: self.readThrottle() and self.readAngle()
                Grouped together they both return the physical values of the motor, can help with debugging and find 
                discrepencies with What your code says and what the Arduino says
    '''
    def readThrottle(self) -> int:

        if (self.debug == False):
            self.ardu.write('R00'.encode())
            return int(self.ardu.readline().decode())
        else:
            return self.throttleValue+self.throttleNeutral

    def readAngle(self) -> int:

        self.ardu.write('r00'.encode())
        return int(self.ardu.readline().decode())

    def readGyro(self):

        self.ardu.write('G00'.encode())
        list = {
            'x': float(self.ardu.readline().decode()),
            'y': float(self.ardu.readline().decode()),
            'z': float(self.ardu.readline().decode())
        }
        return list

    def readAccel(self):

        self.ardu.write('A00'.encode())
        list = {
            'x': float(self.ardu.readline().decode()),
            'y': float(self.ardu.readline().decode()),
            'z': float(self.ardu.readline().decode())
        }
        return list

    def readMag(self):

        self.ardu.write('m00'.encode())
        list = {
            'x': float(self.ardu.readline().decode()),
            'y': float(self.ardu.readline().decode()),
            'z': float(self.ardu.readline().decode())
        }
        return list



    '''
        Function: self.directionChange( Value)
            There is no reason this should be needed... but it is. Pretty much the ESC goes into a failsafe when you 
            suddenly reverse. After going forwards and for our ESC this means any negative value after you send a 
            positive value. Through trial and error I figured out if you set a negative value wait a bit then 
            reset the ESC to 0 it tricks the overprotective fail-safe
            
            Be CAREFUL when calling as it will stop every process in the current thread until steps are complete.
            Would advise calling this function in a different thread when using to prevent situations where the user
            has no control over the car.
            If you don't know how to do this look at how it is handled in the function self.acceleration()
    '''
    def directionChange(self, Value):

        # Trigger Fail-Safe
        self.throttleValue = -120
        self.update()
        time.sleep(.25)

        # Disable Fail-Safe
        self.throttleValue = 0
        self.update()
        time.sleep(.25)

        # Go Around the Fail-Safe
        self.throttleValue = Value
        self.update()


    '''
        Function: self.buildPacket( instructionLetter, Value)
            This reformats your number to be readable by the arduino.
            Shouldn't break so if you can't already tell what it does just explain it as magic.
    '''
    def buildPacket(self, char, value):

        # split the byte in half
        # EX: 0010 0001 0100 0010 -> 0010 0001 and 0100 0010
        # Done to streamline sending the bytes to arduino and allow for numbers above 255.
        self.Low = (value >> 8) & 0xFF
        self.High = value & 0xFF

        # Builds byte array out of the character in binary format and the two bytes above
        self.Packet = bytes([ord(char), self.Low, self.High])

        return self.Packet