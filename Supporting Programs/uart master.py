import machine 
import utime

uart = machine.UART(0,9600, tx = machine.Pin(0), rx = machine.Pin(1))
uart_tx = machine.Pin(0)
uart_rx = machine.Pin(1)

def receive_data():
    while uart.any():
        data = uart.read(1)
        print(data)
        
        

def send_data(data):
    uart.write(data)

while True :
    receive_data()
    send_data("WE ARE GOING TO WIN ZSF")
    utime.sleep(1)	