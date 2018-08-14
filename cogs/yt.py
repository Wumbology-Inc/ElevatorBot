import logging

import discord
from discord.ext import commands


class YoutubeCommands():
    def __init__(self, bot):
        self.bot = bot
        self.defURL = "https://www.youtube.com/watch?v=S5PvBzDlZGs"

    @commands.command()
    async def play(self, ctx: commands.Context):
        raise NotImplementedError


def setup(bot):
    bot.add_cog(YoutubeCommands(bot))
