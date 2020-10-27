"""GPIO pwm driver."""
import pigpio

from pwmled.driver import Driver


class GpioDriver(Driver):
    """Represents a pwm driver, which uses GPIOs of a Raspberry Pi."""

    RESOLUTION = 8

    def __init__(self, pins, freq=200, host=None):
        """
        Initialize the driver.

        :param pins: The pin numbers, that should be controlled.
        :param freq: The pwm frequency.
        :param host: The host name of the Pi on which the pigpio is running.
        """
        super().__init__(pins, self.RESOLUTION, freq)

        if host is not None:
            self._pi = pigpio.pi(host)
        else:
            self._pi = pigpio.pi()
        # set frequency
        for i in range(len(self._pins)):
            self._pi.set_PWM_frequency(self._pins[i], self._freq)

    def _set_pwm(self, raw_values):
        """
        Set pwm values on the controlled pins.

        :param raw_values: Raw values to set (0-255).
        """
        for pin, value in zip(self._pins, raw_values):
            if self._pi.get_PWM_dutycycle(pin) != value:
                self._pi.set_PWM_dutycycle(pin, value)

    def _stop(self):
        """Stop the driver and release resources."""
        self._pi.stop()
