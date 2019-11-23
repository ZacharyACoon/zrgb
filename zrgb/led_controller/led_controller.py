import trio
from zrgb.strip.LEDs import LEDs
from zrgb.led_controller.modes.life_frame_factory import LifeFrameFactory


class LEDController:
    def __init__(self, nursery):
        self.leds = LEDs(18, 269, brightness=5)
        self.nursery = nursery
        self.modes = {
            "life": LifeFrameFactory
        }

    async def worker(self, frame_factory):
        for frame in frame_factory:
            for n, v in enumerate(frame):
                self.leds.set_led(n, v)
            self.leds.show()
            await trio.sleep(3)

    def mode(self, mode, details):
        for task in self.nursery.child_tasks:
            print(task)
            print(dir(task))

        if mode in self.modes:
            self.nursery.start_soon(self.worker, self.modes[mode](self.leds.size))


async def led_controller(command_output):
    async with trio.open_nursery() as nursery:
        controller = LEDController(nursery)
        while True:
            async for command in command_output:
                controller.mode(command.mode, command.details)
            await trio.sleep(0.25)
