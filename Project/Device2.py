import paho.mqtt.client as mqtt
import time
import random

# This device monitoring the humidity outside the house (in percentage %)
def on_publish(client, userdata, result):
    print("Message published")

client = mqtt.Client("mqttx_device2")
client.on_publish = on_publish

client.username_pw_set("103844421", "103844421")
client.connect("rule28.i4t.swin.edu.au", 1883)

topic1 = "103844421/humid_rate"  # Base-topic-private/Sub-topic-level-1
topic2 = "public/humid_rate"  # Base-topic-public/Sub-topic-level-1
client.loop_start()

while True:
    fake_humidity = round(random.uniform(20, 80), 2)
    client.publish(topic1, f"{fake_humidity} %")
    client.publish(topic2, f"{fake_humidity} %")

    time.sleep(5)
