"""Simple led controller."""

from functools import partial

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

    def transition(self, duration, is_on=None, **kwargs):
        """
        Transition to the specified state of the led.

        If another transition is already running, it is aborted.

        :param duration: The duration of the transition.
        :param is_on: The on-off state to transition to.
        :param kwargs: The state to transition to.
        """
        self._cancel_active_transition()

        dest_state = self._prepare_transition(is_on, **kwargs)
        total_steps = self._transition_steps(**dest_state)
        state_stages = [self._transition_stage(step, total_steps, **dest_state)
                        for step in range(total_steps)]
        pwm_stages = [self._get_pwm_values(**stage)
                      for stage in state_stages]
        callback = partial(self._transition_callback, is_on)
        self._active_transition = Transition(self._driver, duration,
                                             state_stages, pwm_stages,
                                             callback)

        TransitionManager().execute(self._active_transition)

        return self._active_transition

    def _cancel_active_transition(self):
        if self._active_transition:
            self._active_transition.cancel()
            self._active_transition = None

    def _transition_callback(self, is_on, transition):
        """
        Callback that is called when a transition has ended.

        :param is_on: The on-off state to transition to.
        :param transition: The transition that has ended.
        """
        # Update state properties
        if transition.state_stages:
            state = transition.state_stages[transition.stage_index]
            if self.is_on and is_on is False:
                # If led was turned off, set brightness to initial value
                # so that the brightness is restored when it is turned on again
                state['brightness'] = self.brightness
            self.set(is_on=is_on, cancel_transition=False, **state)

        self._active_transition = None

    def _prepare_transition(self, is_on=None, **kwargs):
        """
        Perform pre-transition tasks and construct the destination state.

        :param is_on: The on-off state to transition to.
        :param kwargs: The state to transition to.
        :return: The destination state of the transition.
        """
        # Handle transitions with changing on-off-state
        dest_state = kwargs.copy()
        if is_on is not None:
            if is_on and not self.is_on:
                if 'brightness' not in kwargs or kwargs['brightness'] is None:
                    dest_state['brightness'] = self.brightness
                self.set(brightness=0, cancel_transition=False)
            elif not is_on and self.is_on:
                dest_state['brightness'] = 0

        return dest_state

    def _transition_steps(self, brightness=None):
        """
        Get the maximum number of steps needed for a transition.

        :param brightness: The brightness to transition to (0.0-1.0).
        :return: The maximum number of steps.
        """
        if brightness is not None:
            self._assert_is_brightness(brightness)
            return self._driver.steps(self.brightness, brightness)

        return 0

    def _transition_stage(self, step, total_steps, brightness=None):
        """
        Get a transition stage at a specific step.

        :param step: The current step.
        :param total_steps: The total number of steps.
        :param brightness: The brightness to transition to (0.0-1.0).
        :return: The stage at the specific step.
        """
        if brightness is not None:
            self._assert_is_brightness(brightness)
            brightness = self._interpolate(self.brightness, brightness,
                                           step, total_steps)

        return {'brightness': brightness}

    @staticmethod
    def _interpolate(start, end, step, total_steps):
        """
        Interpolate a value from start to end at a given progress.

        :param start: The start value.
        :param end: The end value.
        :param step: The current step.
        :param total_steps: The total number of steps.
        :return: The interpolated value at the given progress.
        """
        diff = end - start
        progress = step / (total_steps - 1)
        return start + progress * diff

    @staticmethod
    def _assert_is_brightness(value):
        """
        Assert that the given value is a valid brightness.

        :param value: The value to check.
        """
        if not 0 <= value <= 1:
            raise ValueError('Brightness must be between 0 and 1.')
