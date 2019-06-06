# echowemoclient
Home IOT system on Raspberry pi with Amazon echo dot

###function
+ Turn On Computer with Bluetooth (check /IOT_Client)
+ Turn Off Computer with MQTT (check /IOT_Client) 
+ Control sonoff by Touch Sensor
+ Turn On/Off Aircon with IR Transmitter/Receiver 

# How to use
1. Make Virtualenv (python2.7)
    > python -m virtualenv ecvenv
2. Activate Virtualenv
    > source ecvenv/bin/activate
3. install lib
    > pip install -r requirements.txt
3. Start Code
    > ./start.sh 
    
    or
    
    >python example-minimal.py
    


# IOT_Client Directory
IOT Client Code (Arduino)
+ Turn Off Desktop Window Service Code
+ Arduino Code of Computer Turn On

# USE GPIO 

+ GPIO 4 - INPUT - Touch Sensor
    + One touch - Sonoff Control
+ GPIO 17 - OUTPUT - 5MM LED 
+ GPIO 18 - INPUT - IR Receiver
+ GPIO 22 - OUTPUT - IR Transmitter
