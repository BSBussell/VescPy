import time
import VescPy

Arduino = VescPy.VESC()

def loop():
    argument = '1500'
    print("Type 'exit' to end ")
    while (1):
        argument = input('Set Throttle: ')
        print(chr(27) + "[2J")
        try:
            if argument == "exit":
                break
            if argument == "read":
                print(Arduino.readThrottle())
            else:
                Arduino.accelerate(int(argument))

                #time.sleep(2)
        except( ValueError):
            print("Invalid Input")





Arduino.setAngle(90)
#print(Arduino.readGyro())
loop()
