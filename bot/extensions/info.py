import lightbulb
import hikari
from hikari import Embed
from datetime import datetime
import pytz
import miru


plugin = lightbulb.Plugin("Info", "📝 Course info")


def load(bot: lightbulb.BotApp) -> None:
    bot.add_plugin(plugin)


@plugin.command()
@lightbulb.command('teo', 'Introduction', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def get_info(ctx: lightbulb.Context):
    bot: hikari.Member = await ctx.app.rest.fetch_member(
        ctx.guild_id, 1263431825435656233)

    questions = 1263431825435656233
    embed = (
        Embed(
            title=f"🧋 A greeting from T.è.o",
            colour="#118ab2",
            url="https://teodocs.vercel.app/",
            description=f"Hello, I'm T.è.o, a virtual assistant for Coderschool TA. I'm here to help you with your learning journey.\n\nEvery week, our tutor will send you a recap note on the topics we just discussed. You can find it on the <#{1239136186241650688}> channel.\n\n Or jump into <#1236972732076523561> to view the resources that has been dedicatedly selected for you. \n\nIf you have any questions, feel free to ask my fellow <@&1233260164233297942> via #questions. They will be here to help you.",
            timestamp=datetime.now().astimezone(pytz.timezone('Asia/Ho_Chi_Minh'))
        )
        .set_thumbnail(bot.avatar_url)
        .set_footer(
            text=f"Requested by {ctx.author.username}",
            icon=ctx.author.avatar_url
        )
    )
    await ctx.respond(embed)


@plugin.command()
@lightbulb.option('code', 'Your code')
@lightbulb.command('submit', 'Submit code', auto_defer=True)
@lightbulb.implements(lightbulb.SlashCommand)
async def get_info(ctx: lightbulb.Context):
    code = ctx.options.code
    await ctx.respond(f"```python {code} ```")


# Define a new custom View that contains 3 items
class BasicView(miru.View):

    # Define a new TextSelect menu with two options
    @miru.text_select(
        placeholder="Select me!",
        options=[
            miru.SelectOption(label="Option 1"),
            miru.SelectOption(label="Option 2"),
        ],
    )
    async def basic_select(self, ctx: miru.ViewContext, select: miru.TextSelect) -> None:
        await ctx.respond(f"You've chosen {select.values[0]}!")

    # Define a new Button with the Style of success (Green)k
    @miru.button(label="Click me!", style=hikari.ButtonStyle.SUCCESS)
    async def basic_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        await ctx.respond("You clicked me!")

    # Define a new Button that when pressed will stop the view
    # & invalidate all the buttons in this view
    @miru.button(label="Stop me!", style=hikari.ButtonStyle.DANGER)
    async def stop_button(self, ctx: miru.ViewContext, button: miru.Button) -> None:
        self.stop()  # Called to stop the view


@plugin.command()
@lightbulb.command("name", "description", auto_defer=False)
@lightbulb.implements(lightbulb.SlashCommand)
async def some_slash_command(ctx: lightbulb.SlashContext) -> None:
    # Create a new instance of our view
    view = BasicView()
    await ctx.respond("Hello miru!", components=view)

    # Assign the view to the client and start it
    client = miru.Client(plugin.app)
    client.start_view(view)
