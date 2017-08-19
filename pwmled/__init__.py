"""PWM controlled leds."""
from threading import Event
from collections import namedtuple


Color = namedtuple('Color', 'R G B')


class CancellationToken:
    """
    Represents a token that is used to cancel concurrent execution of tasks
    and wait for their completion.
    """

    def __init__(self):
        """Initialize the cancellation token."""
        self._request_event = Event()
        self._cancelled_event = Event()

    @property
    def is_cancellation_requested(self):
        """
        Gets a value determining whether cancellation was requested.

        :return: The value.
        """
        return self._request_event.is_set()

    def request_cancellation(self, timeout=None):
        """
        Requests the cancellation of the corresponding task.

        :param timeout: Timeout of the operation in seconds.
        """
        self._request_event.set()
        self._cancelled_event.wait(timeout)

    def confirm_cancellation(self):
        """Confirms that the task has been cancelled. """
        self._cancelled_event.set()
