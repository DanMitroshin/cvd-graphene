# import wiringpi


class BaseCommunicationMethod:
    def setup(self, *args, **kwargs):
        pass

    def send(self, *args, **kwargs):
        pass


# class ExampleBaseCommunicationMethod(BaseCommunicationMethod):
#     def setup(self, *args, **kwargs):
#         wiringpi.wiringPiSetup()
#
#     def send(self, *args, **kwargs):
#         wiringpi.pinMode(6, 1)
