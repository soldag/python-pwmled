"""RGB led controller."""
from pwmled import Color
from pwmled.led import SimpleLed


class RgbLed(SimpleLed):
    """Represents a RGB led that can be controlled."""

    def __init__(self, driver):
        """
        Initialize the led.

        :param driver: The driver that is used to control the led.
        """
        super().__init__(driver)
        self._color = Color(255, 255, 255)

    @property
    def color(self):
        """
        The color property.

        :return: The color of the led.
        """
        return self._color

    @color.setter
    def color(self, color):
        """
        Set the color of the led.

        :param color: The color to set.
        """
        self.set(color=color)

    @property
    def state(self):
        """
        State property.

        :return: The current state of the led.
        """
        return dict(
            **super().state,
            color=self.color,
        )

    def set(self, is_on=None, brightness=None, color=None,
            cancel_transition=True):
        """
        Set properties of the led simultaneously before updating pwm values.

        :param is_on: On-off state of the led.
        :param brightness: Brightness of the led.
        :param color: Color of the led.
        :param cancel_transition: Cancel active transitions.
        """
        if cancel_transition:
            self._cancel_active_transition()

        if color is not None:
            self._assert_is_color(color)
            self._color = color

        super().set(is_on, brightness, cancel_transition=False)

    def _get_pwm_values(self, brightness=None, color=None):
        """
        Get the pwm values for a specific state of the led.

        If a state argument is omitted, current value is used.

        :param brightness: The brightness of the state.
        :param color: The color of the state.
        :return: The pwm values.
        """
        if brightness is None:
            brightness = self.brightness
        if color is None:
            color = self.color

        return [(x / 255) * brightness for x in color]

    @classmethod
    def _assert_is_valid_state(cls, value):
        """
        Assert that the given value is a valid state object.

        :param value: The value to check.
        """
        super()._assert_is_valid_state(value)

        color = value.get('color')
        if color is not None:
            cls._assert_is_color(color)

    @staticmethod
    def _assert_is_color(value):
        """
        Assert that the given value is a valid brightness.

        :param value: The value to check.
        """
        if not isinstance(value, tuple) or len(value) != 3:
            raise ValueError("Color must be a RGB tuple.")

        if not all(0 <= x <= 255 for x in value):
            raise ValueError("RGB values of color must be between 0 and 255.")
