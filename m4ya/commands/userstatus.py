import discord
from discord import app_commands as apc


@apc.command(name="userstatus", description="Sends the Users status")
async def userstatus(interaction: discord.Interaction, member: discord.Member,  ephemeral:bool=True):
    member = interaction.guild.get_member(member.id)

        # Fetch user status
    status = str(member.status)

        # Fetch user activities
    activities = '\n---\n'.join([str(activity) for activity in member.activities])

        # Create an embed message
    e = discord.Embed(title=f"{member.display_name}'s Status and Activities", description=None, color=member.accent_color)
    e.add_field(name='Status', value=status)
    e.add_field(name='Activities', value=activities or 'No activities')

        # Check if the user is listening to Spotify
    for activity in member.activities:
        if isinstance(activity, discord.Spotify):
            spotify = activity
            e.add_field(name="",value="")
            e.add_field(name='Listening to', value=spotify.title, inline=True)
            e.add_field(name='Artist', value=', '.join(spotify.artists), inline=True)
            e.add_field(name='Album', value=spotify.album, inline=True)
            e.add_field(name='Track Link', value=spotify.track_url, inline=False)
            e.add_field(name='Started Playing', value=spotify.start.strftime('%H:%M:%S'), inline=True)
            e.add_field(name='Duration', value=str(spotify.duration // 1000000 * 1000000), inline=True) #division and multiplication to strip miliseconds.
            e.set_image(url=spotify.album_cover_url)
            break

    await interaction.response.send_message(embed=e, ephemeral=ephemeral)

async def setup(bot: discord.Client):
    bot.tree.add_command(userstatus)

async def teardown(bot: discord.Client):
    bot.tree.remove_command(userstatus)