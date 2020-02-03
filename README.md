# python-pwmled [![PyPI version](https://badge.fury.io/py/pwmled.svg)](https://badge.fury.io/py/pwmled)

`python-pwmled` controls LEDs connected to a micro controller using pulse-width modulation. It supports one-color, RGB and RGBW leds driven by GPIOs of an Raspberry Pi or a PCA9685 controller. 

# Installation
`python-pwmled` requires Python 3. It can be installed using pip:
```bash
pip install pwmled
```

When directly controlling the GPIOs of a Raspberry Pi using the `GpioDriver`(see [below](#configuration)), the [pigpio C library](https://github.com/joan2937/pigpio) is required. It can be installed with the following commands:
```bash
wget abyz.co.uk/rpi/pigpio/pigpio.zip
unzip pigpio.zip
cd PIGPIO
make
sudo make install
```
Besides the library, the `pigpiod` utility is installed, which starts `pigpio` as daemon. The daemon must be running when using the `GpioDriver`.
```bash
sudo pigpiod
```

# Usage
### Configuration
`python-pwmled` supports several possibilities for connecting LEDs to your micro controller:
- GPIO: LEDs can be connected directly to the GPIOs of a Raspberry Pi.
- PCA9885: A [PCA9685](https://cdn-shop.adafruit.com/datasheets/PCA9685.pdf) can be used as I2C-bus PWM controller.

```python
from pwmled.driver.gpio import GpioDriver
from pwmled.driver.pca9685 import Pca9685Driver

# GPIO driver, which controls pins 17, 22, 23
driver = GpioDriver([17, 22, 23])
driver = GpioDriver([17, 22, 23], freq=200)
# To control the pigpio on a other machine use the host parameter
driver = GpioDriver([17, 22, 23], host='other.host')

# PCA9685 driver which controls pins 1, 2, 3
driver = Pca9685Driver([1, 2, 3])
driver = Pca9685Driver([1, 2, 3], freq=200, address=0x40)
```

### Control
Each LED needs a separated driver, which controls the corresponding pins. The number and order of pins depends on the led type:
- One-color: 1 pin
- RGB: 3 pins (`[R, G, B]`)
- RGBW: 4 pins (`[R, G, B, W]`)

The supported operations are shown in the following example:

```python
from pwmled import Color
from pwmled.led import SimpleLed
from pwmled.led.rgb import RgbLed
from pwmled.led.rgbw import RgbwLed
from pwmled.driver.gpio import GpioDriver

# One-color led
driver = GpioDriver([C])
led = SimpleLed(driver)
led.on()
led.brightness = 0.5
led.transition(5, brightness=0)
led.off()

# RGB led
driver = GpioDriver([R, G, B])
led = RgbLed(driver)
led.on()
led.color = Color(255, 0, 0)
led.set(color=Color(0, 255, 0), brightness=0.5) # set two properties simultaneously
led.transition(5, color=Color(0, 0, 255), brightness=1)
led.off()

# RGBW led
driver = GpioDriver([R, G, B, W])
led = RgbwLed(driver)
# RgbwLed has same interface as RgbLed
```

# Contributions
Pull-requests are welcome, especially for adding new drivers or led types.

# License
This library is provided under [MIT license](https://raw.githubusercontent.com/soldag/python-pwmled/master/LICENSE.md).
