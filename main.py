import logging
from logging import handlers
from pathlib import Path

import yaml
import discord
from discord.utils import _ColourFormatter
# from discord import app_commands as apc
from discord.ext import commands


CONFIG_PATH = Path("config.yaml")
COMMANDS_PATH = Path("commands")
LOOPS_PATH = Path("loops")


try:
    with CONFIG_PATH.open('r', encoding="utf-8") as config_file:
        config = yaml.safe_load(config_file)
except FileNotFoundError as e:
    raise FileNotFoundError("Config file missing, please copy config.yaml.example to config.yaml and configure as needed.") from e



class Bot(commands.bot.Bot):
    VERSION = "dev-0"
    def __init__(self, settings, *args, **kwargs):
        self.logger = logging.getLogger('M4YA')
        self.config = settings
        self.developmentGuild = discord.Object(id=config['main']['guild_id'])
        super().__init__(*args, **kwargs)

    # def write_config(self):
    #     with CONFIG_PATH.open('w', encoding="utf-8") as config_file:
    #         yaml.safe_dump(config_file)

    async def setup_hook(self):
        await self.load_loops()
        await self.load_commands()
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=self.developmentGuild)
        await self.tree.sync(guild=self.developmentGuild)

    async def load_commands(self):
        for i in COMMANDS_PATH.glob("*.py"):
            await self.load_extension(i.as_posix()[:-3].replace('/', '.'))

    async def load_loops(self):
        for i in LOOPS_PATH.glob("*.py"):
            await self.load_extension(i.as_posix()[:-3].replace('/', '.'))


intents = discord.Intents.all()
client = Bot(config, "M4YA- ", intents=intents)

@client.event
async def on_ready():
    client.logger.info('Connected Successfully! M4YA Version %s', client.VERSION)


if __name__ == "__main__":
    console_handler = logging.StreamHandler()
    log_path = Path(config['main']['log_path'])
    log_path.mkdir(exist_ok=True)
    file_handler = handlers.TimedRotatingFileHandler(log_path/"M4YA.log", 'midnight', encoding="utf-8")

    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', style='{')

    console_handler.setFormatter(_ColourFormatter())
    file_handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logging.getLogger('discord').setLevel(logging.INFO)
    logging.getLogger('M4YA').setLevel(logging.DEBUG)


    del log_path, file_handler, console_handler, formatter, logger


    client.run(client.config['main']['bot_token'], log_handler=None)
