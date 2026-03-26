from machine import Pin,ADC
from time import sleep
import utime


soil_moisture_sensor= ADC(1)     # GPIO PIN USED BY SENSOR AS INPUT DATA TO PICO\
Pump = Pin(15,Pin.OUT)
while True:
    moisturedata = soil_moisture_sensor.read_u16()
    moisturedatapercent = round((moisturedata/65000)*100)
    
    moisturedata=soil_moisture_sensor.read_u16()  # capture data into variable moisturedata
    if moisturedata>50000:                # conditions on when to turn on pump
        print("Of")
        Pump.value(0)
        
    elif moisturedata<20000:
        print("on")
        Pump.value(1)
        
    print(moisturedata)  # show data from moisture sensor 
    print(moisturedatapercent,"%")
    utime.sleep(1.25)
    
