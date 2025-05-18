from random import randint
import discord
from discord import app_commands as apc
from ..utils import derpibooru


@apc.command(name="randompony", description="fetches a random pony on derpibooru, optionally with a search.")
@apc.describe(tags="a list of comma separated tags as on derpibooru ex: `vinyl scratch,octavia melody`")
async def _randompony(interaction: discord.Interaction, tags: str=""):
    report_channel = interaction.client.config['pony']['report_channel']
    #filters made for this specifically
    filter_id = interaction.client.config['pony']['sfw_filter']
    if interaction.channel.is_nsfw():
        filter_id = interaction.client.config['pony']['nsfw_filter']
    #make sure a tag is searched for, api doesn't return anything otherwise.
    if tags == "":
        tags = "safe" if not interaction.channel.is_nsfw() else "explicit"

    #check if the user is trying to bypass the filter, for some specific tags.
    split_tags = tags.split(',')
    if 'foalcon' in split_tags:
        await interaction.client.get_channel(report_channel).send(f"user {interaction.user.mention} attempted to bypass important filters for randompony in {interaction.channel}\n tags: [{', '.join(split_tags)}]")
        await interaction.response.send_message("No.", ephemeral=True)
        return
    if not interaction.channel.is_nsfw() and '-safe' in split_tags:
        await interaction.response.send_message("this is not an nsfw channel, you seem to be trying to bypass our filters, this has been logged.", ephemeral=True)
        await interaction.client.get_channel(report_channel).send(f"user {interaction.user.mention} attempted to bypass filters for randompony in {interaction.channel}\n tags: [{', '.join(split_tags)}]")
        return

    #do a search to check how many results there are.
    args = {"q": tags, "filter_id": filter_id, "per_page": 1}
    total = (await derpibooru.search(args))['total']
    try:
        #pick one of those results at random
        args['page'] = randint(1, total)
    except ValueError: #error: 0 results.
        await interaction.response.send_message(f"Searching for {tags} with filter [{filter_id}](https://derpibooru.org/filters/{filter_id}) seems to have returned nothing.", ephemeral=True)
    info = await derpibooru.search(args)

    embed = await derpibooru.image_data_to_embed(info['images'][0])

    #just confirm that it didn't somehow end up on an nsfw post in a non-nsfw channel.
    if not interaction.channel.is_nsfw() and not "safe" in info['images'][0]['tags']:
        await interaction.response.send_message("this is not an nsfw channel, you seem to be trying to bypass our filters, this has been logged.", ephemeral=True)
        await interaction.client.get_channel(report_channel).send(f"user {interaction.user.mention} attempted to bypass filters for randompony in {interaction.channel}\n tags: [{', '.join(split_tags)}]")
        return

    await interaction.response.send_message(embed=embed)




async def setup(bot: discord.Client):
    bot.tree.add_command(_randompony)

async def teardown(bot: discord.Client):
    bot.tree.remove_command(_randompony)