"""Manager for led transitions."""
import time
import threading
from singleton import Singleton


class TransitionManager(object, metaclass=Singleton):
    """Represents a manager that executes transitions in a separate thread."""

    MIN_STEP_TIME = 0.001

    def __init__(self):
        """Initialize the manager."""
        self._thread = None
        self._transitions = []

    def execute(self, transition):
        """
        Queue a transition for execution.

        :param transition: The transition
        """
        self._transitions.append(transition)
        if self._thread is None or not self._thread.isAlive():
            self._thread = threading.Thread(target=self._transition_loop)
            self._thread.setDaemon(True)
            self._thread.start()

    def _transition_loop(self):
        """Execute all queued transitions step by step."""
        while self._transitions:
            start = time.time()
            for transition in self._transitions:
                transition.step()
                if transition.finished:
                    self._transitions.remove(transition)

            time_delta = time.time() - start
            sleep_time = max(0, self.MIN_STEP_TIME - time_delta)
            time.sleep(sleep_time)
