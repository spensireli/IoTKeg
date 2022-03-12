import datetime
import sys
import time
import serial
import json
import logging

# Configure Logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)


class Temp():
    def __init__(self):
        self.data = []
    
    def getTemp(self, measure, serial_port, baudrate, component, ttl):
        time_to_live = datetime.datetime.utcnow() + datetime.timedelta(hours=ttl)
        time_to_live = time.mktime(time_to_live.timetuple())
        time_to_live = int(time_to_live)
        tempSensor = serial.Serial(port=serial_port, baudrate=baudrate, timeout=.1)
        temp = []
        dev1_temp = []
        dev2_temp = []
        while True:
            data = tempSensor.readline()
            if data:
                temp.append(data.decode().strip())
                if len(temp) == 10:
                    break
        for x in temp:
            try:
                loaded = json.loads(x)
                device = loaded.get('device')
                if device == 'dev1':
                    dev1_temp.append(loaded.get('temp'))
                if device == 'dev2':
                    dev2_temp.append(loaded.get('temp'))
            except Exception as e:
                log.debug(e)
        
        dev1_avg = sum(dev1_temp) / len(dev1_temp)
        dev2_avg = sum(dev2_temp) / len(dev2_temp)
        # avg = sum(temp) / len(temp)
        if measure == 'f':
            dev1_temp = (dev1_avg * 1.8) + 32
            dev2_temp = (dev2_avg * 1.8) + 32
            payload = {
                "component": component,
                "dev1_temperature":round(dev1_temp, 2),
                "dev2_temperature":round(dev2_temp, 2),
                "measurement":"F",
                "ttl":time_to_live
            }
            return(payload)
        else:
            payload = {
                "component": component,
                "dev1_temperature":round(dev1_avg, 2),
                "dev2_temperature":round(dev2_avg, 2),
                "measurement":"F",
                "ttl":time_to_live
            }
            return(payload)

# if __name__ == "__main__":
#     temperature = Temp().getTemp(measure='f', serial_port='/dev/ttyACM0', baudrate=9600, component='Keg', ttl=1)
#     log.(temperature)