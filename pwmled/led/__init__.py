"""Simple led controller."""

from pwmled.transitions.transition import Transition
from pwmled.transitions.transition_manager import TransitionManager


class SimpleLed:
    """Represents a simple, one-color led that can be controlled."""

    def __init__(self, driver):
        """
        Initialize the led.

        :param driver: The driver that is used to control the led.
        """
        self._driver = driver
        self._is_on = False
        self._brightness = 1
        self._active_transition = None

    @property
    def is_on(self):
        """
        On-off state property.

        :return: True, if led is on. False otherwise.
        """
        return self._is_on

    def on(self):
        """Turn the led on."""
        self.set(is_on=True)

    def off(self):
        """Turn the led off."""
        self.set(is_on=False)

    @property
    def brightness(self):
        """
        Brightness property.

        :return: The brightness of the led (0.0-1.0).
        """
        return self._brightness

    @brightness.setter
    def brightness(self, brightness):
        """
        Set the brightness of the led.

        :param brightness: The brightness to set (0.0-1.0).
        """
        self.set(brightness=brightness)

    @property
    def state(self):
        """
        State property.

        :return: The current state of the led.
        """
        return dict(
            is_on=self.is_on,
            brightness=self.brightness,
        )

    def set(self, is_on=None, brightness=None, cancel_transition=True):
        """
        Set properties of the led simultaneously before updating pwm values.

        :param is_on: On-off state of the led.
        :param brightness: Brightness of the led.
        :param cancel_transition: Cancel active transitions.
        """
        if cancel_transition:
            self._cancel_active_transition()

        if is_on is not None:
            self._is_on = is_on

        if brightness is not None:
            self._assert_is_brightness(brightness)
            self._brightness = brightness

        self._update_pwm()

    def _update_pwm(self):
        """Update the pwm values of the driver regarding the current state."""
        if self._is_on:
            values = self._get_pwm_values()
        else:
            values = [0] * len(self._driver.pins)

        self._driver.set_pwm(values)

    def _get_pwm_values(self, brightness=None):
        """
        Get the pwm values for a specific state of the led.

        If a state argument is omitted, current value is used.

        :param brightness: The brightness of the state.
        :return: The pwm values.
        """
        if brightness is None:
            brightness = self.brightness

        return [brightness]

    def transition(self, duration, **dest_state):
        """
        Transition to the specified state of the led.

        If another transition is already running, it is aborted.

        :param duration: The duration of the transition.
        :param dest_state: The state to transition to.
        """
        self._assert_is_valid_state(dest_state)

        self._cancel_active_transition()
        return TransitionManager().execute(Transition(
            self,
            duration,
            self.state,
            dest_state,
        ))

    def _cancel_active_transition(self):
        if self._active_transition:
            self._active_transition.cancel()
            self._active_transition = None

    @classmethod
    def _assert_is_valid_state(cls, value):
        """
        Assert that the given value is a valid state object.

        :param value: The value to check.
        """
        brightness = value.get('brightness')
        if brightness is not None:
            cls._assert_is_brightness(brightness)

    @staticmethod
    def _assert_is_brightness(value):
        """
        Assert that the given value is a valid brightness.

        :param value: The value to check.
        """
        if not 0 <= value <= 1:
            raise ValueError('Brightness must be between 0 and 1.')
