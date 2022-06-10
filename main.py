import discord
import random
import config as cfg

TOKEN = cfg.TOKEN
client = discord.Client()

# Print client to terminal
@client.event
async def on_ready():
    print("Logged in as {0}".format(client.user))

