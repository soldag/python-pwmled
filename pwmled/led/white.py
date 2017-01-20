from pwmled.led import Led


class WhiteLed(Led):
    """Represents a white led that can be controlled."""
    def _get_pwm_values(self):
        """
        Get the pwm values.

        :return: The pwm values.
        """
        return [1]
