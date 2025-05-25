import discord
from discord import app_commands as apc
from ..utils import derpibooru


@apc.command(name="pony", description="fetches a random pony on derpibooru, optionally with a search.")
@apc.describe(tags="a list of comma separated tags as on derpibooru ex: `vinyl scratch,octavia melody`", count="How many ponies to grab")
async def _pony(interaction: discord.Interaction, tags: str="", count: apc.Range[int, 1, 8]=1):
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
        await interaction.client.get_channel(report_channel).send(f"user {interaction.user.mention} attempted to bypass filters in {interaction.channel}\n tags: [{', '.join(split_tags)}]")
        await interaction.response.send_message("No.", ephemeral=True)
        return
    if not interaction.channel.is_nsfw() and '-safe' in split_tags:
        await interaction.response.send_message("this is not an nsfw channel, you seem to be trying to bypass our filters, this has been logged.", ephemeral=True)
        await interaction.client.get_channel(report_channel).send(f"user {interaction.user.mention} attempted to bypass filters in {interaction.channel}\n tags: [{', '.join(split_tags)}]")
        return

    #do a search to check how many results there are.
    args = {"q": tags, "filter_id": filter_id, "per_page": count, "sf":"random"}
    info = await derpibooru.search(args)
    if info['total'] == 0:
        await interaction.response.send_message(f"Searching for {tags} with filter [{filter_id}](https://derpibooru.org/filters/{filter_id}) returned 0 results.", ephemeral=True)
        return


    all_embeds = [await derpibooru.image_data_to_embed(x) for x in info['images']]
    #just confirm that it didn't somehow end up on an nsfw post in a non-nsfw channel.
    if not interaction.channel.is_nsfw() and not all("safe" in x['tags'] for x in info['images']):
        await interaction.response.send_message("this is not an nsfw channel, you seem to be trying to bypass our filters, this has been logged.", ephemeral=True)
        await interaction.client.get_channel(report_channel).send(f"user {interaction.user.mention} attempted to bypass filters in {interaction.channel}\n tags: [{', '.join(split_tags)}]")
        # await interaction.client.get_channel(report_channel).send(embeds=all_embeds) # Used to verify in case this is false reporting people.
        return
    embeds = []
    if count > 1:
        while len(all_embeds) > 0:
            main_embed = all_embeds[0]
            for n, i in enumerate(all_embeds[:4]):
                main_embed.add_field(name=i.title, value=f"[{i.author.name or "no author tag"}]({i.url})")
                if n == 1 or n == 3:
                    main_embed.add_field(name="", value="")
                i.url = main_embed.url
                embeds.append(i)
            main_embed.title = ""
            main_embed.description = ""
            main_embed.set_author(name="")
            del all_embeds[:4]
    else:
        embeds = all_embeds
    await interaction.response.send_message(embeds=embeds)



async def setup(bot: discord.Client):
    bot.tree.add_command(_pony)

async def teardown(bot: discord.Client):
    bot.tree.remove_command(_pony)
