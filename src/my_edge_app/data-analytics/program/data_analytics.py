# Copyright 2021 Siemens AG
# This file is subject to the terms and conditions of the MIT License.  
# See LICENSE file in the top-level directory.

"""Module Data Analytics.

This module consists of DataGenerator class and also the function to generate
bivariate normal distributed datasets.

"""

from mqtt_lib import MQTTClient
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
        self.client = MQTTClient(BROKER_ADDRESS, BROKER_PORT, USERNAME, PASSWORD, MICRO_SERVICE_NAME)

        # number of components
        self.n_transistors = 100
        self.n_capacitors = 200
        self.n_resistors = 300
    
    def material_consumption(self, message):
        self.logger.info('calculating pick and place machine...')
        # unpickle the payload
        payload = message.payload
        material_name, components_used = pickle.loads(payload)
        topic = 'raw_data/material_consumption'

        if material_name == 'Transistor':
            self.logger.info('Transistor material consumed: {}'.format(components_used))
            topic = 'raw_data/material_transistors_in_stock'
            self.n_transistors -= components_used
            payload = self.n_transistors
        elif material_name == 'Capacitor':
            self.logger.info('Capacitor material consumed: {}'.format(components_used))
            topic = 'raw_data/material_capacitors_in_stock'
            self.n_capacitors -= components_used
            payload = self.n_capacitors
        elif material_name == 'Resistor':
            self.logger.info('Resistor material consumed: {}'.format(components_used))
            topic = 'raw_data/material_resistors_in_stock'
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
            self.logger.info('Subscribe to topic raw_data/material_consumption')
            self.client.subscribe('raw_data/material_consumption', self.material_consumption)
            self.logger.info('Finished subscription to topics')

        except Exception as e:
            self.logger.error(str(e))


if __name__ == '__main__':
    # configures basic logger
    logger = logging.getLogger( __name__ )
    logger.setLevel(logging.INFO)


