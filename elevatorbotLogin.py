import json
import logging
import time

from elevatorbot import ElevatorbotClient


# Force UTC Timestamps
# From the logging cookbook: https://docs.python.org/3/howto/logging-cookbook.html
class UTCFormatter(logging.Formatter):
    converter = time.gmtime

logformat = '%(asctime)s %(levelname)s:%(module)s:%(message)s'
dateformat = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='./log/elevatorbot.log', filemode='a', level=logging.INFO, 
                    format=logformat, datefmt=dateformat
                    )

client = WumbotClient(command_prefix='&')

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
    client.run(credentials['TOKEN'])
else:
    logging.info(f"Credential file empty: {credentialpath}")
