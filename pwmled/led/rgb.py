from __future__ import division

from pwmled import Color
from pwmled.led import SingleLed


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
    def color(self, color):
        """
        Set the color of the led.

        :param color: The color to set.
        """
        if not all(0 <= x <= 255 for x in color):
            raise ValueError('Invalid color!')

        self.set(color=color)

    def set(self, is_on=None, brightness=None, color=None):
        """
        Set properties of the led simultaneously before updating pwm values.

        :param is_on: On-off state of the led.
        :param brightness: Brightness of the led.
        :param color: Color of the led.
        """
        if color is not None:
            self._color = color

        super(RgbLed, self).set(is_on, brightness)

        return self._get_pwm_values(brightness=brightness, color=color)

    def _get_pwm_values(self, brightness=None, color=None):
        """
        Get the pwm values for a specific state of the led.
        If no state is provided, current state is used.

        :param brightness: The brightness of the state.
        :param color: The color of the state.
        :return: The pwm values.
        """
        if brightness is None:
            brightness = self.brightness
        if color is None:
            color = self.color

        return [(x / 255) * brightness for x in color]

    def _transition_steps(self, brightness=None, color=None):
        """
        Get the maximum number of steps needed for a transition.

        :param brightness: The brightness to transition to (0.0-1.0).
        :param color: The color to transition to.
        :return: The maximum number of steps.
        """
        values = []
        if color is not None:
            values += [(self.color[i] / 255, color[i] / 255) for i in range(3)]
        if brightness is not None:
            values.append((self.brightness, brightness))

        return max(self._driver.steps(*args) for args in values)

    def _transition_stage(self, step, total_steps,
                          brightness=None, color=None):
        """
        Get a transition stage at a specific step.

        :param step: The current step.
        :param total_steps: The total number of steps.
        :param brightness: The brightness to transition to (0.0-1.0).
        :param color: The color to transition to.
        :return: The stage at the specific step.
        """
        if brightness is not None:
            brightness = self._interpolate(self.brightness, brightness,
                                           step, total_steps)

        if color is not None:
            color = Color(*[self._interpolate(self.color[i], color[i],
                                              step, total_steps)
                            for i in range(3)])

        return self._get_pwm_values(brightness=brightness, color=color)
