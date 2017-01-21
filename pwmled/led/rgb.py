from __future__ import division

from pwmled import Color
from pwmled.led import update_pwm, SingleLed


class RgbLed(SingleLed):
    """Represents a RGB led that can be controlled."""

    def __init__(self, driver):
        """
        Initialize the led.

        :param driver: The driver that is used to control the led.
        """
        super(RgbLed, self).__init__(driver)
        self._color = Color(255, 255, 255)

    @property
    def color(self):
        """
        The color property.

        :return: The color of the led.
        """
        return self._color

    @color.setter
    @update_pwm
    def color(self, color):
        """
        Set the color of the led.

        :param color: The color to set.
        """
        if not all(0 <= x <= 255 for x in color):
            raise ValueError('Invalid color!')

        self._color = color

    def _get_pwm_values(self, color=None, brightness=None):
        """
        Get the pwm values for a specific state of the led.
        If no state is provided, current state is used.

        :param color: The color of the state.
        :param brightness: The brightness of the state.
        :return: The pwm values.
        """
        color = color or self.color
        brightness = brightness or self.brightness

        return [(x / 255) * brightness for x in color]
