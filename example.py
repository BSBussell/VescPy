import time
import VescPy

Arduino = VescPy.VESC()
def update():
    Arduino.update()

def loop():
    argument = '1500'
    print("Type 'exit' to end ")
    while (argument != 'exit'):
        argument = input('Set Throttle: ')
        if (argument == "exit"):
            break
        if (argument == "read"):
            print(Arduino.readThrottle())
        else:
            Arduino.setThrottle(int(argument))
            update()
            time.sleep(2)




loop()
time.sleep(5)






'''

int a;

byte high = (byte)(a >> 8)
byte low = (byte)(a&0xFF)



high

high << 8 + low

'''