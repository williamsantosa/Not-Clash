import math
import random

# Returns the probability of r1 winning
def prob(r1, r2, D):
  return 1.0 / (1.0 + math.pow(10.0, (r2 - r1) / D))

# Updates the Elo rating from results of the game
def eloRating(r1, r2, D, K, w):
  '''
  r1          : Rating of player/team 1
  r2          : Rating of player/team 2
  D           : Effect of difference on probability to win or lose (higher = less effect)
  K           : Maximum value a player's rating can change
  w           : 1 or 2, player/team 1 wins or player/team 2 wins
  returnValue : (newr1, newr2)
  '''
  p1, p2 = prob(r1, r2, D), prob(r2, r1, D)
  rv1 = float(r1) + float(K) * (w - p1)
  rv2 = float(r2) + float(K) * (w - p2)
  return (int(rv1), int(rv2))

# Returns the confidence level that a player is in their Elo
def pConfidence(n):
    '''
    n           : Number of games played
    returnValue : Confidence percent
    '''
    return 1.0 - math.pow(math.exp(1), -0.1 * n)

# Returns teams with players
def teamSort(players, n):
    '''
    players     : List containing player names
    n           : Number of teams
    returnValue : {team# : [playerName]}
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

# Returns teams with players and their roles
def leagueSort(players):
    '''
    prereq      : len(players) == 10
    players     : List containing player names
    returnValue : ({playerName : role}, {playerName : role})
    '''
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