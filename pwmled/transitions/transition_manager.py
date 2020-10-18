"""Manager for led transitions."""
import time
import threading
from singleton import Singleton


class TransitionManager(object, metaclass=Singleton):
    """Represents a manager that executes transitions in a separate thread."""

    STEP_TIME = 0.001

    def __init__(self):
        """Initialize the manager."""
        self._thread = None
        self._transitions = []

    def execute(self, transition):
        """
        Queue a transition for execution.

        :param transition: The transition
        :return: The started transition.
        """
        self._transitions.append(transition)
        if self._thread is None or not self._thread.is_alive():
            self._thread = threading.Thread(
                target=self._transition_loop,
                daemon=True,
            )
            self._thread.start()

        return transition

    def _transition_loop(self):
        """Execute all queued transitions step by step."""
        while self._transitions:
            for transition in self._transitions:
                transition.step()
                if transition.finished:
                    self._transitions.remove(transition)

            time.sleep(self.STEP_TIME)
