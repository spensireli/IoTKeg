# IoTKeg - WIP
Inspired by AWS Simple Beer Service, but utilizes AWS IoT with MQTT, AWS GreenGrass Core, AWS Timestream, and AWS CloudWatch. 

This application collects telemetry data from a number of arduino sensors and sends them to AWS IoT via MQTT using AWS GreenGrass Core.
Once receieved AWS IoT processes the data via a time series database (AWS Timestream) to be used for further analysis & application. Additionally
during this process metrics are posted to AWS CloudWatch for temperature, moisture, and remaining volume. 

