import trio
from zrgb.web_controller.web_server import web_server
from zrgb.led_controller.led_controller import led_controller


async def main(task_status=trio.TASK_STATUS_IGNORED):
    command_input, command_output = trio.open_memory_channel(0)

    async with trio.open_nursery() as nursery:
        nursery.start_soon(web_server, command_input)
        nursery.start_soon(led_controller, command_output)

if __name__ == "__main__":
    trio.run(main)
