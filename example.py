import time
import VescPy

Arduino = VescPy.VESC()

def setup():
    Arduino.setAngle(95)
    Arduino.setThrottle(100)

def update():
    Arduino.update()

setup()
deltaTime = time.time()
while (time.time()-deltaTime<5):
    update()


Arduino.setThrottle(0)
while (time.time()-deltaTime<5):
    update()