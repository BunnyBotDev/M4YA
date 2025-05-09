import discord
from discord import app_commands as apc


@apc.command()
async def avatar(interaction: discord.Interaction, user: discord.User):
    e = discord.Embed()
    e.set_image(url=str(user.avatar))
    await interaction.response.send_message(f"Here is {user.mention}'s avatar!", embed=e, ephemeral=True)


async def setup(bot: discord.Client):
    bot.tree.add_command(avatar)
