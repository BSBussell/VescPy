import time
import VescPy

Arduino = VescPy.VESC()

def setup():
    Arduino.setAngle(90)
    Arduino.setThrottle(10)

def update():
    Arduino.update()

setup()
deltaTime = time.time()
update()
time.sleep(5)

Arduino.setThrottle(-10,100)
deltaTime = time.time()
update()
time.sleep(5)


'''

int a;

byte high = (byte)(a >> 8)
byte low = (byte)(a&0xFF)



high

high << 8 + low


'''