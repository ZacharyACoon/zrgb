from .frame_factory import FrameFactory
from zrgb.led_controller.modes.util.life import Life


class LifeFrameFactory(FrameFactory):
    def __init__(self, size):
        self.life = Life(size)

    def __iter__(self):
        return self

    def __next__(self):
        self.life.new_generation()
        frame = [0xff0000 if _ else 0 for _ in self.life.population]
        return frame
