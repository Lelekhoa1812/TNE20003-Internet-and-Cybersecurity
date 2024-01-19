import paho.mqtt.client as mqtt
import sys

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    if rc == 0:
        client.subscribe(topic)
    else:
        print("Connection failed")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    topic = message.topic
    print(f"Received message from topic '{topic}': {payload}")

client = mqtt.Client("mqttx_client")
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set("103844421", "103844421")
client.connect("rule28.i4t.swin.edu.au", 1883)

# Subscribe to different topics based on command-line arguments
# Base-topic includes: 103844421 
# Sub-topic-level-1 includes: temperature, humid_rate, air_quality, pulution_rate, wake_up_time, heart_rate 
# Sub-topic-level-2 includes: inside, outside (temperature)

if len(sys.argv) != 2:
    print("Usage: python Client.py <topic>")
    sys.exit(1)

topic = sys.argv[1]

client.loop_forever()
