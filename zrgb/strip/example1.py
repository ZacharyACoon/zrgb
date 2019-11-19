from zrgb.strip.ws281x.LEDs import LEDs
from zrgb.strip.mode.lib.life_1d import Life
import trio


async def producer(frame_factory, frame_input):
    while True:
        await frame_input.send(frame_factory.loop())
        await trio.sleep(2)


async def consumer(leds, frame_output):
    while True:
        async for frame in frame_output:
            for i, v in enumerate(frame):
                leds.set_led(i, 0xff0000 if v else 0)
            leds.show()


async def main(frame_factory, leds):
    async with trio.open_nursery() as nursery:
        frame_input, frame_output = trio.open_memory_channel(0)
        nursery.start_soon(producer, frame_factory, frame_input)
        nursery.start_soon(consumer, leds, frame_output)


leds = LEDs(18, 269, brightness=5)
life = Life(leds.size)
trio.run(main, life, leds)
