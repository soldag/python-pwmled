"""PCA9685 pwm driver."""
import busio
import adafruit_pca9685
from adafruit_blinka.agnostic import board_id
try:
    import board
except NotImplementedError:
    # Defer raising error to initialization of Pca9685Driver class
    board = None

from pwmled.driver import Driver


class Pca9685Driver(Driver):
    """Represents a pwm driver, which uses the pins of an PCA9685 I2C board."""

    RESOLUTION = 16

    def __init__(self, pins, freq=200, address=0x40):
        """
        Initialize the driver.

        :param pins: The pin numbers, that should be controlled.
        :param freq: The pwm frequency.
        :param address: The address of the PCA9685.
        """
        super().__init__(pins, self.RESOLUTION, freq)

        # Raise error if board couldn't be imported
        if not board:
            if not board_id:
                raise NotImplementedError('Board is unknown')
            raise NotImplementedError(f'Board "{board_id}" is not supported')

        i2c = busio.I2C(board.SCL, board.SDA)
        self._device = adafruit_pca9685.PCA9685(i2c, address=address)
        self._device.frequency = self._freq

    def _set_pwm(self, raw_values):
        """
        Set pwm values on the controlled pins.

        :param raw_values: Raw values to set (0-65535).
        """
        for pin, value in zip(self._pins, raw_values):
            channel = self._device.channels[pin]
            if channel.duty_cycle != value:
                channel.duty_cycle = value

    def _stop(self):
        """Stop the driver and release resources."""
        self._device.deinit()
