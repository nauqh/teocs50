import bot
import hikari
import lightbulb
import miru

import os
from dotenv import load_dotenv

load_dotenv()


app = lightbulb.BotApp(
    os.environ['TOKEN'],
    intents=hikari.Intents.ALL,
    default_enabled_guilds=[os.environ['GUILD_ID']],
    help_slash_command=True,
    banner=None
)

app.load_extensions_from("./bot/extensions", must_exist=True)


@app.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent) -> None:
    app.d.admin = await app.rest.fetch_user(os.environ['ADMIN'])


def run() -> None:
    app.run(
        activity=hikari.Activity(
            name=f"v{bot.__version__}",
            type=hikari.ActivityType.LISTENING,
            state="💡teodocs | /help"
        )
    )
