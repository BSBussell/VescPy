
import time
from tkinter import *

import VescPy

win = Tk()
master = Frame(win)

Arduino = VescPy.VESC()

def refresh():
    Arduino.update()

def neutral():
    Arduino.setThrottle(1500)
    refresh()

def fullAcceleration():
    Arduino.setThrottle(2000)
    refresh()

def fullReverse():
    Arduino.setThrottle(0)
    refresh()

reverseButton = Button(master, text="Reverse", command=fullReverse)
neutralButton = Button(master, text="Neutral", command=neutral)
accelerationButton = Button(master, text="Full Throttle", command=fullAcceleration)

reverseButton.pack(side=LEFT,padx=10)
neutralButton.pack(side=LEFT,padx=10)
accelerationButton.pack(side=LEFT,padx=10)

l = Label(win, text="Calibration for the ESC")
l2 = Label(win, text="Make sure low voltage mode is disabled and unplug and plug back in the battery")
l3 = Label(win, text="Press Neutral and Press button on ESC until turns it red and release")
l4 = Label(win, text="Once you see a red blink go to full throttle, then once two red go to full reverse")
l.pack()
l2.pack()
l3.pack()
l4.pack()

master.pack()
mainloop()