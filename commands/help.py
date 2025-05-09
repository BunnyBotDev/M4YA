import logging
import discord
from discord import app_commands as apc

@apc.command(name="help", description="Returns bot help.")
async def _help(ctx):
    await ctx.send(f'Not implemented yet, someone help {ctx.author.display_name}.')

async def setup(bot: discord.Client):
    bot.tree.add_command(_help)
    # bot.logger.getLogger("M4YA.help").info("loading help")

async def teardown(bot: discord.Client):
    bot.tree.remove_command(_help)
    # logging.getLogger("M4YA.help").info("unloading help")
