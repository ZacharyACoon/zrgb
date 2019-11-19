from .lib.life_1d import Life


class FrameFactory:
    def __init__(self, size, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.life = Life(size)

    def __iter__(self):
        return self

    def next(self):
        self.life.new_generation()
        frame = [0xff0000 if _ else 0 for _ in self.life.population]
        return frame
