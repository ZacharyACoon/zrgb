import hypercorn
import hypercorn.trio
from quart import render_template
from quart_trio import QuartTrio


async def web_server():
    app = QuartTrio(__name__)

    @app.route("/")
    async def index():
        return await render_template("index.html")

    config = hypercorn.Config.from_mapping(
        bind="0.0.0.0:5000",
        worker_class="trio",
        accesslog="-",
        errorlog="-"
    )

    await hypercorn.trio.serve(app, config)
