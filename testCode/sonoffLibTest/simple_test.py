# -*- coding: utf-8 -*-
import sonoff
import sys
from config import Config

f = file('account.cfg')
cfg = Config(f)

username = cfg.username
password = cfg.password
api_region = cfg.api_region

# -- Dictionary 를 예쁘게 Print 해 줌 (기능에는 필요 없는 함수)--
def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print >> output, '%s{' % ((nested_level) * spacing)
        for k, v in obj.items():
            if hasattr(v, '__iter__'):
                print >> output, '%s%s:' % ((nested_level + 1) * spacing, k)
                dump(v, nested_level + 1, output)
            else:
                print >> output, '%s%s: %s' % ((nested_level + 1) * spacing, k, v)
        print >> output, '%s}' % (nested_level * spacing)
    elif type(obj) == list:
        print >> output, '%s[' % ((nested_level) * spacing)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print >> output, '%s%s' % ((nested_level + 1) * spacing, v)
        print >> output, '%s]' % ((nested_level) * spacing)
    else:
        print >> output, '%s%s' % (nested_level * spacing, obj)


s = sonoff.Sonoff(username, password, api_region)
devices = s.get_devices()
if devices:
    # We found a device, lets turn something on
    for dev in devices:
        #dump(dev)
        print dev['name']


    device_id = devices[0]['deviceid']
    s.switch('on', device_id, None)
