import time

import badger2040
import pimoroni_i2c
import breakout_scd41
from machine import Timer

DEBUG_ENABLE = 0
MAX_ERROR_RESET = 5
PINS_BREAKOUT_GARDEN = {"sda": 4, "scl": 5}
PINS_PICO_EXPLORER = {"sda": 20, "scl": 21}


badger = badger2040.Badger2040()

i2c = pimoroni_i2c.PimoroniI2C(**PINS_BREAKOUT_GARDEN)

breakout_scd41.init(i2c)
breakout_scd41.stop()
breakout_scd41.start()

updating = False
error_count = 0

button_a = machine.Pin(badger2040.BUTTON_A, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_b = machine.Pin(badger2040.BUTTON_B, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_c = machine.Pin(badger2040.BUTTON_C, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_up = machine.Pin(badger2040.BUTTON_UP, machine.Pin.IN, machine.Pin.PULL_DOWN)
button_down = machine.Pin(badger2040.BUTTON_DOWN, machine.Pin.IN, machine.Pin.PULL_DOWN)

def DEBUG(*msg):
    if DEBUG_ENABLE:
        print(msg)

def draw(co2, temperature, humidity):
    badger.pen(15)
    badger.clear()
    badger.pen(0)
    badger.thickness(3)
    badger.text("Air monitor:", 60, 25)
    badger.thickness(2)
    badger.text(str(int(co2)) +" ppm CO2" , 20, 70)
    badger.text (str(int(temperature)) +" ºC    " + str(int(humidity)) + " %RH" , 20, 100)
    badger.update()
    

def CO2monitor():
    DEBUG("wah!")
    global updating
    global error_count
    if not updating:
        updating = True
        DEBUG("UPDATING")
        co2, temperature, humidity = (0,0,0)
        if breakout_scd41.ready(): # <--- blocking
            DEBUG("READY")
            try:
                co2, temperature, humidity = breakout_scd41.measure()
            except Exception as e:
                DEBUG("Failed to get scd41 data")
                DEBUG(e)
                updating = False
                return
            DEBUG(co2, temperature, humidity)
        else:
            DEBUG("wtf")
            error_count = error_count + 1
            if error_count >= MAX_ERROR_RESET:
                breakout_scd41.stop()
                breakout_scd41.start()

        draw(co2, temperature, humidity)
        DEBUG("SLEEPING")
        time.sleep(10)
        
        updating = False
        DEBUG("DONE")

    else:
        return

def refresh_cb(flibble):
    DEBUG("button pressed")
    CO2monitor()

button_a.irq(trigger=machine.Pin.IRQ_RISING, handler=refresh_cb)
timer=Timer(-1)
timer.init(period=120000, mode=Timer.PERIODIC, callback=lambda t:CO2monitor())
#button_b.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
#button_c.irq(trigger=machine.Pin.IRQ_RISING, handler=button)

#button_up.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
#button_down.irq(trigger=machine.Pin.IRQ_RISING, handler=button)
#button_user.irq(trigger=machine.Pin.IRQ_RISING, handler=button)

time.sleep(5)
CO2monitor()