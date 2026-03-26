
from machine import Pin,PWM ,ADC, SPI,PWM, I2C
from time import sleep
import framebuf
import time 
#	from mfrc522 import MFRC522
import machine
import machine
import framebuf
import utime
import math
import random
import gc
import asyncio
import network
import socket
import uasyncio


class LCD_1inch14(framebuf.FrameBuffer):
    def __init__(self):
        self.width = 240
        self.height = 135
        
        self.cs = Pin(CS,Pin.OUT)
        self.rst = Pin(RST,Pin.OUT)
        
        self.cs(1)
        self.spi = SPI(1)
        self.spi = SPI(1,1000_000)
        self.spi = SPI(1,10000_000,polarity=0, phase=0,sck=Pin(SCK),mosi=Pin(MOSI),miso=None)
        self.dc = Pin(DC,Pin.OUT)
        self.dc(1)
        self.buffer = bytearray(self.height * self.width * 2)
        super().__init__(self.buffer, self.width, self.height, framebuf.RGB565)
        self.init_display()
        
        self.red   =   0x07E0
        self.green =   0x001f
        self.blue  =   0xf800
        self.white =   0xffff
        
        

    
        
    def write_cmd(self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)
        

    def write_data(self, buf):
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(bytearray([buf]))
        self.cs(1)
        

    def init_display(self):
        """Initialize dispaly"""  
        self.rst(1)
        self.rst(0)
        self.rst(1)
        
        self.write_cmd(0x36)
        self.write_data(0x70)

        self.write_cmd(0x3A) 
        self.write_data(0x05)

        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.write_data(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)

        self.write_cmd(0xB7)
        self.write_data(0x35) 

        self.write_cmd(0xBB)
        self.write_data(0x19)

        self.write_cmd(0xC0)
        self.write_data(0x2C)

        self.write_cmd(0xC2)
        self.write_data(0x01)

        self.write_cmd(0xC3)
        self.write_data(0x12)   

        self.write_cmd(0xC4)
        self.write_data(0x20)

        self.write_cmd(0xC6)
        self.write_data(0x0F) 

        self.write_cmd(0xD0)
        self.write_data(0xA4)
        self.write_data(0xA1)

        self.write_cmd(0xE0)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0D)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2B)
        self.write_data(0x3F)
        self.write_data(0x54)
        self.write_data(0x4C)
        self.write_data(0x18)
        self.write_data(0x0D)
        self.write_data(0x0B)
        self.write_data(0x1F)
        self.write_data(0x23)

        self.write_cmd(0xE1)
        self.write_data(0xD0)
        self.write_data(0x04)
        self.write_data(0x0C)
        self.write_data(0x11)
        self.write_data(0x13)
        self.write_data(0x2C)
        self.write_data(0x3F)
        self.write_data(0x44)
        self.write_data(0x51)
        self.write_data(0x2F)
        self.write_data(0x1F)
        self.write_data(0x1F)
        self.write_data(0x20)
        self.write_data(0x23)
        
        self.write_cmd(0x21)

        self.write_cmd(0x11)

        self.write_cmd(0x29)
        

    def show(self):
        self.write_cmd(0x2A)
        self.write_data(0x00)
        self.write_data(0x28)
        self.write_data(0x01)
        self.write_data(0x17)
        
        self.write_cmd(0x2B)
        self.write_data(0x00)
        self.write_data(0x35)
        self.write_data(0x00)
        self.write_data(0xBB)
        
        self.write_cmd(0x2C)
        
        self.cs(1)
        self.dc(1)
        self.cs(0)
        self.spi.write(self.buffer)
        self.cs(1)

class Point:
    def __init__(self,x,y):
        self.X=x
        self.Y=y
    def __str__(self):
        return "Point(%s,%s)"%(self.X,self.Y)
        
class Triangle:
    def __init__(self,p1,p2,p3):
        self.P1=p1
        self.P2=p2
        self.P3=p3

    def __str__(self):
        return "Triangle(%s,%s,%s)"%(self.P1,self.P2,self.P3)
    
    def draw(self):
        print("I should draw now")
        self.fillTri()
    # Filled triangle routines ported from http://www.sunshine2k.de/coding/java/TriangleRasterization/TriangleRasterization.html      
    def sortVerticesAscendingByY(self):    
        if self.P1.Y > self.P2.Y:
            vTmp = self.P1
            self.P1 = self.P2
            self.P2 = vTmp
        
        if self.P1.Y > self.P3.Y:
            vTmp = self.P1
            self.P1 = self.P3
            self.P3 = vTmp

        if self.P2.Y > self.P3.Y:
            vTmp = self.P2
            self.P2 = self.P3
            self.P3 = vTmp
        
    def fillTri(self):
        self.sortVerticesAscendingByY()
        if self.P2.Y == self.P3.Y:
            fillBottomFlatTriangle(self.P1, self.P2, self.P3)
        else:
            if self.P1.Y == self.P2.Y:
                fillTopFlatTriangle(self.P1, self.P2, self.P3)
            else:
                newx = int(self.P1.X + (float(self.P2.Y - self.P1.Y) / float(self.P3.Y - self.P1.Y)) * (self.P3.X - self.P1.X))
                newy = self.P2.Y                
                pTmp = Point( newx,newy )
#                print(pTmp)
                fillBottomFlatTriangle(self.P1, self.P2, pTmp)
                fillTopFlatTriangle(self.P2, pTmp, self.P3)



# async def webCom():
#     cl, addr = s.accept()
#     task2 = asyncio.create_task(RunLCD())

#     print('client connected from', addr)
#     request = cl.recv(1024)
#     request = str(request)
#     try:
#         filename = request.split(' ')[1]
#         if filename == '/':
#             filename = '/index.html'
#         serve_file(cl, '/' + filename)
#     except IndexError:
#         pass
#     cl.close()

def receive_data():
    global moisture
    global temperature
    global humidity
    received_data = []
    while uart.any():
        data = uart.read(1)
        received_data.append(data.decode())
    receive_sentence = "".join(received_data)
    data_blocks = receive_sentence.split()
    #print("full block is ", data_blocks)
    for block in data_blocks:
        if "%" in block:
            moisture = block
        elif "C" in block:
            temperature = block
        elif "&" in block:
            humidity = block
    data_blocks = ""

def colour(R,G,B): # Convert RGB888 to RGB565
    return (((G&0b00011100)<<3) +((B&0b11111000)>>3)<<8) + (R&0b11111000)+((G&0b11100000)>>5)

def clear(c):
    lcd.fill(c)

def fillBottomFlatTriangle(p1,p2,p3):
    
    #    print("BF",p1,p2,p3)
    if p2.Y > p3.Y:
        ty = p3.Y
        p3.Y = p2.Y
        p2.Y = ty
        tx = p3.X
        p3.X = p2.X
        p2.X = tx
        print(p1,p2,p3)
    
    slope1 = float(p2.X - p1.X) / float (p2.Y - p1.Y)
    slope2 = float(p3.X - p1.X) / float (p3.Y - p1.Y)

    x1 = p1.X
    x2 = p1.X + 0.5
    #    print("B",p1.Y,p2.Y)
    for scanlineY in range(p1.Y,p2.Y):
    #        print(scanlineY)
    #        lcd.pixel_span(int(x1), scanlineY, int(x2)-int(x1))   # Switch pixel_span() to hline() / Pimoroni to WS
        lcd.hline(int(x1),scanlineY, int(x2)-int(x1),c)        
        lcd.hline(int(x2),scanlineY, -(int(x2)-int(x1)),c)
        lcd.show()          #                  Here and below        
        utime.sleep(0.1)    #     <===== Uncomment to see how graphic elements are drawn
        x1 += slope1
        x2 += slope2
    #    lcd.show()              #                  lcd.show() and utime.sleep(0.1)

def fillTopFlatTriangle(p1,p2,p3):
    #    print("TF",p1,p2,p3)
    slope1 = float(p3.X - p1.X) / float(p3.Y - p1.Y)
    slope2 = float(p3.X - p2.X) / float(p3.Y - p2.Y)

    x1 = p3.X
    x2 = p3.X + 0.5
    #    print("T",p3.Y,p1.Y-1)
    for scanlineY in range (p3.Y,p1.Y-1,-1):
    #        print(scanlineY)
    #        lcd.pixel_span(int(x1), scanlineY, int(x2)-int(x1))  # Switch pixel_span() to hline() / Pimoroni to WS
        lcd.hline(int(x1),scanlineY, int(x2)-int(x1)+1,c)        
        lcd.hline(int(x2),scanlineY, -(int(x2)-int(x1)-1),c)
    #        lcd.show()
    #        utime.sleep(0.1)
        x1 -= slope1
        x2 -= slope2
        # lcd.show()            
# ============== End of Triangles Code ===============

# =========== New GFX Routines ============
def triangle(x1,y1,x2,y2,x3,y3,c): # Draw outline triangle
    lcd.line(x1,y1,x2,y2,c)
    lcd.line(x2,y2,x3,y3,c)
    lcd.line(x3,y3,x1,y1,c)
    
def tri_filled(x1,y1,x2,y2,x3,y3,c): # Draw filled triangle
 
    t=Triangle(Point(x1,y1),Point(x2,y2),Point(x3,y3)) # Define corners
    t.fillTri() # Call main code block  

def circle(x,y,r,c):
    lcd.hline(x-r,y,r*2,c)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i)) # Pythagoras!
        lcd.hline(x-a,y+i,a*2,c) # Lower half
        lcd.hline(x-a,y-i,a*2,c) # Upper half

def ring(x,y,r,c):
    lcd.pixel(x-r,y,c)
    lcd.pixel(x+r,y,c)
    lcd.pixel(x,y-r,c)
    lcd.pixel(x,y+r,c)
    for i in range(1,r):
        a = int(math.sqrt(r*r-i*i))
        lcd.pixel(x-a,y-i,c)
        lcd.pixel(x+a,y-i,c)
        lcd.pixel(x-a,y+i,c)
        lcd.pixel(x+a,y+i,c)
        lcd.pixel(x-i,y-a,c)
        lcd.pixel(x+i,y-a,c)
        lcd.pixel(x-i,y+a,c)
        lcd.pixel(x+i,y+a,c)

def Start():
    clear(0)
    lcd.show()
    lcd.text("WELCOME",90,2,colour(200,0,0))
    cc = colour(200,200,0)
    lcd.text("TO",108,30,cc) 
    lcd.text("THE",105,50,cc)     
    lcd.text("FUTURE",98,70,colour(255,255,255))
    lcd.text("OF",110,90,colour(150,75,0))
    lcd.text("AGRICULTURE",80,110,colour(0,255,0))

    lcd.show()
    utime.sleep(3)
    lcd.fill(0)

    # Built into framebuf library with the basic font
    lcd.rect(60,50,128,47,colour(255,0,0))
    lcd.show()
    utime.sleep(0.6)
    lcd.text("AGRIVISION",90,70,colour(0,255,0))
    lcd.show()


    # Circle & Ring
    c = colour(0,0,255)
    ring(120,67,65,c)
    lcd.show()
    utime.sleep(1)


    # Thread art
    for i in range(0,61,4):
        lcd.line(0,10+i,i,70,colour(255,255,0))
        lcd.show()
    utime.sleep(1)



    clear(0)




async def main():
    rfidtag = 0
    global current_page, moisture, humidity
    asyncio.create_task(web_server())  # Start the web server in the background
    
    lcd.text("AGRIVISION",80,2,colour(200,0,0))
    lcd.text(" future of agriculture ",30,10,colour(120,50,3))
    cc = colour(200,200,0)
    lcd.text("-FOR MORE INFO LOG INTO",30,40,cc) 
    lcd.text("WWW.AGRIVISION.ORG",50,50,cc)     
    lcd.text("-REGISTER RFID TO CONTINUE",15,80,colour(255,255,255))
    lcd.text("A = NEXT B = FIRSTPAGE",10, 120 ,colour(120,90,0))
    lcd.text("T P G INC",10,110,colour(0,255,0))
    lcd.show()
    
    if rfidtag == 0 :
        clear(0)
        lcd.text("RFID AUTHENTICATION COMPLETE",30,40,colour(255,255,255))
        lcd.text("COMPLETE",50,50,colour(255,255,255))
        lcd.show()
        current_page += 1
        
        while True :
            if current_page == 1:
                clear(0)
                lcd.text("MOISTURE",80,2,colour(200,0,0))
                lcd.text("ONLINE LOCATION MOISTURE DATA ",2,30,colour(120,50,3))
                lcd.text("variablename",40,40,cc)
                cc = colour(200,200,0)
                lcd.text("-MOISTURE DATA CURRENTLY",2,70,cc) 
                lcd.text(moisture,50,80,cc)     
                lcd.text("-keep a good moisture content of",2,100,colour(255,255,255))
                lcd.text("A = NEXT B = FIRSTPAGE",10, 125 ,colour(120,90,0))
                lcd.text("above 40%",2,110,colour(0,255,0))
                lcd.show()
                clear(0)
                if key0.value() == 0 :
                    current_page += 1
                    clear(0)
                    lcd.show()
                elif key1.value() == 0:
                    current_page -= 1
                    clear(0)
                    lcd.show()

                elif current_page == 2 :
                    lcd.text("LIGHT INTENSITY",80,2,colour(200,0,0))
                    lcd.text("ONLINE LIGHT DATA",2,30,colour(120,50,3))
                    lcd.text("variablename",40,40,cc)
                    cc = colour(200,200,0)
                    lcd.text("CURRENT LIGHT INTENSITY",2,70,cc) 
                    lcd.text("variablename",50,80,cc)    
                    lcd.text("-keep a good LIGHT INTENSITY",2,100,colour(255,255,255))
                    lcd.text("A = NEXT B = FIRSTPAGE",10, 125 ,colour(120,90,0))
                    lcd.text("above 40%",2,110,colour(0,255,0))
                    lcd.show()
                    if key0.value() == 0 :
                        current_page += 1
                        clear(0)
                        lcd.show()            
                elif key1.value() == 0:
                    current_page -= 1                 
                    clear(0)
                    lcd.show()            

            elif current_page == 3 :
                lcd.text("HUMIDITY",80,2,colour(200,0,0))
                lcd.text("ONLINE HUMIDITY DATA",2,30,colour(120,50,3))
                lcd.text("variablename",40,40,cc)
                cc = colour(200,200,0)
                lcd.text("CURRENT HUMIDITY STATUS",2,70,cc) 
                lcd.text(humidity,50,80,cc)     
                lcd.text("keep HUMIDITY LEVELS ",15,100,colour(255,255,255))
                lcd.text("A = NEXT B = FIRSTPAGE",10, 125 ,colour(120,90,0))
                lcd.text("above 40%",10,110,colour(0,255,0))
                
                lcd.show()
                if key0.value() == 0 :
                    current_page += 1
                    clear(0)
                    lcd.show()            
                elif key1.value() == 0:
                    current_page -= 1     
                    clear(0)
                    lcd.show()

            elif current_page == 4 :
                lcd.text("TEMPERATURE",80,2,colour(200,0,0))
                lcd.text(" ONLINE TEMPERATURE DATA ",2,30,colour(120,50,3))
                lcd.text("variablename",40,40,cc)
                cc = colour(200,200,0)
                lcd.text("CURRENT TEMPERAURE STATUS",2,70,cc) 
                lcd.text(temperature,50,80,cc)     
                lcd.text("keep a good TEMPERATURE of",15,100,colour(255,255,255))
                lcd.text("A = NEXT B = FIRSTPAGE",10, 125 ,colour(120,90,0))
                lcd.text("above 40%",10,110,colour(0,255,0))
                lcd.show()
                if key0.value() == 0 :
                    current_page += 1
                    clear(0)
                    lcd.show()            
                elif key1.value() == 0:
                    current_page -= 1     
                    clear(0)
                    lcd.show()

            elif current_page == 5 :
                lcd.text("ACTUATOR STATUS",80,2,colour(200,0,0))
                lcd.text(" future of agriculture ",50,10,colour(120,50,3))
                cc = colour(200,200,0)
                lcd.text("WATER PUMP-check blinking red led",1,30,cc) 
                lcd.text("HUMIDIFIER - coming soon",1,50,cc)     
                lcd.text("FAN -check constant BLUE LED ",2,70,colour(255,255,255))
                lcd.text("A = NEXT B = PREVIOUS",10, 120 ,colour(120,90,0))
                lcd.text("GREENHOUSE LIGHTS -coming soon",1,90,colour(0,255,0))
                lcd.show()
                if key0.value() == 0 :
                    current_page += 1
                    clear(0)
                    lcd.show()            
                elif key1.value() == 0:
                    current_page -= 1
                    clear(0)
                    lcd.show()

            elif current_page == 6 :
                lcd.text("AGRIVISION",80,2,colour(200,0,0))
                lcd.text(" future of agriculture ",30,10,colour(120,50,3))
                cc = colour(200,200,0)
                lcd.text("WEATHER PREDICTION TODAY",1,40,cc) 
                lcd.text("VARIABLENAME",1,55,cc)     
                lcd.text("AI",1,80,colour(255,255,255))
                lcd.text("A = NEXT B = PREVIOUS",10, 120 ,colour(120,90,0))
                lcd.text("",1,90,colour(0,255,0))
                lcd.show()
                if key1.value () == 0 :
                    current_page -= 1
                    clear(0)
                    lcd.show()
                    
            
            
            await asyncio.sleep(1)
            receive_data()
            utime.sleep(1)
            print("moistrue", moisture)
            print("temp", temperature)
            print("humidity", humidity, "\n")

            asyncio.create_task(web_server())  # Start the web server in the background
            asyncio.create_task(UpdateData())  # Start the web server in the background






#button debouncer
button_press = False
debouncer = 200

#for program state
STATE_INIT = 0
STATE_RUNNING = 1
STATE_BUTTON_PRESSEND = 2
state = STATE_INIT

#lcd declarations
BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10    
CS = 9

#uart communication declaration
uart = machine.UART(0,9600, tx = machine.Pin(0), rx = machine.Pin(1))
uart_tx = machine.Pin(0)
uart_rx = machine.Pin(1)

#rfid declarations
sda = machine.Pin(20, machine.Pin.OUT)
sck = machine.Pin(18, machine.Pin.OUT)
mosi = machine.Pin(19, machine.Pin.OUT)
miso = machine.Pin(16, machine.Pin.OUT)
rst = machine.Pin(26, machine.Pin.OUT)

#LCD buttons declarations
key0 = Pin(15,Pin.IN,Pin.PULL_UP) # Normally 1 but 0 if pressed
key1 = Pin(7,Pin.IN,Pin.PULL_UP)

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

width = 240
height = 135

#receiving data from field pico
moisture = ""
temperature = ""
humidity = ""

key1.value() == 1
key0.value() == 1
pages = 0

current_page = 0
        
#pump pins and declaration

PumpStatus = "Off"
Pump =  machine.Pin(2 ,machine.Pin.OUT)

lcd = LCD_1inch14()


lcd.show()
Start()
#WebStart()
uasyncio.run(main())
    