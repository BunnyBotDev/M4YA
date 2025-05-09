import discord
from discord import app_commands as apc


@apc.command()
async def userinfo(interaction: discord.Interaction, user: discord.User):
    e = discord.Embed(title=user.display_name+"'s info", description="Here is what I could find.", color=user.accent_color)
    e.add_field(name='Title', value=user.name)
    e.add_field(name='User ID', value=user.id)
    e.add_field(name='Status', value=user.status)
    e.add_field(name='Highest Role', value=user.top_role)
    e.add_field(name='Join Date', value=user.joined_at)
    e.add_field(name='Registration Date', value=user.created_at)
    e.add_field(name='Profile Picture', value=user.avatar)
    if user.avatar is not None:
        #setting the embeds image to the users avatar that was passed via discord.User
        e.set_image(url=str(user.avatar))
    await interaction.response.send_message(f"Heres is <@{user.id}>'s info!", embed=e, ephemeral=False)

async def setup(bot: discord.Client):
    bot.tree.add_command(userinfo)