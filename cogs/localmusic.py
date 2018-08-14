import asyncio
import logging
import random
from pathlib import Path

import discord
from discord.ext import commands


class LocalMusic():
    def __init__(self, bot):
        self.bot = bot
        self.musicpath = Path('./music')

    async def on_ready(self):
        elevatorchannel = self.bot.get_channel(self.bot.elevatorchannelID)
        self.VC = await elevatorchannel.connect()
        self._VCchannel = self.VC.channel

        self.player = discord.FFmpegPCMAudio(self.getrandommusic())
        # Only start player if other users are in the voice channel
        if len(self._VCchannel.members) > 1:
            self.play()

        # TODO: Generate embed loop
        # TODO: Restart music when done

    def play(self):
        if not self.VC.is_playing():
            if not self.VC.is_paused():
                self.VC.play(self.player)
            else:
                self.VC.resume()

    async def on_voice_state_update(self, member, before, after):
        if member == self.bot.user:
            # Ignore bot events
            return
        
        if before.channel != self._VCchannel and after.channel == self._VCchannel:
            # User joined channel, start/resume music
            # LocalMusic.start() makes the paused vs. not playing check
            self.play()
        elif before.channel == self._VCchannel and after.channel != self._VCchannel:
            # User left channel, pause if they were the last one
            if len(self._VCchannel.members) <= 1:
                self.VC.pause()

    def getrandommusic(self):
        flist = list(self.musicpath.glob('./*.m4a'))
        
        return random.choice(flist)

def setup(bot):
    bot.add_cog(LocalMusic(bot))