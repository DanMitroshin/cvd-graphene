# import wiringpi


class BaseCommunicationMethod:
    def __init__(self, *args, **kwargs):
        self.ready = False
        self.rs485 = None

    def setup(self, *args, **kwargs):
        self.ready = True

    # def check_ready(func):
    #     def wrapper()

    def send(self, *args, **kwargs):
        raise NotImplementedError


# class ExampleBaseCommunicationMethod(BaseCommunicationMethod):
#     def setup(self, *args, **kwargs):
#         wiringpi.wiringPiSetup()
#
#     def send(self, *args, **kwargs):
#         wiringpi.pinMode(6, 1)
