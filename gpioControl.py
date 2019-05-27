# -*- coding: utf-8 -*-
import RPi.GPIO as g
import time

IN_TOUCH = 4  # GPIO 4
OUT_LED = 17  # GPIO 17

def setGPIO():
    # BCM
    g.setmode(g.BCM)

    g.setup(IN_TOUCH, g.IN, pull_up_down = g.PUD_DOWN)
    g.setup(OUT_LED, g.OUT, initial=g.LOW)



def runTouchSensor(touchOpt, callback, *args):
    g.add_event_detect(IN_TOUCH, g.BOTH)

    # 터치버튼을 누르면 LED ON 때면 OFF
    def sensorCallBack(arg1):
        # arg1 BCM PinNumber
        value = g.input(arg1)

        print "Touch " + "GPIO Value : " + str(value)
        if value == 1:
            g.output(OUT_LED, value)
        else:
            g.output(OUT_LED, 0)
            callback(*args)


    g.add_event_callback(IN_TOUCH, sensorCallBack)

def clearGPIO():
    g.cleanup()




if __name__ == "__main__":
    # # ------------------ only Touch ---------------------
    # def callBack(arg):
    #     print 'Im Call Back Function ! ' + str(arg)
    #
    # setGPIO()
    # runTouchSensor(None, callBack, 3)
    # # -------------------------------------------------------

    # ------------ Touch with Sonoff ---------------
    import sonoffStateChange as ssc
    from config import Config

    f = file('account.cfg')
    cfg = Config(f)
    USERNAME = cfg.username
    PASSWORD = cfg.password
    API_REGION = cfg.api_region
    SONOFF_LAMP = 'Lamp'

    s = ssc.logOnSonoff(USERNAME, PASSWORD, API_REGION)
    setGPIO()
    runTouchSensor(None, ssc.changeSonoffState, s, SONOFF_LAMP)
    # -------------------------------------------------------
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

    pass