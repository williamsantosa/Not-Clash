import discord
import random
import sys
import os
import math
import sqlite3
import config as cfg
from database import *
from probability import *

TOKEN = cfg.TOKEN
client = discord.Client()

# Print client to terminal
@client.event
async def on_ready():
    print("Logged in as {0}".format(client.user))

# Return for channel messages
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]

# Run the client on server/machine
if __name__ == "__main__":
    client.run(TOKEN)   