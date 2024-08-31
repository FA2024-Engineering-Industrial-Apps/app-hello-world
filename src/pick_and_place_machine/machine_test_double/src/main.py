import paho.mqtt.client as mqtt
from machine import PickAndPlaceMachine
import pickle
import time

# MQTT Broker details
BROKER_ADDRESS = 'ie-databus'
BROKER_PORT = 1883
MICRO_SERVICE_NAME = 'pick_and_place_machine'

# Authentication details
USERNAME = 'edge'
PASSWORD = 'edge'

# Define the topic you want to publish to
TOPIC = 'raw_data/material_consumption'

my_machine: PickAndPlaceMachine
client: mqtt.Client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"{MICRO_SERVICE_NAME} connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Message {mid} published successfully.")

def send_material_used_msg(material_name : str, components_used : int) -> None:
    msg = pickle.dumps((material_name, components_used))
    client.publish(TOPIC, payload=msg, qos=1)

def refill_material_roll(material_name : str) -> None:
    my_machine.refill_material(material_name, 100)

def main():
    client = mqtt.Client(MICRO_SERVICE_NAME)
    client.username_pw_set(USERNAME, PASSWORD)

    client.on_connect = on_connect
    client.on_publish = on_publish

    client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=60)
    client.loop_start()

    my_machine = PickAndPlaceMachine("My Machine", [("Transistor", 100), ("Capacitor", 100), ("Resistor", 100)])

    my_machine.set_material_used_event_handler(send_material_used_msg)
    my_machine.set_material_roll_empty_event_handler(refill_material_roll)

    my_machine.start()

    while my_machine.is_running():
        time.sleep(10)

if __name__ == "__main__":
    main()