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

my_machine: PickAndPlaceMachine = PickAndPlaceMachine("My Machine", [("Transistor", 100), ("Capacitor", 200), ("Resistor", 300)])
client: mqtt.Client = mqtt.Client(MICRO_SERVICE_NAME)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"{MICRO_SERVICE_NAME} connected to MQTT Broker!")
    else:
        print(f"Failed to connect, return code {rc}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f'Connection ended unexpectedly from broker, error code {rc}')

def on_subscribe(client, userdata, mid, granted_qos):
    print(f'Successfully subscribed ')

def send_material_used_msg(material_name : str, components_used : int) -> None:
    msg = pickle.dumps((material_name, components_used))
    client.publish(TOPIC, payload=msg, qos=2)

def on_roll_empty(material_name : str) -> None:
    my_machine.shutdown()

def main():
    client.username_pw_set(USERNAME, PASSWORD)

    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    client.connect(BROKER_ADDRESS)
    client.loop_start()

    my_machine.set_material_used_event_handler(send_material_used_msg)
    my_machine.set_material_roll_empty_event_handler(on_roll_empty)

    my_machine.start()

    while my_machine.is_running():
        time.sleep(10)

if __name__ == "__main__":
    main()