import trio
from zrgb.strip import mode


class LedController:
    def __init__(self, leds):
        self.leds = leds
