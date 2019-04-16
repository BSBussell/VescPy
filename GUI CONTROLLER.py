import time
from tkinter import *

import VescPy

win = Tk()
master = Frame(win)

throttle = 0
textThrottle = StringVar()
textThrottle.set(str(throttle))


angle = 90

textPhysical = StringVar()
textPhysical.set(str(throttle))

Arduino = VescPy.VESC()


def read():
    global textPhysical
    textPhysical.set(str(Arduino.readThrottle()))
    refresh()

def refresh(event = None):
    Arduino.update()

def increment(event=None):
    global throttle
    global throttleValue
    throttle += 5
    Arduino.accelerate(throttle)
    textThrottle.set(str(throttle))
    #refresh()

def decrement(event=None):
    global throttle
    global throttleValue
    throttle -= 5
    Arduino.accelerate(throttle)
    textThrottle.set(str(throttle))
    #refresh()

def left(event = None):
    global angle
    angle -= 10
    Arduino.setAngle(angle)
    refresh()

def right(event = None):
    global angle
    angle += 10
    Arduino.setAngle(angle)
    refresh()



win.bind('<Up>', increment)
win.bind('<Down>', decrement)
win.bind('<Left>', left)
win.bind('<Right>', right)
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