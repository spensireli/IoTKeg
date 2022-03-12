import datetime
import sys
import time
import serial
import json
import logging

# Configure Logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


class Moist():
    def __init__(self):
        self.data = []
    
    def getMoisture(self, serial_port, baudrate, component):
        moistureSensor = serial.Serial(port=serial_port, baudrate=baudrate, timeout=.1)
        moisture = []
        moisture_percent_average = []
        while True:
            data = moistureSensor.readline()
            if data:
                moisture.append(data.decode().strip())
                if len(moisture) == 10:
                    break
        for x in moisture:
            try:
                loaded = json.loads(x)
                device = loaded.get('device')
                percent = float(loaded.get('percent'))
                moisture_percent_average.append(percent)
            except Exception as e:
                log.debug(e)           
        avg = sum(moisture_percent_average) / len(moisture_percent_average)
        payload = {
            "device": device,
            "moisture_percent": float(round(avg, 2))
        }
        return(payload)



# if __name__ == "__main__":
#     print(Moist().getMoisture('/dev/ttyACM2', 9600, 'moisture_sensor'))