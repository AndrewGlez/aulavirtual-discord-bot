import asyncio
import interactions
from interactions import slash_command, SlashContext, OptionType, slash_option, Intents, Client, listen
from dotenv import load_dotenv
import os
import logging
import chromalog
from dotenv import set_key
import json
from bs4 import BeautifulSoup
from page_format import get_page
import traceback


chromalog.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

load_dotenv()


bot = Client(intents=Intents.ALL,
             activity=interactions.Activity(type=interactions.ActivityType.WATCHING,
                                            name="moodle.pucese.edu.ec"),
             status=interactions.Status.DO_NOT_DISTURB)


@listen()
async def on_ready():
    logger.info(f"logged in as {bot.user}")
    while True:
        try:
            if await compare_data():
                await send_to()
            else:
                await asyncio.sleep(600)
        except Exception:
            logger.error(f'{traceback.format_exc()}')
            error_embed = interactions.Embed(description=f'```{(traceback.format_exc())}```',
                                             color=interactions.Color.from_rgb(255,0,0))
            await bot.get_channel(1152584034053001296)\
                .send(embed=error_embed)
            break


@slash_command(name="update-credentials",
               description="Update Moodle session credentials.")
@slash_option(name="sesskey",
              description="insert value",
              opt_type=OptionType.STRING,
              required=True)
@slash_option(name="moodle_session",
              description="insert value",
              opt_type=OptionType.STRING,
              required=True)
async def update_keys(ctx: SlashContext,
                      sesskey: str,
                      moodle_session: str):
    set_key(".env", "sesskey", sesskey)
    set_key(".env", "MoodleSession", moodle_session)

    await ctx.send(content="Environment variables updated!")


async def send_to():
    channel = None
    author = None
    color = None
    course_image = None
    with open('task.json', 'r') as f:
        data = json.load(f)

        tasks_list = data[0]['data']['events']

        for task in tasks_list:

            id = task['course']['id']
            task_name = task['name']
            #description = task['description'].replace("\\", "").replace("\r", "").replace("\n", "")
            direct_url = task['url']
            #course_name = task['course']['fullname']
            time = task['formattedtime']
            #instance = task['instance']

            # format remaining time
            soup_time = BeautifulSoup(time, 'html.parser')
            formatted_time = soup_time.text

            # format description
            try:
                params = os.getenv('MoodleSession')
                box, links = get_page(params, direct_url)
                formatted_desc = box
            except:
                box = "null"
            
            # img's and authors
            with open('imgs.json', 'r') as d:
                data = json.load(d)
                if id == 204:
                    channel = bot.get_channel(1145851499889569863)
                    author = interactions.EmbedAuthor(name='Jose Luis Carvajal',
                                                      icon_url=data[0]['docente']['carvajal'])
                    color = interactions.Color.from_rgb(255, 153, 255)
                    course_image = data[0]['cursos']['SO']
                if id == 203:
                    channel = bot.get_channel(1145851080425611286)
                    author = interactions.EmbedAuthor(name='Jose Luis Carvajal',
                                                      icon_url=data[0]['docente']['carvajal'])
                    color = interactions.Color.from_rgb(222, 175, 255)
                    course_image = data[0]['cursos']['FCC']
                if id == 201:
                    channel = bot.get_channel(1145851213854818334)
                    author = interactions.EmbedAuthor(name='Jaime Paúl Sayago',
                                                      icon_url=data[0]['docente']['sayago'])
                    color = interactions.Color.from_rgb(218, 247, 166)
                    course_image = data[0]['cursos']['POO']
                if id == 216:
                    channel = bot.get_channel(1145851213854818334)
                    author = interactions.EmbedAuthor(name='Homero Velastegui',
                                                      icon_url=data[0]['docente']['homero'])
                    color = interactions.Color.from_rgb(88, 24, 69)
                    course_image = data[0]['cursos']['RD']
                if id == 205:
                    channel = bot.get_channel(1145851213854818334)
                    author = interactions.EmbedAuthor(name='Pablo Pico',
                                                      icon_url=data[0]['docente']['pico'])
                    color = interactions.Color.from_rgb(94, 0, 75)
                    course_image = data[0]['cursos']['IOT']
                if id == 202:
                    channel = bot.get_channel(1145851213854818334)
                    author = interactions.EmbedAuthor(name='Jaime Paúl Sayago',
                                                      icon_url=data[0]['docente']['sayago'])
                    color = interactions.Color.from_rgb(44, 94, 0)
                    course_image = data[0]['cursos']['BDD']
                if id == 651:
                    channel = bot.get_channel(1145851144510373999)
                    author = interactions.EmbedAuthor(name='Homero Velastegui',
                                                      icon_url=data[0]['docente']['homero'])
                    color = interactions.Color.from_rgb(44, 94, 0)
                    course_image = data[0]['cursos']['TA']

            # embed constructor
            field_list = [
                interactions.EmbedField(
                    name='Descripción',
                    value=f'{formatted_desc}',

                ),
                interactions.EmbedField(
                    name='Links',
                    value=f'> {links}',
                )]
            full_embed = interactions.Embed(
                author=author,
                title=task_name,
                url=direct_url,
                fields=field_list,
                color=color,
                thumbnail=bot.user.avatar_url,
                images=interactions.EmbedAttachment(url=course_image),
                footer=interactions.EmbedFooter(text=formatted_time, 
                                                icon_url='https://cdn-icons-png.flaticon.com/512/66/66163.png')
            )

            await channel.send(embed=full_embed)


async def compare_data():
    logger.debug('Start fetching task.....')
    from save_tasks import fetch_task

    # Fetch new data
    new_data = fetch_task()

    # Current local data
    try:
        with open('task.json', 'r+') as f:
            current_data = json.load(f)
            # Compare
            new_ids = {item['id'] for item in new_data[0]['data']['events']}
            current_ids = {item['id'] for item in current_data[0]['data']['events']}
            if new_ids != current_ids:
                f.seek(0)
                f.truncate()
                f.write(json.dumps(new_data, indent=2))
                return True
            return False
    except:
        with open('task.json', 'w') as f:
            f.seek(0)
            f.truncate()
            f.write(json.dumps(new_data, indent=2))



bot.start(str(os.getenv('bot-token')))
