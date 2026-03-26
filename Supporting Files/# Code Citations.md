# Code Citations

## License: unknown
https://github.com/tacker66/pihome/tree/10d77a5f0036f5095c8181e6ca8faf087c105622/MicroPython/Pico_LCD_114_V2.py

```
):
        self.rst(1)
        self.rst(0)
        self.rst(1)
        self.write_cmd(0x36)
        self.write_data(0x70)
        self.write_cmd(0x3A)
        self.write_data(0x05)
        self.write_cmd(0xB2)
        self.write_data(0x0C
```


## License: unknown
https://github.com/TCmatj/RaspberryPi_PicoGameConsole/tree/a5c5bac7c27d548c591fcfce23820dbc736a0b6b/Lcd.py

```
.rst(1)
        self.rst(0)
        self.rst(1)
        self.write_cmd(0x36)
        self.write_data(0x70)
        self.write_cmd(0x3A)
        self.write_data(0x05)
        self.write_cmd(0xB2)
        self.write_data(0x0C)
        self.
```


## License: MIT
https://github.com/tacker66/mp_playground/tree/f1e8dc52e1285faa6014f63f849f1712ad0affa3/Pico_LCD_114_V2.py

```
(0x0C)
        self.write_data(0x00)
        self.write_data(0x33)
        self.write_data(0x33)
        self.write_cmd(0xB7)
        self.write_data(0x35)
        self.write_cmd(0xBB)
        self.write_data(0x19)
        self.write_cmd(0xC0)
        self.write_data(
```


## License: GPL_2_0
https://github.com/teleshoes/pico-lcd/tree/704c8611805c53a7f6790b54f9924acc6f3eb194/src/lcd.py

```
self, cmd):
        self.cs(1)
        self.dc(0)
        self.cs(0)
        self.spi.write(bytearray([cmd]))
        self.cs(1)

    def write_data(self, data):
        self.cs(1
```

