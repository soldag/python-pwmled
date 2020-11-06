"""GPIO pwm driver."""
import pigpio

from pwmled.driver import Driver


class GpioDriver(Driver):
    """Represents a pwm driver, which uses GPIOs of a Raspberry Pi."""

    RESOLUTION = 8

    def __init__(self, pins, freq=200, host='localhost', port=8888):
        """
        Initialize the driver.

        :param pins: The pin numbers, that should be controlled.
        :param freq: The pwm frequency.
        :param host: The host name of the Pi on which pigpio is running.
        :param port: The port on which pigpio is running.
        """
        super().__init__(pins, self.RESOLUTION, freq)

        self._pi = pigpio.pi(host, port, show_errors=False)
        if not self._pi.connected:
            raise ConnectionError('Could not connect to the pigpio daemon')

        for pin in self._pins:
            self._pi.set_PWM_frequency(pin, freq)

    def _set_pwm(self, raw_values):
        """
        Set pwm values on the controlled pins.

        :param raw_values: Raw values to set (0-255).
        """
        for pin, value in zip(self._pins, raw_values):
            try:
                current_value = self._pi.get_PWM_dutycycle(pin)
            except pigpio.error as error:
                if error.value == 'GPIO is not in use for PWM':
                    current_value = 0
                else:
                    raise

            if current_value != value:
                self._pi.set_PWM_dutycycle(pin, value)

    def _stop(self):
        """Stop the driver and release resources."""
        self._pi.stop()
