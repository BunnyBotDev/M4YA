import logging
from typing import Optional
import discord
from discord import app_commands as apc
from ..utils import derpibooru


@apc.command(name="pony", description="posts a specific pony by derpibooru id.")
async def _pony(interaction: discord.Interaction, image_id:Optional[int]=0):
    embed, is_safe = await derpibooru.id_to_embed(image_id)

    ## NSFW check
    if not interaction.channel.is_nsfw() and not is_safe:
        await interaction.response.send_message(f"post {image_id} is nsfw, this is not an nsfw channel.", ephemeral=True)
        return

    await interaction.response.send_message(embed=embed)


async def setup(bot: discord.Client):
    bot.tree.add_command(_pony)

async def teardown(bot: discord.Client):
    bot.tree.remove_command(_pony)