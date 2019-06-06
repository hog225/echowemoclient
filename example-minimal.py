# -*- coding: utf-8 -*-
""" fauxmo_minimal.py - Fabricate.IO

    This is a demo python file showing what can be done with the debounce_handler.
    The handler prints True when you say "Alexa, device on" and False when you say
    "Alexa, device off".

    If you have two or more Echos, it only handles the one that hears you more clearly.
    You can have an Echo per room and not worry about your handlers triggering for
    those other rooms.

    The IP of the triggering Echo is also passed into the act() function, so you can
    do different things based on which Echo triggered the handler.
"""

import fauxmo
import logging
import time
import threadFunction as tf
from debounce_handler import debounce_handler
import gpioControl as gc
import sonoffStateChange as ssc
from config import Config
import irlib as ir

logging.basicConfig(level=logging.DEBUG)

# ------------ MQTT INFO -----------
BROKER_IP = "127.0.0.1"
BROKER_PORT = 1883
MQ_TOPIC = "/home_iot/Desktop"


# ------------ Bluetooth Address -----------
HC_06_com_addr = "20:14:04:11:22:37"
HC_06_com_port = 1

# ------------ Device Name -----------------
COMPUTER = 'Desktop'
AIRCON = 'Aircon'

# ------------ Touch Sonoff ----------------
f = file('account.cfg')
cfg = Config(f)
USERNAME = cfg.username
PASSWORD = cfg.password
API_REGION = cfg.api_region
SONOFF_LAMP = 'Lamp'
# ------------------IR BUTTON----------------------
IR_BUTTON_FILE = "ir-codes"
AIRCON_ON = 1
AIRCON_OFF = 2

class device_handler(debounce_handler):
    """Publishes the on/off state requested,
       and the IP address of the Echo making the request.
    """
    # Device
    TRIGGERS = {COMPUTER: 51999, AIRCON: 52000}

    def act(self, client_address, state, name):
        print "State", state, "on ", name, "from client @"
        # "Desktop" 에 관한 명령이 Echo dot 으로 들어오면 처리해 주는 부분
        if name == COMPUTER:
            if state == True:
                tf.bt_q.put_nowait('True')
            elif state == False:
                tf.publishMSG(BROKER_IP, BROKER_PORT, MQ_TOPIC, 'Off')
        elif name == AIRCON:
            if state == True:
                ir.sendIRSignal(IR_BUTTON_FILE, AIRCON_ON)
            elif state == False:
                ir.sendIRSignal(IR_BUTTON_FILE, AIRCON_OFF)
        return True

if __name__ == "__main__":
    # Startup the fauxmo server
    fauxmo.DEBUG = True
    p = fauxmo.poller()
    u = fauxmo.upnp_broadcast_responder()
    u.init_socket()
    p.add(u)

    tf.connectBluetooth(HC_06_com_addr, HC_06_com_port)
    RecoveryThread = tf.MThread(1, "RecoveryThread", tf.recoveryProcess, HC_06_com_addr, HC_06_com_port)
    RecoveryThread.start()
    print 'fauxmo start'
    # Register the device callback as a fauxmo handler
    d = device_handler()
    for trig, port in d.TRIGGERS.items():
        fauxmo.fauxmo(trig, u, p, None, port, d)

    # Loop and poll for incoming Echo requests
    logging.debug("Entering fauxmo polling loop")

    # -----------Touch Sensor Control Sonoff--------------------
    s = ssc.logOnSonoff(USERNAME, PASSWORD, API_REGION)
    gc.setGPIO()
    gc.runTouchSensor(None, ssc.changeSonoffState, s, SONOFF_LAMP)

    # ----------------------------------------
    try:
        while True:
            try:
                # Allow time for a ctrl-c to stop the process
                p.poll(100)
                time.sleep(0.1)
            except Exception, e:
                logging.critical("Critical exception: " + str(e))
                RecoveryThread.stop_flag.clear()
                RecoveryThread.join()

    except KeyboardInterrupt:
        print "Keyboard Interrupt"

    except:
        print "other error "

    finally:
        gc.clearGPIO()