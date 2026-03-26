import machine

power = machine.Pin("LED",machine.Pin.OUT)

power.value(1)