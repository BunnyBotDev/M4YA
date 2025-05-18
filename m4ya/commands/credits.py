import logging
from pathlib import Path
import discord
from discord import app_commands as apc

@apc.command(name="credits", description="Sends the Credits")
async def _credits(interaction: discord.Interaction):
    with Path("credits.txt").open() as f:
        embed = discord.Embed(colour=discord.Colour.fuchsia(), title="Credits", description=f.read())
        await interaction.response.send_message(embed=embed)

async def setup(bot: discord.Client):
    bot.tree.add_command(_credits)

async def teardown(bot: discord.Client):
    bot.tree.remove_command(_credits)