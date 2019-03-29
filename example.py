import time
import VescPy

Arduino = VescPy.VESC()

def setup():
    Arduino.setAngle(160)
    Arduino.setThrottle(1500)

def update():
    Arduino.update()

setup()
deltaTime = time.time()
update()
time.sleep(5)

Arduino.setThrottle(1500)
update()
time.sleep(5)






'''

int a;

byte high = (byte)(a >> 8)
byte low = (byte)(a&0xFF)



high

high << 8 + low

'''