import aiohttp
import logging
import discord

async def id_to_embed(image_id) -> (discord.Embed, bool):
    """
    takes in an id from derpibooru and converts it to an embed.
    image_id: integer id from derpibooru.
    ---
    returns a tuple following the following format: (embed, is_safe)
    """
    async with aiohttp.ClientSession() as session:
        async with session.get('http://derpibooru.org/api/v1/json/images/%d' % image_id) as resp:
            json = await resp.json()
            image = json['image']
    
    return await image_data_to_embed(image), "safe" in image['tags']

async def image_data_to_embed(image):
    embed = discord.Embed(title="#%d" % image['id'], url="https://derpibooru.org/images/%d" % image['id'])
    embed.set_image(url=image['representations']['medium'])
    embed.colour = discord.Colour.random(seed=image['id'])
    try:
        embed.description = image['description']
        if len(embed.description) > 100:
            embed.description = embed.description[:100] + "..."
    except IndexError: #no description
        pass
    try:
        embed.set_author(name=[x for x in image['tags'] if x.startswith("artist:")].pop()[7:])
    except IndexError: #no artist tag
        pass
    return embed

async def search(args):
    async with aiohttp.ClientSession() as session:
        async with session.get('http://derpibooru.org/api/v1/json/search/images', params=args) as resp:
            return await resp.json()