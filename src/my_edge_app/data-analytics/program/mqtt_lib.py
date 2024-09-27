import paho.mqtt.client as mqtt
import logging
from typing import Callable, Any

class MQTTClient:
    """
    Easy-to-use MQTT client for connecting to an MQTT broker and subscribing
    to topics. Use the subscribe method to configure a callback event handler method
    for receiving messages sent to the given topic.
    """
    def __init__(self, broker_address : str, broker_port : int, username : str, password : str, client_id: str = "MQTT_Client") -> None:
        """
        Constructs a new MQTTClient and starts the MQTT broker.

        :param broker_address: Hostname or address of the MQTT broker.
        :param broker_port: Port of the MQTT broker.
        :param username: Broker username for authentication.
        :param password: Broker password for authentication.
        :param client_id: Client ID for the MQTT connection (default is "MQTT_Client").
        """
        self._logger = logging.getLogger( __name__ )
        self._logger.setLevel(logging.INFO)
        self._topic_callback = dict()
        self._client = mqtt.Client(client_id)
        self._client.on_connect = self._on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_subscribe = self._on_subscribe
        self._client.on_message = self._on_message
        self._start_mqtt_broker(broker_address, broker_port, username, password)
        
    def subscribe(self, topic : str, callback : Callable[[mqtt.MQTTMessage], None]) -> None:
        """ Subscribes to given topic, assigning a callback function that
        handles the received MQTT message.

        :param topic: String with the topic to subscribe
        :param callback: Function to handle messages received on the topic. This function must accept
                 one parameter (an `MQTTMessage` object) and return `None`.
        """
        self._topic_callback.update({topic:callback})
        self._client.subscribe(topic)

    def publish(self, topic : str, payload : str, qos : int = 0, retain : bool = False) -> None:
        """ Publishes a message to the given topic.

        :param topic: String with the topic to publish
        :param payload: String with the message to publish
        :param qos: Quality of Service level (default is 0)
        :param retain: Retain flag (default is False)
        """
        self._client.publish(topic, payload, qos, retain)
        
    def _start_mqtt_broker(self, broker_address: str, broker_port: int, username: str, password: str) -> None:
        try:
            self._client.username_pw_set(username, password)
            self._client.connect(broker_address, broker_port)
            self._client.loop_start()
        except Exception as e:
            self._logger.error(str(e))
        
    def _on_connect(self, _client: mqtt.Client, userdata: Any, flags: dict, rc: int) -> None:
        self._logger.info('Connected successfully to broker, response code {}'.format(rc))

    def _on_disconnect(self, _client: mqtt.Client, userdata: Any, rc: int) -> None:
        if rc != 0:
            self._logger.warning('Connection ended unexpectedly from broker, error code {}'.format(rc))

    def _on_subscribe(self, _client: mqtt.Client, userdata: Any, mid: int, granted_qos: list) -> None:
        self._logger.info('Successfully subscribed')
        
    def _on_message(self, client: mqtt.Client, userdata: Any, message: mqtt.MQTTMessage) -> None:
        self._logger.info('New message received on topic: {}'.format(message.topic))
        try:
            if message.topic in self._topic_callback:
                self._topic_callback[message.topic](message)
            else:
                self._logger.warning('No callback registered for topic: {}'.format(message.topic))
        except Exception as err:
            self._logger.error('An error occurred while handling new message of {}: {}'.format(message.topic, err))
