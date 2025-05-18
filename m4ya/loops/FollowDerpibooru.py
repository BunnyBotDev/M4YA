import logging
from pathlib import Path
import json
from discord.ext import tasks, commands
from ..utils import derpibooru

STORAGE = Path(__file__).parent.parent / 'data' / 'pony'

class DerpibooruChecker(commands.Cog):
    def __init__(self, bot: commands.Bot, last_id: int, query: str):
        self.bot = bot
        self.last_id = last_id
        self.args = {'q':query, 'per_page':5, 'filter_id':self.bot.config['pony']['sfw_filter']}
        self.channel = bot.config['pony']['follow_channel']

    @commands.Cog.listener()
    async def on_ready(self):
        logging.getLogger("M4YA.DerpibooruChecker").info("Starting to check for new posts...")
        await self.watch_for_posts()
        self.watch_for_posts.start()


    @tasks.loop(minutes=15)
    async def watch_for_posts(self):
        info = await derpibooru.search(self.args)
        #oldest to newest
        for image in reversed(info['images']):
            if image['id'] > self.last_id: #ids are in upload order.
                await self.bot.get_channel(self.channel).send(embed=await derpibooru.image_data_to_embed(image))
                self.last_id = image['id']
        with (STORAGE/'follow.json').open('w+') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
            data[self.args['q']] = self.last_id
            json.dump(data, f)



async def setup(bot: commands.Bot):
    followquery = bot.config['pony']['follow_query']
    if followquery is False:
        return
    STORAGE.mkdir(exist_ok=True, parents=True)
    try:
        with (STORAGE/'follow.json').open('r') as f:
            last_id = json.load(f)[followquery]
    except FileNotFoundError:
        last_id = 0
    except ValueError:
        last_id = 0

    await bot.add_cog(DerpibooruChecker(bot, last_id, followquery))

async def teardown(bot: commands.Bot):
    await bot.remove_cog("DerpibooruChecker")
    logging.getLogger("M4YA.DerpibooruChecker").info("Stopping.")
