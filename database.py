import sqlite3

# Generate Database with discordid, elo, wins, games, primaryrole, and secondaryrole
def generateDatabase():
  '''
  roles
  0 = Fill
  1 = Top
  2 = Jungle 
  3 = Mid
  4 = Bot
  5 = Support
  '''
  connection = sqlite3.connect("Data.db")
  cursor = connection.cursor()
  cursor.execute("CREATE TABLE Data (discordid BIGINT, elo INT, wins INT, games INT, primaryrole INT, secondaryrole INT)")
  return connection

# Insert new player into Database
def insert(connection, discordid):
  cursor = connection.cursor()
  cursor.execute("INSERT INTO Data VALUES ({}, 1000, 0, 0, 0, 0)".format(discordid))
  connection.commit()

# Modify data
def modify(connection, discordid, type, value):
  cursor = connection.cursor()
  cursor.execute("UPDATE Data SET {} = {} WHERE discordid = {}".format(type, value, discordid))

# Read elo from Data
def elo(connection, discordid):
  cursor = connection.cursor()
  data = cursor.execute("SELECT elo FROM Data WHERE discordid = {}".format(discordid)).fetchall()
  return data[0][0]

# Read wins from Data
def wins(connection, discordid):
  cursor = connection.cursor()
  data = cursor.execute("SELECT wins FROM Data WHERE discordid = {}".format(discordid)).fetchall()
  return data[0][0]

# Read games from Data
def games(connection, discordid):
  cursor = connection.cursor()
  data = cursor.execute("SELECT games FROM Data WHERE discordid = {}".format(discordid)).fetchall()
  return data[0][0]

# Read primaryrole from Data
def primaryrole(connection, discordid):
  cursor = connection.cursor()
  data = cursor.execute("SELECT primaryrole FROM Data WHERE discordid = {}".format(discordid)).fetchall()
  return data[0][0]

# Read secondaryrole from Data
def secondaryrole(connection, discordid):
  cursor = connection.cursor()
  data = cursor.execute("SELECT secondaryrole FROM Data WHERE discordid = {}".format(discordid)).fetchall()
  return data[0][0]

# Check if existing entry in Data
def exists(connection, discordid):
  cursor = connection.cursor()
  found = cursor.execute("SELECT EXISTS(SELECT * FROM Data WHERE discordid = {});".format(discordid)).fetchall()
  return found[0][0] == 1