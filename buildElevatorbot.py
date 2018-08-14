import logging
import os
import time

import docker


# Force UTC Timestamps
# From the logging cookbook: https://docs.python.org/3/howto/logging-cookbook.html
class UTCFormatter(logging.Formatter):
    converter = time.gmtime

logformat = '%(asctime)s %(levelname)s:%(module)s:%(message)s'
dateformat = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(filename='./log/elevatorbotdocker.log', filemode='a', level=logging.INFO, 
                    format=logformat, datefmt=dateformat
                    )

client = docker.from_env()
APIClient = docker.APIClient()

# Find & kill any existing containers that haven't been stopped/cleaned up
dockername = 'elevatorbot'
containerfilter = {'name':dockername}
elevatorbotcontainers = APIClient.containers(filters=containerfilter)
logging.info(f"Found {len(elevatorbotcontainers)} running {dockername} containers")
for container in elevatorbotcontainers:
    APIClient.stop(container['Id'])
else:
    logging.info(f"Stopped {len(elevatorbotcontainers)} {dockername} containers")

# Build the new image
logging.info(f"Building new {dockername} image...")
img, buildlog = client.images.build(path='.', tag=dockername, rm=True)
[logging.debug(line) for line in buildlog]
logging.info(f"{dockername} image build complete")

# Restart the bot container
logging.info(f"Restarting {dockername}...")
vol = {f'{os.getcwd()}/log': {'bind': '/app/log', 'mode': 'rw'}}
client.containers.run(img.id, auto_remove=True, detach=True, name=dockername, volumes=vol)
