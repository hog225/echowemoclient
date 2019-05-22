# -*- coding: utf-8 -*-
import RPi.GPIO as g
import time

IN_TOUCH = 4 # GPIO 4
OUT_LED = 17 # GPIO 17 

# BCM
g.setmode(g.BCM)

#g.setup(IN_TOUCH, g.IN, pull_up_down = g.PUD_DOWN)
g.setup(IN_TOUCH, g.IN)
g.setup(OUT_LED, g.OUT, initial=g.LOW)


g.add_event_detect(IN_TOUCH, g.BOTH)
# 터치버튼을 누르면 LED ON 때면 OFF
def sensorCallBack(arg1):
    # arg1 BCM PinNumber
    value = g.input(arg1)

    print "Touch " + "GPIO Value : "+str(value)
    if value == 1:
        g.output(OUT_LED, value)
    else:
        g.output(OUT_LED, 0)

g.add_event_callback(IN_TOUCH, sensorCallBack)

print "Start"


try:
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print "Keyboard Interrupt"

except:
    print "other error "

finally:
    g.cleanup()
    
