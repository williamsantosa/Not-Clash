# Not Clash

Not Clash is a tool based off the original League of Legends event called "Clash" where teams of 5 players face off against one another in a bracket style tournament to see who is the winner. Thus, "Not Clash" borrows that idea and converts its functionality to fit the purpose of a smaller friend group rather than many teams. 10 players are randomly sorted into 2 teams and battle against one another. The winners gain Elo and the losers lose Elo. Their statistics are saved in a database that utilizes SQL commands executed by the sqlite3 Python3 library. Match data is saved as a pickle object and commands are utilized in Discord to help with the logistics of the game.

## Setup

1. Install [Python3](https://www.python.org/downloads/) v3.5.3+.
2. Install [discord.py](https://pypi.org/project/discord.py/).
3. Set up [Discord Bot](https://discordpy.readthedocs.io/en/stable/discord.html) and insert credentials.
4. Install pickle if Python3 is less than v3.8.
5. Rename `configtemplate.py` to `config.py` and change variables.

## Usage

**Starting the Program**
1. Enter directory of `main.py`.
2. Execute `python3 ./main.py &`.

**Stopping the Program**
1. Execute `ps aux | grep python`.
2. Kill `pid` located on the left side of the display

## Commands

**League**

Commands for Not Clash tournaments.

`league <@player1> <@player2> ... <@player10>`
> Starts a new game and randomly allocates the pinged players into two teams. Displays the match in Discord.

`finish <team number>`
> Finishes the game and updates statistics of the players. Team number is either `1` or `2`, representing the winning team.

`cancel`
> Cancels the current game if there is one.

`swap <@player1> <@player2>`
> Swaps the two players if they are on the same team.

`display`
> Displays the current game if there is one.

`register [@player]`
> Registers the player or the pinged player if provided.

`primary <role>`
> Sets the primary role to be either Fill, Top, Jungle, Mid, Bot, or Support.

`secondary <role>`
> Sets the secondary role to be either Fill, Top, Jungle, Mid, Bot, or Support.

`stats [@player]`
> Displays the player's statistics or the pinged player's statistics if provided.

**Legacy**

Legacy commands from the Clash Helper that was the predecessor for the Not Clash bot.

`lteam <n teams> <player1> <player2> ... <player10>`
> Creates `n` teams and equally distributes players among the teams.

`lleague <player1> <player2> ... <player10>`
> Creates 2 teams and equally distributes players among the teams with their roles.