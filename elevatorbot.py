import logging
import re
from datetime import datetime

import discord


class ElevatorbotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(ElevatorbotClient, self).__init__(*args, **kwargs)
        self.add_command(self.ver)
        self.add_command(self.uptime)
        self.add_command(self.kill)

    async def on_ready(self):
        self.launch_time = datetime.utcnow()
        logging.info(f'Logged in as {self.user}')
        print(f'Logged in as {self.user}')  # Keep print statement for dev debugging

    @commands.command()
    async def kill(self, ctx):
        """
        Disconnect bot from Discord

        Only valid if bot owner invokes the command in a DM
        """
        if isDM(ctx.message.channel) and isOwner(ctx.message.author):
            logging.info('Bot session killed by Owner')
            await ctx.send('Shutting down... :wave:')
            await self.close()
        if isOwner(ctx.message.author) and not isDM(ctx.message.channel):
            await ctx.send(f'{ctx.message.author}, this command only works in a DM')
        else:
            logging.info(f'Unauthorized kill attempt by {ctx.message.author}')
            await ctx.send(f'{ctx.message.author}, you are not authorized to perform this operation')

def isOwner(user):
    """
    Check to see if the input User's ID matches the Owner ID
    """
    ownerID = 129606635545952258
    return user.id == ownerID

def isDM(channel):
    """
    Check to see if a channel is a DM

    A DM is either an instance of DMChannel or GroupChannel
    """
    return not isinstance(channel, discord.TextChannel)
