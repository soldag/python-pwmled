"""Generic pwm driver."""
from __future__ import division
import math


class Driver:
    """Represents the base class for pwm drivers."""

    IO_TRIES = 10

    def __init__(self, pins, resolution, freq):
        """
        Initialize the driver.

        :param pins: The pin numbers that should be controlled.
        :param resolution: The resolution of the pwm channel.
        :param freq: The pwm frequency.
        """
        if not isinstance(pins, list):
            pins = [pins]

        self._pins = pins
        self._resolution = resolution
        self._freq = freq
        self._state = [0] * len(self._pins)
        self._max_raw_value = math.pow(2, self._resolution) - 1

    @property
    def pins(self):
        """
        Color property.

        :return: The pins numbers that are controlled.
        """
        return self._pins

    def set_pwm(self, values):
        """
        Set pwm values on the controlled pins.

        :param values: Values to set (0.0-1.0).
        :return:
        """
        if len(values) != len(self._pins):
            raise ValueError('Number of values has to be identical with '
                             'the number of pins.')
        if not all(0 <= v <= 1 for v in values):
            raise ValueError('Values must be between 0 and 1.')

        for tries in range(self.IO_TRIES):
            try:
                self._set_pwm(self._to_raw_pwm(values))
                break
            except IOError as error:
                if tries == self.IO_TRIES - 1:
                    raise error
        self._state = values

    def _set_pwm(self, values):
        """
        Method stub for setting the pwm values.

        Has to be implemented by inheriting classes.
        :param values: Values to set (0.0-1.0).
        """
        raise NotImplementedError

    def _to_raw_pwm(self, values):
        """
        Convert uniform pwm values to raw, driver-specific values.

        :param values: The uniform pwm values (0.0-1.0).
        :return: Converted, driver-specific pwm values.
        """
        return [self._to_single_raw_pwm(values[i])
                for i in range(len(self._pins))]

    def _to_single_raw_pwm(self, value):
        """
        Convert a single uiform pwm value to raw, driver-specific value.

        :param value: The uniform pwm value (0.0-1.0).
        :return: Converted, driver-specific pwm value.
        """
        return int(round(value * self._max_raw_value))

    def _to_uniform_pwm(self, values):
        """
        Convert raw pwm values to uniform values.

        :param values: The raw pwm values.
        :return: Converted, uniform pwm values (0.0-1.0).
        """
        return [self._to_single_uniform_pwm(values[i])
                for i in range(len(self._pins))]

    def _to_single_uniform_pwm(self, value):
        """
        Convert a single raw pwm value to uniform value.

        :param value: The raw pwm value.
        :return: Converted, uniform pwm value (0.0-1.0).
        """
        return value / self._max_raw_value

    def steps(self, start, end):
        """
        Get the maximum number of steps the driver needs for a transition.

        :param start: The start value as uniform pwm value (0.0-1.0).
        :param end: The end value as uniform pwm value (0.0-1.0).
        :return: The maximum number of steps.
        """
        if not 0 <= start <= 1:
            raise ValueError('Values must be between 0 and 1.')
        if not 0 <= end <= 1:
            raise ValueError('Values must be between 0 and 1.')

        raw_start = self._to_single_raw_pwm(start)
        raw_end = self._to_single_raw_pwm(end)
        return abs(raw_start - raw_end)

    def stop(self):
        """Stop the driver and release resources."""
        self._stop()

    def _stop(self):
        """
        Method stub for stopping the driver.

        Has to be implemented by inheriting classes.
        """
        pass
