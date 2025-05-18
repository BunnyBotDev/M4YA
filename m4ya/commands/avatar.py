import discord
from discord import app_commands as apc


@apc.command(name="avatar", description="Sends selected users Avatar as an embed.")
async def avatar(interaction: discord.Interaction, user: discord.User, ephemeral:bool=True):
    e = discord.Embed()
    e.set_image(url=str(user.avatar))
    await interaction.response.send_message(f"Here is {user.mention}'s avatar!", embed=e, ephemeral=ephemeral)


async def setup(bot: discord.Client):
    bot.tree.add_command(avatar)

async def teardown(bot: discord.Client):
    bot.tree.remove_command(avatar)