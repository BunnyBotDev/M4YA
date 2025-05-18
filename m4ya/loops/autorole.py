import logging
import discord
from discord.ext import commands

class AutoRole(commands.Cog):
    def __init__(self, bot: commands.Bot, guild: int, role: int):
        self.bot = bot
        self.guild_id = guild
        self.role_id = role
        self.guild = None
        self.role = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(self.guild_id)
        self.role = self.guild.get_role(self.role_id)


    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        if member.guild == self.guild:
            logging.getLogger("M4YA.autorole").debug("Adding %s to %s", self.role.name, member.name)
            await member.add_roles(self.role)

async def setup(bot: commands.Bot):
    guild_id = bot.config['autorole']['guild']
    role_id = bot.config['autorole']['role']
    await bot.add_cog(AutoRole(bot, guild_id, role_id))
    logging.getLogger("M4YA.autorole").info("Starting Autorole")

async def teardown(bot: commands.Bot):
    await bot.remove_cog("AutoRole")
    logging.getLogger("M4YA.autorole").info("Stopping Autorole.")
