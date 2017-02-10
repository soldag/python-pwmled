class SingleLed(object):
    """Represents a single led that can be controlled."""

    def __init__(self, driver):
        """
        Initialize the led.

        :param driver: The driver that is used to control the led.
        """
        self._driver = driver
        self._is_on = False
        self._brightness = 1

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
        if not 0 <= brightness <= 1:
            raise ValueError('Value must be between 0 and 1.')

        self.set(brightness=brightness)

    def set(self, is_on=None, brightness=None):
        """
        Set properties of the led simultaneously before updating pwm values.

        :param is_on: On-off state of the led.
        :param brightness: Brightness of the led.
        """
        if is_on is not None:
            self._is_on = is_on
        if brightness is not None:
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
        If no state is provided, current state is used.

        :param brightness: The brightness of the state.
        :return: The pwm values.
        """
        if brightness is None:
            brightness = self.brightness

        return [brightness]

    def transition(self, duration, **kwargs):
        """
        Transition to the specified state of the led.

        :param duration: The duration of the transition.
        :param kwargs: The state to transition to.
        """
        total_steps = self._transition_steps(**kwargs)
        stages = [self._transition_stage(step, total_steps, **kwargs)
                  for step in range(total_steps)]
        self._driver.transition(duration, stages)

        # Update state properties
        self.set(**kwargs)

    def _transition_steps(self, brightness=None):
        """
        Get the maximum number of steps needed for a transition.

        :param brightness: The brightness to transition to (0.0-1.0).
        :return: The maximum number of steps.
        """
        return self._driver.steps(self.brightness, brightness)

    def _transition_stage(self, step, total_steps, brightness):
        """
        Get a transition stage at a specific step.

        :param step: The current step.
        :param total_steps: The total number of steps.
        :param brightness: The brightness to transition to (0.0-1.0).
        :return: The stage at the specific step.
        """
        brightness = self._interpolate(self.brightness, brightness,
                                       step, total_steps)
        return self._get_pwm_values(brightness)

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
