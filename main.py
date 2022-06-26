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

# Help message
async def usage(message):
    author = message.author

    msg = discord.Embed(
        colour = discord.Color.orange()
    )

    msg.set_author(name="Help")
    msg.add_field(name=".ping", value="<@259884790914875392>", inline=False)
    await message.channel.send(author, embed=msg)

# Output Teams, Legacy
async def legacyTeam(listmsg, message):
    # Obtain number of teams
    n = listmsg[1]
    if int(n) <= 1:
        client.get_channel(message.channel.id).send(f"Please input a number greater than 1. You inputted {n}.")
        return
    # Get players and sort the teams
    players = listmsg[2:]
    teams = teamSort(players, int(n))
    msg = ""
    # Print out the teams in Discord
    for team in teams:
        t = team + 1
        msg = msg + f"Team {t}\n"
        for player in teams[team]:
            msg = msg + "- " + player.capitalize() + "\n"
        msg = msg + "\n"

    # Send message in Discord
    await message.channel.send("```" + msg + "```")

# Output League Teams, Legacy
async def legacyLeague(listmsg, message):
    players = listmsg[1:]
    if(len(players) != 10):
        await message.channel.send(f"Please input 10 names. You inputted {len(players)} names.")
    teams = leagueSort(players)
    msg = ""
    t = 1
    # Compile string
    for team in teams:
        msg = msg + f"Team {t}\n"
        for player in team:
            msg = msg + "- " + player.capitalize() + " | " + team[player] + "\n"
        msg = msg + "\n"
        t = t + 1 
    
    # Send message
    await message.channel.send("```" + msg + "```")
    return

# Print client to terminal
@client.event
async def on_ready():
    print("Logged in as {0}".format(client.user))

# Return for channel messages
@client.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    lmsg = user_message.lower()

    # Print message to terminal, split message
    print(f"{username}: {user_message} ({channel})")
    listmsg = lmsg.split(" ")

    # Help command and create variable for message put lowercase
    if listmsg[0] == "!help":
        await usage(message)
        return
    
    # Any number of teams and players
    elif listmsg[0] == "!lteam":
        await legacyTeam(listmsg, message)
        return

    # Specifically for League of Legends 5v5, returns the player and the role within each team
    elif listmsg[0] == "!lleague":
        await legacyLeague(listmsg, message)
        return

# Run the client on server/machine
if __name__ == "__main__":
    client.run(TOKEN)   