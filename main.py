import time

import badger2040
import pimoroni_i2c
import breakout_scd41

PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}

badger = badger2040.Badger2040()

i2c = pimoroni_i2c.PimoroniI2C(**PINS_BREAKOUT_GARDEN)

breakout_scd41.init(i2c)
breakout_scd41.start()


button_a = machine.Pin(badger2040.BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_b = machine.Pin(badger2040.BUTTON_B, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_c = machine.Pin(badger2040.BUTTON_C, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_up = machine.Pin(badger2040.BUTTON_UP, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_down = machine.Pin(badger2040.BUTTON_DOWN, machine.Pin.IN, machine.Pin.PULL_DOWN)

def CO2monitor():
    if breakout_scd41.ready():
        co2, temperature, humidity = breakout_scd41.measure()
        print(co2, temperature, humidity)
        
        badger.pen(15)
        badger.clear()
        
        badger.pen(0)
        badger.thickness(3)
        badger.text("Air monitor:", 60, 25)
        badger.thickness(2)
        badger.text(str(int(co2)) +" ppm CO2" , 20, 70)
        badger.text (str(int(temperature)) +" ºC    " + str(int(humidity)) + " %RH" , 20, 100)
        badger.update()
    else:
        print("wtf")

def anything(flibble):
    print("button pressed")
    CO2monitor()

button_a.irq(trigger=machine.Pin.IRQ_RISING, handler=anything)
#button_b.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
#button_c.irq(trigger=machine.Pin.IRQ_RISING, handler=button)

#button_up.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
#button_down.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
#button_user.irq(trigger=machine.Pin.IRQ_RISING, handler=button)



while True:
    CO2monitor()
    time.sleep(120) 