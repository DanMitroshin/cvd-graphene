
class AbstractController(object):
    """
    Class for device controllers
    """

    def send(self, *args, **kwargs):
        """
        Send value to sensor
        :param args:
        :param kwargs:
        :return: any value from sensor answer
        """
        pass

    def wait_seconds(self, seconds, after_wait=None, **kwargs):
        """

        :param after_wait: function for execute after waiting
        :param seconds: amount of seconds
        :param kwargs:
        :return:
        """
        pass

    def wait_until_value(self, value, on_reached=None, **kwargs):
        """
        Wait time until target value is not reached
        :param on_reached: function for execute after value is reached
        :param value: target value
        :param kwargs:
        :return:
        """
