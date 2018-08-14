import asyncio
import logging
from pathlib import Path

import discord
from discord.ext import commands


class LocalMusic():
    def __init__(self, bot):
        self.bot = bot
        self.musicpath = Path('./music/elevator1.m4a')

    async def on_ready(self):
        elevatorchannel = self.bot.get_channel(self.bot.elevatorchannelID)
        self.VC = await elevatorchannel.connect()

        player = discord.FFmpegPCMAudio(self.musicpath)
        self.VC.play(player)

    @commands.command()
    async def play(self, ctx: commands.Context):
        player = self.bot.VC.create
        raise NotImplementedError

def setup(bot):
    bot.add_cog(LocalMusic(bot))