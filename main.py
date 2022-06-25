import discord
import random
import sys
import os
import config as cfg


TOKEN = cfg.TOKEN
client = discord.Client()

### Helper Functions

# Returns a list of players on each team
# If uneven, place random player into first team, otherwise second team
def teamSort(players, n):
    '''
    players  : List containing player names
    n        : Number of teams
    '''
    # Create copy of players
    p_copy = players.copy()

    # Initialize dictionary containing all teams and players
    teams = {i:[] for i in range(n)} # team number : list of players in team

    # Sort until no leftover players
    curr = 0 # current team
    while len(p_copy) > 0:
        # Put player into team and remove from list of players
        index = random.randint(0, len(p_copy) - 1)
        teams[curr].append(p_copy.pop(index))

        # Increment, reset if needed
        curr = curr + 1 if curr < n else 0
        
    return teams

# Return a list of players in each team and their roles
# Works only if there are 10 players
def leagueSort(players):
    # Check if != 10 players
    if len(players) != 10:
        return
    
    # Initialize team 1 and team 2
    # Player : Role
    t1 = {}
    t2 = {} 

    # Create teams with their roles and place in each respective dictionary
    roles = ["Top","Jungle","Mid","Bot","Support"]
    teams = teamSort(players, 2)
    for player in teams[0]:
        t1[player] = roles.pop(random.randint(0, len(roles) - 1))
    roles = ["Top","Jungle","Mid","Bot","Support"]
    for player in teams[1]:
        t2[player] = roles.pop(random.randint(0, len(roles) - 1))
    
    return (t1, t2)

### Runtime Functions

# Print client to terminal
@client.event
async def on_ready():
    print("Logged in as {0}".format(client.user))

# Run the client on server/machine
if __name__ == "__main__":
    client.run(TOKEN)   