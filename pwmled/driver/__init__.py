from __future__ import division
import time
import math

from datetime import datetime


class Driver(object):
    """Represents the base class for pwm drivers."""

    TRANSITION_MIN_WAIT = 0.01

    def __init__(self, pins, resolution, freq):
        """
        Initialize the driver.

        :param pins: The pin numbers, that should be controlled.
        :param resolution: The resolution of the pwm channel.
        :param freq: The pwm frequency.
        """
        if not isinstance(pins, list):
            pins = [pins]

        self.pins = pins
        self.resolution = resolution
        self.freq = freq
        self.state = [0] * len(self.pins)

        self._max_raw_value = math.pow(2, self.resolution) - 1

    def set_pwm(self, values):
        """
        Set pwm values on the controlled pins.

        :param values: Values to set (0.0-1.0).
        :return:
        """
        if len(values) != len(self.pins):
            raise ValueError('Number of values has to be identical with '
                             'the number of pins.')
        if not all(0 <= v <= 1 for v in values):
            raise ValueError('Values have to be between 0 and 1.')

        self._set_pwm(self._convert_to_raw_pwm(values))
        self.state = values

    def _set_pwm(self, values):
        """
        Method stub for setting the pwm values.

        Has to be implemented by inheriting classes.
        :param values: Values to set (0.0-1.0).
        """
        raise NotImplementedError

    def _convert_to_raw_pwm(self, values):
        """
        Convert uniform pwm values to raw, driver-specific values.

        :param values: The uniform pwm values (0.0-1.0).
        :return: Converted, driver-specific pwm values.
        """
        return [int(round(values[i] * self._max_raw_value))
                for i in range(len(self.pins))]

    def _convert_to_uniform_pwm(self, values):
        """
        Convert raw pwm values to uniform  values.

        :param values: The raw pwm values.
        :return: Converted, uniform pwm values (0.0-1.0).
        """
        return [values[i] / self._max_raw_value for i in range(len(self.pins))]

    def transition(self, duration, values):
        """
        Transition from the current values to specified values.

        :param duration: The duration of the transition.
        :param values: The values to transition to.
        """
        raw_state = self._convert_to_raw_pwm(self.state)
        raw_values = self._convert_to_raw_pwm(values)
        steps = max(abs(raw_state[i] - raw_values[i])
                    for i in range(len(self.pins)))
        wait = duration / steps
        if wait < self.TRANSITION_MIN_WAIT:
            steps = int(math.floor(duration / self.TRANSITION_MIN_WAIT))
            wait = self.TRANSITION_MIN_WAIT

        for step in range(steps):
            start_time = datetime.now()
            progress = (step + 1) / steps
            values = [self._interpolate(raw_state[i], raw_values[i], progress)
                      for i in range(len(self.pins))]
            self.set_pwm(self._convert_to_uniform_pwm(values))
            time_delta = datetime.now() - start_time
            time.sleep(max(0, wait - time_delta.total_seconds()))

    @staticmethod
    def _interpolate(start, end, progress):
        """
        Interpolate a value from start to end at a given progress.

        :param start: The start value.
        :param end: The end value.
        :param progress: The progress.
        :return: The interpolated value at the given progress.
        """
        diff = end - start
        return start + progress * diff

    def stop(self):
        """Stop the driver and release resources."""
        self._stop()

    def _stop(self):
        """
        Method stub for stopping the driver.

        Has to be implemented by inheriting classes.
        """
        pass
