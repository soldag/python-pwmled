from functools import wraps


def update_pwm(function):
    """
    Update pwm values after a execution of a function.

    :param function: The function to execute.
    :return: Decorator.
    """
    def _decorator(self, *args, **kwargs):
        """
        Decorator function.

        :param args: Passthrough positional arguments.
        :param kwargs: Passthrough keyword arguments.
        """
        function(self, *args, **kwargs)
        self._update_pwm()
    return wraps(function)(_decorator)


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

    @update_pwm
    def on(self):
        """Turn the led on."""
        self._is_on = True

    @update_pwm
    def off(self):
        """Turn the led off."""
        self._is_on = False

    @property
    def brightness(self):
        """
        Brightness property.

        :return: The brightness of the led (0.0-1.0).
        """
        return self._brightness

    @brightness.setter
    @update_pwm
    def brightness(self, brightness):
        """
        Set the brightness of the led.

        :param brightness: The brightness to set (0.0-1.0).
        :return:
        """
        if not 0 <= brightness <= 1:
            raise ValueError('Value must be between 0 and 1.')

        self._brightness = brightness

    def transition(self, duration, **kwargs):
        """
        Transition to the specified state of the led.

        :param duration: The duration of the transition.
        :param kwargs: The state to transition to.
        """
        values = self._get_pwm_values(**kwargs)
        self._driver.transition(duration, values)

    def _update_pwm(self):
        """Update the pwm values of the driver regarding the current state."""
        self._driver.set_pwm(self._get_pwm_values())

    def _get_pwm_values(self, brightness=None):
        """
        Get the pwm values for a specific state of the led.
        If no state is provided, current state is used.

        :param brightness: The brightness of the state.
        :return: The pwm values.
        """
        brightness = brightness or self.brightness

        return [brightness]
