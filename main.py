from hashlib import new
import discord
import config as cfg
import sqlite3
import os
import pickle
from database import *
from probability import *

TOKEN = cfg.TOKEN
client = discord.Client()

# Help message
async def usage(message):
    msg = discord.Embed(
        colour = discord.Color.orange()
    )

    msg.add_field(name="League", value="!league <@player1> <@player2> ...\n!finish <team number>\n!cancel\n!register [@player]\n!stats [@player]", inline=False)
    msg.add_field(name="Legacy", value="!lteam <number of teams> <player1> <player2> ...\n!lleague <player1> <player2> ...", inline=False)
    await message.channel.send(embed=msg)

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
        return
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

# Register player, check if duplicate
async def registerPlayer(message, conn, id):
    if exists(conn, id):
        print("Found discordid...")
        return
    register(conn, id)
    await message.channel.send(f"<@{id}> succesfully registered!")

# Print client to terminal
@client.event
async def on_ready():
    print("Logged in as {0}".format(client.user))
    if not os.path.exists("Data.db"):
        print("Generating Data.db...")
        generateDatabase()
        print("Generated Data.db.")
        return
    print("Found Data.db.")
        
# Return for channel messages
@client.event
async def on_message(message):
    conn = sqlite3.connect("Data.db")
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

    # League of Legends Ordering
    elif listmsg[0] == "!league":
        # Split into individual IDs
        ids = lmsg.split("<@")[1:]
        ids = [ids[i][:ids[i].find(">")] for i in range(len(ids))]

        # Error message
        if(len(ids) != 10):
            await message.channel.send(f"Please ping 10 players. You inputted {len(ids)} players.")
            return
        
        # Check if ID exists in Data.db, register if not
        for id in ids:
            await registerPlayer(message, conn, id)

        # Create teams and save match data
        teams = leagueSort(ids)
        with open("match.pkl", "wb") as f:
            pickle.dump(teams, f)

        str1, str2 = "", ""
        for player in teams[0]:
            str1 += f"<@{str(player)}> : {teams[0][player]}\n"
        for player in teams[1]:
            str2 += f"<@{str(player)}> : {teams[1][player]}\n"

        # Send message in Discord
        msg = discord.Embed(
            colour = discord.Color.orange()
        )

        msg.add_field(name="Team 1", value=str1, inline=False)
        msg.add_field(name="Team 2", value=str2, inline=False)

        await message.channel.send(embed=msg)
        return

    # Finish match and update teams
    elif listmsg[0] == "!finish":
        # Load Match Data
        with open("match.pkl", "rb") as f:
            mData = pickle.load(f)

        print(mData)
        
        # Calculate new team Elo
        r1, r2 = 0, 0
        winTeam = int(listmsg[1])
        for id in mData[0]:
            r1 += elo(conn, int(id))
        for id in mData[1]:
            r2 += elo(conn, int(id))
        r1, r2 = r1 / 5.0, r2 / 5.0

        newTeamElo = eloRating(r1, r2, 600, 100, winTeam)

        diff1, diff2 = newTeamElo[0] - r1, newTeamElo[1] - r2

        for id in mData[0]:
            modify(conn, id, "elo", elo(conn, id) + diff1)
            modify(conn, id, "games", games(conn, id) + 1)
            if winTeam == 0:
                modify(conn, id, "wins", wins(conn, id) + 1) 
        for id in mData[1]:
            modify(conn, id, "elo", elo(conn, id) + diff2)
            modify(conn, id, "games", games(conn, id) + 1)
            if winTeam == 1:
                modify(conn, id, "wins", wins(conn, id) + 1)
        
        await message.channel.send(f"Succesfully updated teams. Team {winTeam} won!")
        os.remove("match.pkl")
        return

    # Register new player
    elif listmsg[0] == "!register":
        if len(listmsg) == 1:
            id = message.author.id
        else:
            val = listmsg[1]
            id = int(val[val.index("<@")+2:val.index(">")])
        await registerPlayer(message, conn, id)
        return

    # Statistics for the player
    elif listmsg[0] == "!stats":
        if len(listmsg) == 1:
            id = message.author.id
        else:
            val = listmsg[1]
            id = val[val.index("<@")+2:val.index(">")]

        if not exists(conn, id):
            await message.channel.send(f"<@{id}> is not registered.")
            return

        roles = {
            0 : "Fill",
            1 : "Top",
            2 : "Jungle",
            3 : "Mid",
            4 : "Bottom", 
            5 : "Support"
        }

        msg = discord.Embed(colour = discord.Color.orange())
        
        msg.add_field(name="Player", value=f"<@{id}>", inline=False)
        msg.add_field(name="Elo", value=str(elo(conn,id)), inline=False)
        msg.add_field(name="Wins", value=str(wins(conn,id)), inline=False)
        msg.add_field(name="Games", value=str(games(conn,id)), inline=False)
        msg.add_field(name="Primary Role", value=roles[primaryrole(conn,id)],inline=False)
        msg.add_field(name="Secondary Role", value=roles[secondaryrole(conn,id)],inline=False)

        await message.channel.send(embed=msg)
        return

    # Cancels a game
    elif listmsg[0] == "!cancel":
        os.remove("match.pkl")
        await message.channel.send("Sucessfully cancelled game.")
        
# Run client on server/machine
if __name__ == "__main__":
    client.run(TOKEN)   