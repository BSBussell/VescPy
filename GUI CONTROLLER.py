import time
from tkinter import *

import VescPy

win = Tk()
master = Frame(win)

throttle = 0
textThrottle = StringVar()
textThrottle.set(str(throttle))


textPhysical = StringVar()
textPhysical.set(str(throttle))

Arduino = VescPy.VESC()


def read():
    global textPhysical
    textPhysical.set(str(Arduino.readThrottle()))
    refresh()

def refresh():
    Arduino.update()

def increment():
    global throttle
    global throttleValue
    throttle += 1
    Arduino.accelerate(throttle)
    textThrottle.set(str(throttle))
    refresh()

def decrement():
    global throttle
    global throttleValue
    throttle -= 1
    Arduino.accelerate(throttle)
    textThrottle.set(str(throttle))
    refresh()



subtract = Button(master, text="<", command=decrement, repeatdelay=500, repeatinterval=50)
throttleValue = Label(master, textvariable=textThrottle)
add = Button(master, text=">", command=increment, repeatdelay=500, repeatinterval=50)

subtract.pack(side=LEFT)
throttleValue.pack(side=LEFT)
add.pack(side=LEFT)

data = Frame(win)

physicalValue = Label(data, textvariable=textPhysical)
reload = Button(data, text="Update", command = read)

physicalValue.pack(side=LEFT)
reload.pack(side=RIGHT, padx=10)


master.pack()
data.pack()

mainloop()