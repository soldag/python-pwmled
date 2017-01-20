from pwmled import Color
from pwmled.led import Led, update_pwm


class RgbLed(Led):
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

    def _get_pwm_values(self):
        """
        Get the pwm values regarding the current color.

        :return: The pwm values.
        """
        return [x / 255 for x in self.color]
