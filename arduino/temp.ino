#include <OneWire.h>
#include <DallasTemperature.h>

#define ONE_WIRE_BUS 2
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);


uint8_t sensor1[8] = { 0x28, 0x5A, 0xB1, 0x96, 0xF0, 0x01, 0x3C, 0xC1 };
uint8_t sensor2[8] = { 0x28, 0xAE, 0x40, 0x96, 0xF0, 0x01, 0x3C, 0x04 };
void setup(void)
{
  Serial.begin(9600);
  sensors.begin();
}

void loop(void)
{
  sensors.requestTemperatures();
  
  Serial.print("{ \"device\": \"dev1\", \"temp\": ");
  printTemperature(sensor1);
  Serial.println(" }");

  Serial.print("{ \"device\": \"dev2\", \"temp\": ");
  printTemperature(sensor2);
  Serial.println(" }");

  Serial.println();
  delay(1000);
}

void printTemperature(DeviceAddress deviceAddress)
{
  float tempC = sensors.getTempC(deviceAddress);
  Serial.print(tempC);
}