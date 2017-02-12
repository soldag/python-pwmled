"""PCA9685 pwm driver."""
from Adafruit_PCA9685 import PCA9685

from pwmled.driver import Driver


class Pca9685Driver(Driver):
    """Represents a pwm driver, which uses the pins of an PCA9685 I2C board."""

    RESOLUTION = 12

    def __init__(self, pins, freq=200, address=0x40):
        """
        Initialize the driver.

        :param pins: The pin numbers, that should be controlled.
        :param freq: The pwm frequency.
        :param address: The address of the PCA9685.
        """
        super(Pca9685Driver, self).__init__(pins, self.RESOLUTION, freq)

        self._device = PCA9685(address)
        self._device.set_pwm_freq(self._freq)

    def _set_pwm(self, raw_values):
        """
        Set pwm values on the controlled pins.

        :param raw_values: Raw values to set (0-4095).
        """
        for i in range(len(self._pins)):
            self._device.set_pwm(self._pins[i], 0, raw_values[i])
