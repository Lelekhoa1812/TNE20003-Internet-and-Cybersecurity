import paho.mqtt.client as mqtt
import time
import random
import sys

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        if topic:
            client.subscribe(topic)
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    topic = message.topic
    print(f"Received message from topic '{topic}': {payload}")

client = mqtt.Client("mqttx_user")
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("103844421", "103844421")
client.connect("rule28.i4t.swin.edu.au", 1883)

# Subscribe to different topics based on command-line arguments
# Base-topic includes: 103844421 
# Sub-topic-level-1 includes: temperature, humid_rate, air_quality, pulution_rate
# Sub-topic-level-2 includes: inside, outside (temperature)

if len(sys.argv) > 1:
    topic = sys.argv[1]
    client.loop_forever()
else:
    base_topic = "103844421"
    
    # Publish wake-up time as a sub-topic-level-1
    topic1 = "wake_up_time"
    fake_wut = f"{random.randint(4, 10)}:{random.randint(0, 5)}{random.randint(0, 9)} AM"
    print(f"Today wake-up time is: {fake_wut}")
    client.publish(f"{base_topic}/{topic1}", fake_wut)

    # Publish heart rate as a sub-topic-level-1
    topic2 = "heart_rate"
    fake_ht = round(random.uniform(40, 140), 2)
    print(f"Today heart rate is: {fake_ht} bpm")
    client.publish(f"{base_topic}/{topic2}", str(fake_ht))
