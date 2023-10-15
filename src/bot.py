import interactions
from interactions import slash_command, SlashContext, OptionType, slash_option, Intents, Client, listen
from dotenv import load_dotenv
import os
import logging
import chromalog
from dotenv import set_key

chromalog.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

load_dotenv()


bot = Client(intents=Intents.ALL, activity=interactions.Activity(type=interactions.ActivityType.WATCHING, name="moodle.pucese.edu.ec"),
        status=interactions.Status.DO_NOT_DISTURB)


@listen()
async def on_ready():
    logger.info(f"logged in as {bot.user}")


@slash_command(name="update-credentials",
               description="Update Moodle session credentials.")
@slash_option(name="sesskey", description="insert value", opt_type=OptionType.STRING, required=True)
@slash_option(name="moodle_session", description="insert value", opt_type=OptionType.STRING, required=True)
async def update_keys(ctx: SlashContext, sesskey: str, moodle_session: str):
    set_key(".env", "sesskey", sesskey)
    set_key(".env", "MoodleSession", moodle_session)

    await ctx.send(content="Environment variables updated!")


bot.start(str(os.getenv('bot-token')))
