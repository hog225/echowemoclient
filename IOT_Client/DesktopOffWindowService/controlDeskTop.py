#-*- coding: utf-8 -*-
import paho.mqtt.client as mqtt
import time
import os

MQ_SHUTDOWN = "/home_iot/Desktop"
MQ_BROKER_IP = "192.168.0.231"

def on_connect(client, userdata, flags, rc):
    try:
        client.subscribe(MQ_SHUTDOWN)
    except:
        pass


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.payload)
    try:
        if msg.topic == MQ_SHUTDOWN:
            if msg.payload == b'Off':
                # 테스트 용도
                #print("--------------Shut Down Computer--------------")
                # 컴퓨터 끄는 window 명령어
                os.system("shutdown /s /t 0")

    except Exception as e:
        pass



def serviceRun():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    while True:
        try:
            client.connect(MQ_BROKER_IP, 1883, 60)
            break
        except Exception as e:
            time.sleep(10)
    print("Service Run")
    client.loop_forever()


if __name__ == "__main__":
    serviceRun()