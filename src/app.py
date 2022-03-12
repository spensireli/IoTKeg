import serial
import json
import sys
import os
import concurrent.futures
from lcd import Lcd
from temp import Temp
from moisture import Moist
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import logging


logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

clientDevice = os.environ.get('CLIENT_DEVICE')
clientEndpoint = os.environ.get('CLIENT_ENDPOINT')
rootCA = os.environ.get('ROOT_CA_PATH')
privateKey = os.environ.get('PRIVATE_KEY_PATH')
cert = os.environ.get('CERTIFICATE_PATH')



def print_to_std_out(*a):
    print(*a, file = sys.stdout)

if __name__ == "__main__":

    # Initialize LCD
    init_board = Lcd.initialize_board(board='/dev/ttyACM0')


    # Init MQTT for AWS IoT.
    myMQTTClient = AWSIoTMQTTClient("keg")
    myMQTTClient.configureEndpoint("a1v1dnmlrpmwkw-ats.iot.us-east-1.amazonaws.com", 8883)
    myMQTTClient.configureCredentials("/home/spensireli/AmazonRootCA1.ca", "/home/spensireli/privatekey.pem", "/home/spensireli/certificate.cer")
    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    myMQTTClient.connect()



    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     futureTemp = executor.submit(Temp().getTemp, 'f', '/dev/ttyACM0', 9600, 'Keg', 1)
    #     return_value_temp = futureTemp.result()
    #     print(return_value_temp)
    #     futureMoisture = executor.submit(Moist().getMoisture, '/dev/ttyACM2', 9600, 'moisture_sensor')
    #     return_value_moisture = futureMoisture.result()
    #     print(return_value_moisture)




    while True:
        try:
            # with concurrent.futures.ThreadPoolExecutor() as executor:
            #     futureTemp = executor.submit(Temp().getTemp, 'f', '/dev/ttyACM0', 9600, 'Keg', 1)
            #     return_value_temp = futureTemp.result()
            #     futureMoisture = executor.submit(Moist().getMoisture, '/dev/ttyACM2', 9600, 'moisture_sensor')
            #     return_value_moisture = futureMoisture.result()

            return_value_moisture = Moist().getMoisture('/dev/ttyACM1', 9600, 'moisture_sensor')
            return_value_temp = Temp().getTemp('f', '/dev/ttyACM2', 9600, 'Keg', 1)
            log.info(return_value_moisture)
            log.info(return_value_temp)

            moisture_percent = return_value_moisture.get('moisture_percent')
            moisture_percent = float(moisture_percent)

            return_value_temp['moisture_percent'] = moisture_percent

            toDynamo = {"state":{"reported":return_value_temp}}
            log.info(toDynamo)
            textMeas = toDynamo.get('state').get('reported').get('measurement')
            textComp = toDynamo.get('state').get('reported').get('component')
            dev1_textTemp = round(toDynamo.get('state').get('reported').get('dev1_temperature'))
            dev2_textTemp = round(toDynamo.get('state').get('reported').get('dev2_temperature'))
            toDynamo = json.dumps(toDynamo)
            text = f'{textComp}: Tower:{dev2_textTemp}{textMeas} Fridge:{dev1_textTemp}{textMeas}'
            log.info(text)
            write_text = Lcd.write_text(init_board, text=text)
            log.debug(write_text)
            publish = myMQTTClient.publish("$aws/things/keg/shadow/name/keg/update", toDynamo, 0)
            log.info(publish)
            # time.sleep(60)
        except Exception as e:
            log.debug(e)
        # publish = myMQTTClient.publish("$aws/things/keg/shadow/name/keg/update", toDynamo, 0)
        # publish = myMQTTClient.publishAsync("$aws/things/keg/shadow/name/keg/update", toDynamo, 0)
        # Dont think I need to disconnect because its going to send forever. 
        # myMQTTClient.disconnect()

