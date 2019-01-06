"""RGB led controller."""
from __future__ import division

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

    def _prepare_transition(self, is_on=None, brightness=None, color=None):
        """
        Perform pre-transition tasks and construct the destination state.

        :param is_on: The on-off state to transition to.
        :param brightness: The brightness to transition to (0.0-1.0).
        :param color: The color to transition to.
        :return: The destination state of the transition.
        """
        dest_state = super()._prepare_transition(is_on,
                                                 brightness=brightness,
                                                 color=color)

        # Handle transitions from off to on and changing color
        if is_on and not self.is_on and color is not None:
            self.set(color=color, cancel_transition=False)

        return dest_state

    def _transition_steps(self, brightness=None, color=None):
        """
        Get the maximum number of steps needed for a transition.

        :param brightness: The brightness to transition to (0.0-1.0).
        :param color: The color to transition to.
        :return: The maximum number of steps.
        """
        values = []
        if brightness is not None:
            self._assert_is_brightness(brightness)
            values.append((self.brightness, brightness))

        if color is not None:
            self._assert_is_color(color)
            values += [(self.color[i] / 255, color[i] / 255) for i in range(3)]

        if not values:
            return 0

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
            self._assert_is_brightness(brightness)
            brightness = self._interpolate(self.brightness, brightness,
                                           step, total_steps)

        if color is not None:
            self._assert_is_color(color)
            color = Color(*[self._interpolate(self.color[i], color[i],
                                              step, total_steps)
                            for i in range(3)])

        return {'brightness': brightness, 'color': color}

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
