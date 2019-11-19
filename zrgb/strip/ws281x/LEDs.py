import _rpi_ws281x as ws


class LEDs:
    def __init__(
            self,
            pin,
            count,
            brightness=255,
            strip_type=ws.WS2811_STRIP_GRB,
            frequency=800000,
            dma=5,
            invert=0,
            channel=0
    ):
        self.size = count
        self.channel = channel
        self._data = ws.new_ws2811_t()

        # reset
        for n in range(2):
            c = ws.ws2811_channel_get(self._data, n)
            ws.ws2811_channel_t_count_set(c, 0)
            ws.ws2811_channel_t_gpionum_set(c, 0)
            ws.ws2811_channel_t_invert_set(c, 0)
            ws.ws2811_channel_t_brightness_set(c, 0)

        # initialize
        self._channel = ws.ws2811_channel_get(self._data, self.channel)
        ws.ws2811_channel_t_count_set(self._channel, self.size)
        ws.ws2811_channel_t_gpionum_set(self._channel, pin)
        ws.ws2811_channel_t_invert_set(self._channel, invert)
        ws.ws2811_channel_t_brightness_set(self._channel, brightness)
        ws.ws2811_channel_t_strip_type_set(self._channel, strip_type)

        ws.ws2811_t_freq_set(self._data, frequency)
        ws.ws2811_t_dmanum_set(self._data, dma)

        ws.ws2811_init(self._data)

    def __del__(self):
        ws.delete_ws2811_t(self._data)

    def __len__(self):
        return ws.ws2811_channel_t_count_get(self._channel)

    def get_led(self, n):
        return ws.ws2811_led_get(self._channel, n % self.size)

    def set_led(self, n, v):
        return ws.ws2811_led_set(self._channel, n % self.size, v)

    def __getitem__(self, pos):
        if isinstance(pos, slice):
            return [self.get_led(n) for n in range(pos.indices(self.size))]
        else:
            return self.get_led(pos)

    def __setitem__(self, pos, value):
        if isinstance(pos, slice):
            for i, p in enumerate(pos.indices(self.size)):
                return self.set_led(p, value[i])
        else:
            return self.set_led(pos, value)

    def show(self):
        ws.ws2811_render(self._data)
