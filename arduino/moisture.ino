#define SensorPin A0 
float sensorValue = 0; 

const int dry = 610;
const int wet = 380;

void setup() { 
 Serial.begin(9600); 
} 
void loop() { 
 for (int i = 0; i <= 100; i++) 
 { 
   sensorValue = sensorValue + analogRead(SensorPin); 
   delay(1); 
 } 
 sensorValue = sensorValue/100.0;
 int percentageHumidty = map(sensorValue, wet, dry, 100, 0);
 Serial.print("{ \"device\": \"moisture_sensor\", \"percent\": ");
 Serial.print(percentageHumidty);
 Serial.println(" }");
 
 delay(1000); 
} 