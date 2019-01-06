"""Transition of a led."""
import time
import math
import threading


class Transition:
    """Represents a transition of a led."""

    def __init__(self, driver, duration, state_stages,
                 pwm_stages, callback=None):
        """
        Initialize the transition.

        :param driver: The driver of the led.
        :param duration: The duration.
        :param state_stages: The state stages to be executed.
        :param pwm_stages: The pwm stages to be executed.
        :param callback: Callback that is called when transition has finished.
        """
        self._driver = driver
        self._callback = callback
        self.duration = duration
        self.state_stages = state_stages
        self.pwm_stages = pwm_stages

        self.stage_index = 0
        self.cancelled = False
        self.finished = False
        self._finish_event = threading.Event()
        self._start_time = time.time()

    def step(self):
        """Apply the current stage of the transition based on current time."""
        if self.cancelled or self.finished:
            return

        if not self.pwm_stages:
            self._finish()
            return

        if self.duration == 0:
            progress = 1
        else:
            run_time = time.time() - self._start_time
            progress = max(0, min(1, run_time / self.duration))
        self.stage_index = math.ceil((len(self.pwm_stages) - 1) * progress)
        stage = self.pwm_stages[self.stage_index]
        self._driver.set_pwm(stage)

        if progress == 1:
            self._finish()

    def _finish(self):
        """Mark transition as finished and execute callback."""
        self.finished = True
        if self._callback:
            self._callback(self)
        self._finish_event.set()

    def wait(self, timeout=None):
        """
        Wait for transition to be finished.

        :param timeout: Timeout of the operation in seconds.
        """
        self._finish_event.wait(timeout=timeout)

    def cancel(self):
        """
        Cancel the transition.
        """
        self._finish()
        self.cancelled = True
