"""Token for cancellation of transitions."""
from threading import Event


class CancellationToken:
    """Represents a token used to cancel concurrent execution of tasks."""

    def __init__(self):
        """Initialize the cancellation token."""
        self._request_event = Event()
        self._cancelled_event = Event()

    @property
    def is_cancellation_requested(self):
        """
        Get a value determining whether cancellation was requested.

        :return: The value.
        """
        return self._request_event.is_set()

    def request_cancellation(self, timeout=None):
        """
        Request the cancellation of the corresponding task.

        :param timeout: Timeout of the operation in seconds.
        """
        self._request_event.set()
        self._cancelled_event.wait(timeout)

    def confirm_cancellation(self):
        """Confirm that the task has been cancelled."""
        self._cancelled_event.set()
