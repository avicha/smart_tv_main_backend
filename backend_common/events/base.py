# coding=utf-8
from blinker import signal


class BaseEvent():

    def __init__(self):
        self.name = self.__class__.__name__
        self.signal = signal(self.name)
        self.signal.connect(self.handle)

    def send(self, sender, **args):
        return self.signal.send(sender, **args)

    def handle(self, sender, **args):
        return
