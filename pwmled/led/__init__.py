"""Simple led controller."""

from pwmled import CancellationToken


class SimpleLed(object):
    """Represents a simple, one-color led that can be controlled."""

    def __init__(self, driver):
        """
        Initialize the led.

        :param driver: The driver that is used to control the led.
        """
        self._driver = driver
        self._is_on = False
        self._brightness = 1
        self._active_transitions = []

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

    def set(self, is_on=None, brightness=None, cancel_transitions=True):
        """
        Set properties of the led simultaneously before updating pwm values.

        :param is_on: On-off state of the led.
        :param brightness: Brightness of the led.
        :param cancel_transitions: Determines, whether transitions should be cancelled.
        """
        if cancel_transitions:
            self._cancel_active_transitions()

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
        # Cancel active transitions and register cancellation token of current
        self._cancel_active_transitions()
        cancellation_token = CancellationToken()
        self._active_transitions.append(cancellation_token)

        # Perform the actual transition
        dest_state = self._perform_transition(duration, is_on, kwargs,
                                              cancellation_token)

        # Update state properties
        if self.is_on and is_on is False:
            # If led was turned off, set brightness to initial value afterwards
            # so that the brightness is restored when it is turned on again
            dest_state['brightness'] = self.brightness
        self.set(is_on=is_on, cancel_transitions=False, **dest_state)

        # Remove cancellation token from active transitions and confirm
        # cancellation, if requested
        self._active_transitions.remove(cancellation_token)
        if cancellation_token.is_cancellation_requested:
            cancellation_token.confirm_cancellation()

    def _cancel_active_transitions(self):
        """Cancel active transitions and wait for their exit."""
        for transition in self._active_transitions:
            transition.request_cancellation(timeout=1)

    def _perform_transition(self, duration, is_on, dest_state,
                            cancellation_token):
        """
        Perform the actual transition to the specified state of the led.

        :param duration: The duration of the transition.
        :param is_on: The on-off state to transition to.
        :param dest_state: The state to transition to.
        :param cancellation_token: Token used for cancelling the transition.
        :return: The state of the led at the moment of return.
        """
        if self.is_on or is_on:
            dest_state = self._prepare_transition(is_on, **dest_state)
            total_steps = self._transition_steps(**dest_state)
            state_stages = [self._transition_stage(step, total_steps, **dest_state)
                            for step in range(total_steps)]
            pwm_stages = [self._get_pwm_values(**stage)
                          for stage in state_stages]
            stage_index = self._driver.transition(duration, pwm_stages,
                                                  cancellation_token)

            # If transition was cancelled early, use last applied stage as
            # destination state
            if cancellation_token.is_cancellation_requested:
                dest_state = state_stages[stage_index]

        return dest_state

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
                self.brightness = 0
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
