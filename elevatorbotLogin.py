import json
import logging
import time
from datetime import datetime

from discord.ext import commands


# Force UTC Timestamps
# From the logging cookbook: https://docs.python.org/3/howto/logging-cookbook.html
class UTCFormatter(logging.Formatter):
    converter = time.gmtime

logformat = '%(asctime)s %(levelname)s:%(module)s:%(message)s'
dateformat = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='./log/elevatorbot.log', filemode='a', level=logging.INFO, 
                    format=logformat, datefmt=dateformat
                    )
class ElevatorBotClient(commands.Bot):
    def __init__(self, *args, **kwargs):
        super(ElevatorBotClient, self).__init__(*args, **kwargs)
        self.elevatorchannelID = 465186905013616650

    async def on_ready(self):
        self.launch_time = datetime.utcnow()
        logging.info(f'Logged in as {self.user}')
        print(f'Logged in as {self.user}')  # Keep print statement for dev debugging

        elevatorchannel = self.get_channel(self.elevatorchannelID)
        self.VC = await elevatorchannel.connect()

def loadCredentials(credentialJSON):
    """
    Load login credentials from the input JSON file
    """
    with open(credentialJSON, mode='r') as fID:
        credentials = json.load(fID)

    return credentials

credentialpath = './credentials.JSON'
credentials = loadCredentials(credentialpath)
if credentials:
    client = ElevatorBotClient(command_prefix='$')
    
    # Load cogs
    client.load_extension("cogs.bot")
    client.load_extension("cogs.yt")

    # Finally, try to log in
    client.run(credentials['TOKEN'])
else:
    logging.info(f"Credential file empty: {credentialpath}")
    raise EnvironmentError
