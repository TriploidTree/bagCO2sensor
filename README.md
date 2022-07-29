# Handbag CO2 sensor
A CO2 sensor built into a handbag, based on the Pimorni Badger2040 and SCD41 sensor.

I decided to build this initially as a thermometer in a bag, as I was tired of going places that were too warm and wanted proof to show people "It's too warm". I then decided to go for a CO2 sensor too, as it's a quick and dirty way to measure ventilation quality, so now I can say "It's too warm AND too stuffy, we need to open windows or get out".

## Materials

A messenger style bag with a lined flap is easiest for putting the sensor and screen in, but you can pin it to the outside of any bag.

A Pimoroni Badger 2040 (https://shop.pimoroni.com/products/badger-2040?variant=39752959852627)

A CO2 sensor (I used the Pimoroni SCD41 breakout https://shop.pimoroni.com/products/scd41-co2-sensor-breakout?variant=39652270833747)

A way to connect them (Pimorni also supply a handy cable https://shop.pimoroni.com/products/jst-sh-cable-qwiic-stemma-qt-compatible?variant=31910609813587, but you could wire them up however you're comfortable)

A power supply (I went with a powerbank, as I'd be carrying the handbag anyway, and it should be useful for charging phones/headphones on the go)

## Code

Cobbled together with a lot of help from Pimoroni's library of tutorials and examples: https://github.com/pimoroni/pimoroni-pico and https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/examples/breakout_scd41

Use Thonny to put main.py on your Badger2040.

## Final assembly



## Behaviour

The general behaviour is an update of values on the screen every 2 minutes.
If you press button A, you get an immediate update.
Sometimes the sensor doesn't respond, (it seems to not be ready), and will update after the next 2 minute sleep or so. Plugging it in and out also seems to work.

The sensor can take a minute or two to adjust to changes, particularly when going from indoors to outdoors. Breathing on it can impact the reading for the subsequent seconds too.

The sensor can self calibrate if it's left in outdoor air (well ventilated rooms are also good). 

