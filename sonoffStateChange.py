# -*- coding: utf-8 -*-

import sonoff
import time

BOUNCE_TIME = 5 # seconds
FIRST_CALL = 0

# Sonoff ------------------------------------
def logOnSonoff(username, password, api_region):
    s = sonoff.Sonoff(username, password, api_region)
    return s

def changeSonoffState(sonoff, deviceName):

    devices = sonoff.get_devices()
    if devices:
        for dev in devices:
            if dev['name'] == deviceName:
                device_id = dev['deviceid']
                if dev['params']['switch'] == 'on':
                    print 'Sonoff OFF'
                    sonoff.switch('off', device_id, None)
                else:
                    print 'Sonoff ON'
                    sonoff.switch('on', device_id, None)




if __name__ == "__main__":

    # ----Sonoff ------
    from config import Config
    f = file('account.cfg')
    cfg = Config(f)
    username = cfg.username
    password = cfg.password
    api_region = cfg.api_region
    # ------------------------
    pass