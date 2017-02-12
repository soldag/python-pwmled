"""GPIO pwm driver."""
import pigpio

from pwmled.driver import Driver


class GpioDriver(Driver):
    """Represents a pwm driver, which uses GPIOs of a Raspberry Pi."""

    RESOLUTION = 8

    def __init__(self, pins, freq=200):
        """
        Initialize the driver.

        :param pins: The pin numbers, that should be controlled.
        :param freq: The pwm frequency.
        """
        super(GpioDriver, self).__init__(pins, self.RESOLUTION, freq)

        self._pi = pigpio.pi()

    def _set_pwm(self, raw_values):
        """
        Set pwm values on the controlled pins.

        :param raw_values: Raw values to set (0-255).
        """
        for i in range(len(self._pins)):
            self._pi.set_PWM_dutycycle(self._pins[i], raw_values[i])

    def _stop(self):
        """Stop the driver and release resources."""
        self._pi.stop()
