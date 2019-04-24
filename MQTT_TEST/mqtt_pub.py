import paho.mqtt.client as mqtt


client = mqtt.Client()
client.connect("127.0.0.1",1883)

client.publish("test", 'Hello how are you')
client.loop(2)
