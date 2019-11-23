import hypercorn
import hypercorn.trio
from quart import render_template, request
from quart_trio import QuartTrio


class Command:
    @classmethod
    def factory(cls, request):
        return Command(
            mode=request.view_args["mode"],
            details=request.args
        )

    def __init__(self, mode, details):
        self.mode = mode
        self.details = details

    def __repr__(self):
        return f'Command(mode="{self.mode}", details="{self.details}")'


async def web_server(command_input):
    app = QuartTrio(__name__)

    @app.route("/")
    async def index():
        return await render_template("index.html")

    @app.route("/api/<path:mode>")
    async def api(mode):
        await command_input.send(Command.factory(request))
        return "", 200

    config = hypercorn.Config.from_mapping(
        bind="0.0.0.0:5000",
        worker_class="trio",
        accesslog="-",
        errorlog="-"
    )

    await hypercorn.trio.serve(app, config)
