import paho.mqtt.client as mqtt
import json
from enum import Enum
from typing import Optional
import os
import binascii
import random
from threading import Timer

class DropperEvent(Enum):
    SENSOR_FAILURE = -10,
    UPDATE_FAILED = -6,
    BOOTING = 0,
    DELIVERY_REQUEST = 1,
    DELIVERED = 2,
    PRIME_REQUEST = 3,
    PRIMED = 4,
    UPDATE_REQUEST = 5,
    UPDATE_OK = 6

class Dropper:
    messagesCount: int = 0
    cycles: int = 0
    timer: Optional[Timer] = None
    serial: str

    @staticmethod
    def generateSerial():
        return "GKDP-" + binascii.b2a_hex(os.urandom(6)).upper().decode()[:1]

    def cleanup(self):
        if (self.timer is not None):
            self.timer.cancel()

    def __init__(self, mqttClient: mqtt.Client, serial: Optional[str]):
        self.mqttClient = mqttClient
        if (serial is None):
            self.serial = Dropper.generateSerial()
        else:
            if not serial.startswith("GKDP-"):
                raise ValueError("Dropper serial must start with GKDP-")
            self.serial = serial
            print("Dropper serial: " + self.serial)

    def send(self, topic: str, payload: str, qos: int = 0, retain: bool = False):
        self.mqttClient.publish(topic, payload, qos, retain)
        self.messagesCount += 1

    def report(self, event: DropperEvent):
        if (DropperEvent.DELIVERED == event):
            self.cycles += 1
        jsonEvent = json.dumps({
            "cycle": self.cycles,
            "doses": self.cycles,
            "event": event.value,
        })
        self.send("Dropper/" + self.serial + "/report", jsonEvent, 1)

    def handDropCycleEvent(self):
        self.report(DropperEvent.DELIVERY_REQUEST)
        if (self.timer is not None):
            print("Dropper {self.serial} Canceling timer")
            self.timer.cancel()
        self.timer = Timer(random.uniform(0.5, 3.0), self.report, [DropperEvent.DELIVERED])
        self.timer.start()