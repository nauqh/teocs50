import bot
import hikari
import lightbulb

import asyncio
import os
from dotenv import load_dotenv
from bot.utils.embed import noti_embed
from bot.utils.helpers import today, yesterday

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


async def check_threads(
    guild: int,
    forum_channel: int,
    staff_channel: int,
    mentor_role=1233260164233297941
):
    CHECK_INTERVAL = 2000
    while True:
        await asyncio.sleep(CHECK_INTERVAL)
        threads = [
            thread for thread in await app.rest.fetch_active_threads(guild)
            if isinstance(thread, hikari.GuildThreadChannel) and
            thread.parent_id == int(forum_channel) and
            thread.created_at.date() in [today(), yesterday()]
        ]
        for thread in threads:
            messages: list[hikari.Message] = await thread.fetch_history()
            members = {message.author.id for message in messages}
            if len(members) <= 1:
                author = await app.rest.fetch_member(guild, thread.owner_id)
                attachments = [att.url for att in messages[0].attachments]

                embed = noti_embed(thread.name,
                                   messages[0].content,
                                   f"https://discord.com/channels/{thread.guild_id}/{thread.id}", author)

                if attachments:
                    embed.set_image(attachments[0])

                await app.rest.create_message(
                    staff_channel,
                    content=(
                        f"<@&{mentor_role}> "
                        "this thread remains unresolved for more than 15min"),
                    embed=embed
                )


@app.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent) -> None:
    asyncio.create_task(
        check_threads(os.environ['GUILD_ID'],
                      os.environ['FORUM_CHANNEL1'], os.environ['STAFF_CHANNEL'])
    )
    asyncio.create_task(
        check_threads(os.environ['GUILD_ID'],
                      os.environ['FORUM_CHANNEL2'], os.environ['STAFF_CHANNEL'])
    )


def run() -> None:
    app.run(
        activity=hikari.Activity(
            name=f"v{bot.__version__}",
            type=hikari.ActivityType.LISTENING,
            state="💡teodocs | /help"
        )
    )
