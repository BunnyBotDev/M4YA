import discord
from discord import app_commands as apc


@apc.command(name="serverinfo", description="Sends information about the Server")
async def serverinfo(interaction: discord.Interaction):
    e = discord.Embed(title=interaction.guild.name+"'s info", description="here is what I could find.")
    e.add_field(name="Guild Name", value=interaction.guild.name)
    e.add_field(name="Members", value=interaction.guild.member_count)
    e.add_field(name="Owner", value=interaction.guild.owner)
    e.add_field(name="Created At", value=interaction.guild.created_at)
    await interaction.response.send_message(embed=e)

async def setup(bot: discord.Client):
    bot.tree.add_command(serverinfo)

async def teardown(bot: discord.Client):
    bot.tree.remove_command(serverinfo)