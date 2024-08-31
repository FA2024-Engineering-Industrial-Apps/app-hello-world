# Copyright 2021 Siemens AG
# This file is subject to the terms and conditions of the MIT License.  
# See LICENSE file in the top-level directory.

"""Module Data Analytics.

This module consists of DataGenerator class and also the function to generate
bivariate normal distributed datasets.

"""

import paho.mqtt.client as mqtt
import sys
import logging
import statistics
import json
import pickle

BROKER_ADDRESS='ie-databus'
BROKER_PORT=1883
MICRO_SERVICE_NAME = 'data-analytics'
""" Broker user and password for authtentification"""
USERNAME='edge'
PASSWORD='edge'

class DataAnalyzer():
    """
    Data Analyzer connects to mqtt broker and waits for new
    input data to calculate KPIs.

    """

    def __init__(self, logger_parent):
        """ Starts the instantiated object with a proper logger """
        
        logger_name = '{}.{}'.format(logger_parent,__name__)
        self.logger = logging.getLogger(logger_name)
        self.client = mqtt.Client(MICRO_SERVICE_NAME)
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.on_message
        self.topic_callback = dict()

        # number of components
        self.n_capacitors = 50
        self.n_resistors = 50
        self.n_transistors = 50

    def on_connect(self, client, userdata, flags, rc):
        self.logger.info('Connected successfully to broker, response code {}'.format(rc))

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            self.logger.warning('Connection ended unexpectedly from broker, error code {}'.format(rc))

    def on_subscribe(self, client, userdata, mid, granted_qos):
        
        self.logger.info('successfully subscribed ')

    def on_message(self, client, userdata, message):
        self.logger.info('New message received on topic: {}'.format(message.topic))
        try:
            self.topic_callback[message.topic](message.payload)
        except Exception as err:
            self.logger.error('An error ocurred while hanlding new message of {}: {}'.format(message.topic, err))

    def subscribe(self, topic, callback):
        """ Subscribes to given topic, assigning a callback function that
        handles the received payload

        :topic:     string with the topic to subscribe
        :callback:  function to assign the payload received
        """
        self.topic_callback.update({topic:callback})
        self.client.subscribe(topic)
    
    def material_consumption(self, payload):
        self.logger.info('calculating pick and place machine...')
        # unpickle the payload
        material_name, components_used = pickle.loads(payload)
        topic = 'raw_data/material_consumption'

        if material_name == 'Transistor':
            self.logger.info('Transistor material consumed: {}'.format(components_used))
            topic = 'raw_data/material_transistor_in_stock'
            self.n_transistors -= components_used
            payload = self.n_transistors
        elif material_name == 'Capacitor':
            self.logger.info('Capacitor material consumed: {}'.format(components_used))
            topic = 'raw_data/material_capacitor_in_stock'
            self.n_capacitors -= components_used
            payload = self.n_capacitors
        elif material_name == 'Resistor':
            self.logger.info('Resistor material consumed: {}'.format(components_used))
            topic = 'raw_data/material_resistor_in_stock'
            self.n_resistors -= components_used
            payload = self.n_resistors
        else:
            self.logger.error('Material not found')

        self.client.publish(topic=topic, payload=payload, qos=1)
        return

    def handle_data(self):        
        """
        Starts the connection to MQTT broker and subscribe to respective
        topics.

        """
        
        self.logger.info('Preparing Mqtt Connection')
        try:
            self.client.username_pw_set(USERNAME, PASSWORD)
            self.client.connect(BROKER_ADDRESS)
            self.client.loop_start()
            self.logger.info('Subscribe to topic raw_data/material_consumption')
            self.subscribe(topic='raw_data/material_consumption', callback=self.material_consumption)
            self.logger.info('Finished subscription to topics')

        except Exception as e:
            self.logger.error(str(e))


if __name__ == '__main__':
    # configures basic logger
    logger = logging.getLogger( __name__ )
    logger.setLevel(logging.INFO)


