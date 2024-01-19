import tkinter as tk
import sys
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
        client.subscribe(topic_entry.get())
    else:
        print("Connection to MQTT broker failed")

def on_message(client, userdata, message):
    payload = message.payload.decode()
    topic = message.topic
    display_data(topic, payload)

def display_data(topic, data):
    data_text.config(state=tk.NORMAL)
    data_text.insert(tk.END, f"Topic: {topic}\nData: {data}\n\n")
    data_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("MQTT Client Interface")

topic_label = tk.Label(root, text="Topic:")
topic_label.pack()

topic_entry = tk.Entry(root)
topic_entry.pack()

data_text = tk.Text(root, wrap=tk.WORD, width=40, height=20)
data_text.config(state=tk.DISABLED)
data_text.pack()

subscribe_button = tk.Button(root, text="Subscribe", command=lambda: subscribe_topic(topic_entry.get()))
subscribe_button.pack()

def subscribe_topic(new_topic):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.username_pw_set("103844421", "103844421")
    client.connect("rule28.i4t.swin.edu.au", 1883)
    
    client.loop_start()
    client.subscribe(new_topic)

root.mainloop()
