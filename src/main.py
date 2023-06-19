from .dropper import Dropper
import paho.mqtt.client as mqtt
from dotenv import dotenv_values
import time
import signal
import sys
import random

config = dotenv_values(".env")

class Simulator:
    droppers: list[Dropper] = []
    isRunning: bool = False
    def __init__(self):
        self.droppers = []
        self.mqttClient = mqtt.Client()
        self.mqttClient.connect(config["MQTT_HOST"], int(config["MQTT_PORT"]), 60)

    def initDroppers(self):
        if (config["DROPPER_RUN"] == "true"):
            dropperSerials = config["DROPPER_SERIALS"].split(",")
            if (len(dropperSerials) > 0):
                for serial in dropperSerials:
                    self.droppers.append(Dropper(self.mqttClient, serial))
            else:
                for i in range(0, 10):
                    self.droppers.append(Dropper(self.mqttClient, None))

    def cleanup(self, signal, frame):
        print("Cleaning up...")
        for dropper in self.droppers:
            dropper.cleanup()
        self.isRunning = False
        sys.exit(0)

    def run(self):
        self.isRunning = True
        signal.signal(signal.SIGINT, self.cleanup)
        while (self.isRunning):
            randomDropper = random.choice(self.droppers)
            randomDropper.handDropCycleEvent()
            time.sleep(1)

def main():
    simulator = Simulator()
    simulator.run()

