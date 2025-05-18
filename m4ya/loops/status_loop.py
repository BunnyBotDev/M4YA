import logging
from random import choice
import aiohttp
import yaml
import discord
from discord.ext import tasks, commands

class StatusLoop(commands.Cog):
    def __init__(self, bot: commands.Bot, status: list):
        self.bot = bot
        self.status = status

    @commands.Cog.listener()
    async def on_ready(self):
        await self.change_status()
        self.change_status.start()

    @tasks.loop(seconds=60)
    async def change_status(self):
        activity = discord.activity.CustomActivity(choice(self.status))
        await self.bot.change_presence(activity=activity)

async def setup(bot: commands.Bot):
    status = bot.config['status']['status'] # Preloaded list from config.
    loaded_external = False
    status_url = bot.config['status'].get('status_url', False) #online list, default value False if it's not there.
    if status_url is not False:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(status_url) as response:
                    status = yaml.safe_load(await response.read())['statuses']
                    loaded_external = True
        except (aiohttp.ClientError, yaml.YAMLError):
            pass # These exceptions might happen if anything goes wrong loading, don't error, just fallback to local.
    if len(status) < 1:
        logging.getLogger("M4YA.status").info("Not Starting status loop, no statuses configured.")
        return #back out of loading if there's not any statuses to set, this will just error later.

    await bot.add_cog(StatusLoop(bot, status))
    logging.getLogger("M4YA.status").info("Starting Status loop: %s", "online" if loaded_external else "local")

async def teardown(bot: commands.Bot):
    await bot.remove_cog("StatusLoop")
    logging.getLogger("M4YA.status").info("Stopping Status Loop.")
