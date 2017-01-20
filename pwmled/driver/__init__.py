class Driver:
    """Represents the base class for pwm drivers."""
    def __init__(self, pins, freq=200, **kwargs):
        """
        Initialize the driver.

        :param pins: The pin numbers, that should be controlled
        :param freq: The pwm frequency.
        :param kwargs: Additional, driver-specific arguments.
        """
        if not isinstance(pins, list):
            pins = [pins]

        self.pins = pins
        self.freq = freq

        self._initialize(**kwargs)

    def _initialize(self, **kwargs):
        """
        Method stub for initialization.

        Has to be implemented by inheriting classes.
        """
        pass

    def set_pwm(self, values):
        """
        Set pwm values on the controlled pins.

        :param values: Values to set (0-100).
        :return:
        """
        if len(values) != len(self.pins):
            raise ValueError('Number of values has to be identical with '
                             'the number of pins.')
        if not all(0 <= v <= 100 for v in values):
            raise ValueError('Values have to be between 0 and 100.')

        self._set_pwm(values)

    def _set_pwm(self, values):
        """
        Method stub for setting the pwm values.

        Has to be implemented by inheriting classes.
        :param values: Values to set (0-100).
        """
        pass

    def stop(self):
        """Stop the driver and release resources."""
        self._stop()

    def _stop(self):
        """
        Method stub for stopping the driver.

        Has to be implemented by inheriting classes.
        """
        pass
