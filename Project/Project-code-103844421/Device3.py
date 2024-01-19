import paho.mqtt.client as mqtt
import time
import random

# This device monitoring the air quality (asi) and pollution rate (%) outside the house
def on_publish(client, userdata, result):
    print("Message published")

client = mqtt.Client("mqttx_device3")
client.on_publish = on_publish

client.username_pw_set("103844421", "103844421")
client.connect("rule28.i4t.swin.edu.au", 1883)

base_topic1 = "103844421"  # Base-topic-private
base_topic2 = "public"  # Base-topic-public
topic1 = "air_quality"  # Sub-topic-level-1
topic2 = "polution_rate"  #  Sub-topic-level-1
client.loop_start()

while True:
    # Generate random data for air_quality and pollution_rate
    fake_aq = round(random.uniform(1, 30), 2)
    fake_pr = round(random.uniform(10, 50), 2)

    client.publish(f"{base_topic1}/{topic1}", f"{fake_aq} asi")
    client.publish(f"{base_topic1}/{topic2}", f"{fake_pr} %")
    client.publish(f"{base_topic2}/{topic1}", f"{fake_aq} asi")
    client.publish(f"{base_topic2}/{topic2}", f"{fake_pr} %")

    time.sleep(5)
