import machine 
import utime

#uart communication declaration
uart = machine.UART(0,9600, tx = machine.Pin(0), rx = machine.Pin(1))
uart_tx = machine.Pin(0)
uart_rx = machine.Pin(1)

moisture = ""
temperature = ""
humidity = ""
lightintensity = ""


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


receive_data()