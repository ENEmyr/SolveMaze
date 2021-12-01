from configs import MQTTConfig
import paho.mqtt.client as mqtt
from collections.abc import Callable
from typing import Union

MQTT_CONF = MQTTConfig()

class Client:
    def __init__(self, 
            broker:str=MQTT_CONF.Broker,
            port:int=MQTT_CONF.Port,
            subs:dict=MQTT_CONF.SubTopics,
            pubs:dict=MQTT_CONF.PubTopics,
            username:str=MQTT_CONF.Username,
            password:str=MQTT_CONF.Password,
            qos:int=MQTT_CONF.Qos,
            keepalive:int=MQTT_CONF.Keepalive):
        self.broker = broker
        self.port = int(port)
        self.username = username
        self.password = password
        self.qos = int(qos)
        self.keepalive = int(keepalive)
        self.subs = subs
        self.pubs = pubs
        self.client = mqtt.Client('SolveMazeBot')
        self.client.username_pw_set(self.username, self.password)
        self.client.connect(self.broker, self.port, self.keepalive)
        self.client.on_message = self.__on_data
        self.subs_val = dict()
        topics_lst = []
        for topic in self.subs.keys():
            topics_lst.append((self.subs[topic], self.qos))
        [status, msg_id] = self.client.subscribe(topics_lst)
        self.subs_val['angulardistance'] = None
        # if len(self.subs) != 0:
        #     for ch in subs: 
        #         self.subs_val[ch] = None
        print(f'Subscribe status: {status}, with message id: {msg_id}')

    def sub(self, topics:list=[]) -> dict:
        ret_dict = dict()
        for topic in topics:
            if len(self.subs_val) == 0:
                break
            if topic == None:
                continue
            if topic.lower() in dict(self.subs).keys():
                ret_dict[topic] = self.subs_val[topic.lower()]
            elif topic.lower() in dict(self.subs).values():
                ret_dict[topic] = self.subs_val[topic.lower()]
        return ret_dict

    def pub(self, topics_payload_pair:dict, verbose:bool=False) -> bool:
        for topic in topics_payload_pair.keys():
            result = self.client.publish(topic, topics_payload_pair[topic], self.qos)
            if verbose:
                if result[0] == 0:
                    print(f'Publish to topic: {topic} successfully.')
                else:
                    print(f'Failed to publish to topic: {topic}.')
        return True if result == 0 else False

    def __on_data(self, topic, payload):
        if payload:
            self.subs_val[str(topic)] = payload
        else:
            self.subs_val[str(topic)] = None

    def __get_subs_key(self, target_val:str) -> Union[str, int]:
        try:
            for key in dict(self.subs):
                if self.subs[key] == target_val:
                    return key
        except Exception as e:
            print(e)

