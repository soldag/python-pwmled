from Adafruit_PCA9685 import PCA9685

from pwmled.driver import Driver


class Pca9685Driver(Driver):
    """Represents a pwm driver, which uses the pins of an PCA9685 I2C board."""

    MAX_VALUE = 4095

    def _initialize(self, address=0x40):
        """
        Initialize the driver.

        :param address: The address of the PCA9685.
        """
        self._device = PCA9685(address)
        self._device.set_pwm_freq(self.freq)

    def _set_pwm(self, values):
        """
        Set pwm values on the controlled pins.

        :param values: Values to set (0.0-1.0).
        """
        for i in range(len(self.pins)):
            self._device.set_pwm(self.pins[i], 0, int(round(values[i] * self.MAX_VALUE)))
