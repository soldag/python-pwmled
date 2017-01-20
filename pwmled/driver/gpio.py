import RPi.GPIO as GPIO

from pwmled.driver import Driver


class GpioDriver(Driver):
    """Represents a pwm driver, which uses GPIOs of a Raspberry Pi."""

    MAX_VALUE = 100

    def _initialize(self):
        """Initialize the driver."""
        self._pwms = []
        GPIO.setup(self.pins, GPIO.OUT)
        for pin in self.pins:
            pwm = GPIO.PWM(pin, self.freq)
            pwm.start(0)
            self._pwms.append(pwm)

    def _set_pwm(self, values):
        """
        Set pwm values on the controlled pins.

        :param values: Values to set (0.0-1.0).
        """
        for i in range(len(self._pwms)):
            self._pwms[i].ChangeDutyCycle(values[i] * self.MAX_VALUE)

    def _stop(self):
        """Stop the driver and release resources."""
        for pin in self._pwms:
            pin.stop()
        GPIO.cleanup()
