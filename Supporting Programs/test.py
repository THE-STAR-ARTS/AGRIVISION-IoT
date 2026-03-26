from machine import Pin,PWM ,ADC, SPI,PWM, I2C
from time import sleep
import framebuf
import time 
#from mfrc522 import MFRC522
import machine
import utime

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
key1 = Pin(22,Pin.IN,Pin.PULL_UP)
key2 = Pin(2,Pin.IN,Pin.PULL_UP)
key3 = Pin(3,Pin.IN,Pin.PULL_UP)

#RGB AGRIVISION
rgbled =  machine.Pin(7, machine.Pin.OUT )

#buzzer declaration
buzzer = machine.Pin(16,machine.Pin.OUT)

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
lightintensity = ""

IpAddress = "192.168.4.1"

#UART PROGRAM
def receive_data():
    global moisture, temperature, humidity

    if not uart.any():
        return

    try:
        received_data = uart.read().decode().strip()
        data_blocks = received_data.split()

        for block in data_blocks:
            if "%" in block:
                moisture = block
            elif "C" in block:
                temperature = block
            elif "&" in block:
                humidity = block

    except Exception as e:
        print("UART receive error:", e)

def buzzersound():
    buzzer.value(1)
    utime.sleep(0.1)
    buzzer.value(0)

#button debouncer
button_press = False
debouncer = 200

#for program state
STATE_INIT = 0
STATE_RUNNING = 1
STATE_BUTTON_PRESSEND = 2
state = STATE_INIT

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

lcd = LCD_1inch14()

def colour(R,G,B): # Convert RGB888 to RGB565
    return (((G&0b00011100)<<3) +((B&0b11111000)>>3)<<8) + (R&0b11111000)+((G&0b11100000)>>5)

def clear(c):
    lcd.fill(c)

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
        lcd.hline(int(x1),scanlineY, int(x2)-int(x1),cc)        
        lcd.hline(int(x2),scanlineY, -(int(x2)-int(x1)),cc)
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
        lcd.hline(int(x1),scanlineY, int(x2)-int(x1)+1,cc)        
        lcd.hline(int(x2),scanlineY, -(int(x2)-int(x1)-1),cc)
#        lcd.show()
#        utime.sleep(0.1)
        x1 -= slope1
        x2 -= slope2
#    lcd.show()            
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

def vline(self, x, y, length, color):
        
        self.fill_rect(x, y, 1, length, color)
        self.fill_rect(x, y, length, 1, color)

#def fill_rect(self, x, y, width, height, color)

# =============================== Main lcd code=======================================================================================================
# startup screen
clear(0)
utime.sleep(1)
lcd.show()
lcd.hline(0,95,240,colour(0,0,0))
lcd.vline(59,0,240,colour(0,0,0))
lcd.vline(190,0,240,colour(0,0,0))
lcd.hline(0,50,240,colour(0,0,0))
lcd.fill_rect(0,50,59,45,colour(0,0,125))#the middle left 
lcd.fill_rect(190,50,59,45,colour(0,0,125)) # the middle right 
lcd.fill_rect(190,0,59,45,colour(255,0,0))# the right top
lcd.fill_rect(190,95,59,45,colour(255,0,0))# the bottom right
lcd.fill_rect(0,0,59,47,colour(0,0,255)) # the top left center
lcd.fill_rect(0,95,59,47,colour(0,0,255)) # the bottom left 
lcd.fill_rect(60,0,128,47,colour(0,255,0))# the top middle
lcd.fill_rect(60,95,128,47,colour(0,255,0))#the bottom middle 
lcd.fill_rect(60,50,128,47,colour(0,0,0)) # the center

lcd.text("T P 6 INC.",90,70,colour(0,255,0))
lcd.show()
utime.sleep(3)
lcd.fill(0)

# Built into framebuf library with the basic font
lcd.fill_rect(0,0,240,135,colour(0,182,0))
lcd.text("AGRIVISION", 70, 65, colour(255, 255, 255))
lcd.show()
utime.sleep(0.5)

for i in range(0, 129, 8):  # Progress from 0 to 128 in steps of 8
    lcd.fill_rect(50, 80, i, 20, colour(255,0,0))  # Animate fill
    lcd.show()
    utime.sleep(0.1)

clear(0)
lcd.show()

key1.value() == 1
key0.value() == 1

Loaded = False

current_page = 1
while True :
    receive_data()
    if current_page == 1:
        if not Loaded:
            lcd.hline(0,95,240,colour(255,255,255))
            lcd.hline(0,35,240,colour(255,255,255))
            lcd.hline(0,76,240,colour(255,255,255))
            lcd.fill_rect(0,0,240,35 , colour(0,128,0 ) )
            lcd.fill_rect(0,35,240,60 , colour(0,0,128 ) )
            lcd.fill_rect(0,95,240,45,colour(255,0,0 ) )
            lcd.text("A G R I V I S I O N",40,2,colour(255,255,255))
            lcd.text("FUTURE OF AGRICULTURE",33,15,colour(255,255,255))
            lcd.text("FOR MORE INFO LOG INTO",0,40,colour(255,255,255))
            lcd.text(IpAddress,0,50,colour(255,0,0))
            lcd.text("CONNECTED TO -",0,70,colour(255,255,255))
        cc = colour(200,200,0)
        lcd.text("T P G INC",10,120,colour(0,255,0))
        lcd.show()
        Loaded = True
        if key0.value() == 0 :
            buzzersound()
            current_page += 1
            clear(0)
            lcd.show()
            Loaded = False
        
            
    elif current_page == 2 :
        if not Loaded:
            lcd.hline(0,95,240 , colour(0,0,0 ) )
            lcd.fill_rect(0 , 0 ,240,130 , colour(0,190,0 ) )
            lcd.fill_rect(30,0, 110 , 20 , colour ( 255 , 255 , 255 ) )
            lcd.fill_rect(60,80,80,20,colour(255,255,255))
            lcd.fill_rect(190,0 , 70 , 140 , colour(255,255,255 ) )
            lcd.text("PAGE 2",192,70,colour(0,0,0))
            lcd.text("MOISTURE",55,2,colour(200,0,0))
            cc = colour(200,200,0)
            lcd.text("CURRENT MOISTURE DATA",10,70,colour(255,255,255)) 
            lcd.text(moisture,80,85,cc)     
            lcd.text("NEXT=>",192, 10 ,colour(0,0,0))
            lcd.text("BACK=>",192, 115, colour (0,0,0)) 
            lcd.text("T P G INC",10,120,colour(0,255,0))   
            lcd.show()
            Loaded = True
        if key0.value() == 0 :
            buzzersound()
            current_page += 1
            clear(0)
            lcd.show()
            Loaded = False
        elif key1.value() == 0:
            buzzersound()
            current_page -= 1
            clear(0)
            lcd.show()
            Loaded = False
            
    elif current_page == 3 :
        lcd.hline(0,95,240 , colour(0,0,0 ) )
        lcd.fill_rect(0 , 0 ,240,130 , colour(255,105,180 ) )
        lcd.fill_rect(30,0, 110 , 20 , colour ( 255 , 255 , 255 ) )
        lcd.fill_rect(60,80,80,20,colour(255,255,255))
        lcd.fill_rect(190,0 , 70 , 140 , colour(255,255,255 ) )
        lcd.text("PAGE 3",192,70,colour(0,0,0))
        lcd.text("TEMPERATURE",45,2,colour(200,0,0))
        cc = colour(200,200,0)
        lcd.text("TEMPERATURE DATA",30,70,colour(255,255,255)) 
        lcd.text(temperature,80,85,cc)     
        lcd.text("NEXT=>",192, 10 ,colour(0,0,0))
        lcd.text("BACK=>",192, 115, colour (0,0,0))   
        lcd.text("T P G INC",10,120,colour(0,255,0)) 
        lcd.show()
        Loaded = True
        if key0.value() == 0 :
            buzzersound()
            current_page += 1
            clear(0)
            lcd.show()
            Loaded = False
        elif key1.value() == 0:
            buzzersound()
            current_page -= 1
            clear(0)
            lcd.show()  
            Loaded = False              
            
    elif current_page == 4 :
        if not Loaded:
            lcd.hline(0,95,240 , colour(0,0,0 ) )
            lcd.fill_rect(0 , 0 ,240,130 , colour(128,0,128 ) )
            lcd.fill_rect(30,0, 110 , 20 , colour ( 255 , 255 , 255 ) )
            lcd.fill_rect(60,80,80,20,colour(255,255,255))
            lcd.fill_rect(190,0 , 70 , 140 , colour(255,255,255 ) )
            lcd.text("PAGE 4",192,70,colour(0,0,0))
            lcd.text("HUMIDITY",55,2,colour(200,0,0))
            cc = colour(200,200,0)
            lcd.text("CURRENT HUMIDITY DATA",10,70,colour(255,255,255)) 
            lcd.text(humidity,80,85,cc)     
            lcd.text("NEXT=>",192, 10 ,colour(0,0,0))
            lcd.text("BACK=>",192, 115, colour (0,0,0))  
            lcd.text("T P G INC",10,120,colour(0,255,0))  
            lcd.show()
            Loaded = True
        if key0.value() == 0 :
            buzzersound()
            current_page += 1
            clear(0)
            lcd.show()
            Loaded = False
        elif key1.value() == 0:
            buzzersound()
            current_page -= 1
            clear(0)
            lcd.show()
            Loaded = False     

    elif current_page == 5 :
        if not Loaded:
            lcd.hline(0,95,240 , colour(0,0,0 ) )
            lcd.fill_rect(0 , 0 ,240,130 , colour(128,128,128 ) )
            lcd.fill_rect(30,0, 110 , 20 , colour ( 255 , 255 , 255 ) )
            lcd.fill_rect(60,80,80,20,colour(255,255,255))
            lcd.fill_rect(190,0 , 70 , 140 , colour(255,255,255 ) )
            lcd.text("PAGE 5",192,70,colour(0,0,0))
            lcd.text("MOISTURE",55,2,colour(200,0,0))
            cc = colour(200,200,0)
            lcd.text("CURRENT MOISTURE DATA",10,70,colour(255,255,255)) 
            lcd.text(moisture,80,85,cc)     
            lcd.text("NEXT=>",192, 10 ,colour(0,0,0))
            lcd.text("BACK=>",192, 115, colour (0,0,0))   
            lcd.text("T P G INC",10,120,colour(0,255,0)) 
            lcd.show()
            Loaded = True
        if key0.value() == 0 :
            buzzersound()
            current_page += 1
            clear(0)
            lcd.show()
            Loaded = False
        elif key1.value() == 0:
            buzzersound()
            current_page -= 1
            clear(0)
            lcd.show()    
            Loaded = False

    elif current_page == 6 :
        if not Loaded:
            lcd.hline(0,95,240 , colour(0,0,0 ) )
            lcd.fill_rect(0 , 0 ,240,130 , colour(255,0,0 ) )
            lcd.fill_rect(30,0, 110 , 20 , colour ( 255 , 255 , 255 ) )
            lcd.fill_rect(60,80,80,20,colour(255,255,255))
            lcd.fill_rect(190,0 , 70 , 140 , colour(255,255,255 ) )
            lcd.text("PAGE 6",192,70,colour(0,0,0))
            lcd.text("LIGHT",55,2,colour(200,0,0))
            cc = colour(200,200,0)
            lcd.text("LIGHT INTENSITY",30,70,colour(255,255,255)) 
            lcd.text(lightintensity,80,85,cc)     
            lcd.text("NEXT=>",192, 10 ,colour(0,0,0))
            lcd.text("BACK=>",192, 115, colour (0,0,0))    
            lcd.text("T P G INC",10,120,colour(0,255,0))
            lcd.show()
            Loaded = True
        if key0.value() == 0 :
            buzzersound()
            current_page += 1
            clear(0)
            lcd.show()
            Loaded = False
        elif key1.value() == 0:
            buzzersound()
            current_page -= 1
            clear(0)
            lcd.show()  
            Loaded = False   

    elif current_page == 7 :
        if not Loaded:
            lcd.hline(0,95,240 , colour(0,0,0 ) )
            lcd.fill_rect(0 , 0 ,240,130 , colour(0,0,128 ) )
            lcd.fill_rect(30,0, 110 , 20 , colour ( 255 , 255 , 255 ) )
            lcd.fill_rect(190,0 , 70 , 140 , colour(255,255,255 ) )
            lcd.text("PAGE 7",192,70,colour(0,0,0))
            lcd.text("AGRIVISION",55,2,colour(200,0,0))
            cc = colour(200,200,0)
            lcd.text("THANK YOU FOR ",10,70,colour(255,255,255)) 
            lcd.text("CHECKING US OUT",10,80, colour(255,255,255))     
            lcd.text("BACK=>",192, 115, colour (0,0,0))
            lcd.text("T P G INC",10,120,colour(0,255,0))  
            lcd.show()
            Loaded = True
        if key1.value() == 0 :
            buzzersound()
            current_page -= 1
            clear(0)
            lcd.show()
            Loaded = False
#===================================END OF LCD SCREEN CODE============================================================================================================