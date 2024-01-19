import paho.mqtt.client as mqtt
import time
import random

# This device monitoring the temperature in and outside the house (in Celsius degree)
def on_publish(client, userdata, result):
    print("Message published")

client = mqtt.Client("mqttx_device1")
client.on_publish = on_publish

client.username_pw_set("103844421", "103844421")
client.connect("rule28.i4t.swin.edu.au", 1883)

base_topic1 = "public/temperature"  # Base-topic-public/Sub-topic-level-1
base_topic2 = "103844421/temperature"  # Base-topic-private/Sub-topic-level-1
client.loop_start()

while True:
    fake_temperature_inside = round(random.uniform(15, 30), 2)
    fake_temperature_outside = round(random.uniform(-10, 40), 2)

    # Publish temperature data to corresponding to the Sub-topic-level-2
    client.publish(f"{base_topic1}/inside", f"{fake_temperature_inside} °C")  
    client.publish(f"{base_topic1}/outside", f"{fake_temperature_outside} °C")  
    client.publish(f"{base_topic2}/inside", f"{fake_temperature_inside} °C")  
    client.publish(f"{base_topic2}/outside", f"{fake_temperature_outside} °C")  

    time.sleep(5)
