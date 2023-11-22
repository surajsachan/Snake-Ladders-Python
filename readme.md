# Snakes and Ladders Game

## Description
This is an implementation of the classic board game "Snakes and Ladders" in Python. The game is designed for 2-4 players and features a customizable board size. Players take turns rolling a dice to move their piece across the board, encountering ladders that advance their progress and snakes that set them back.

## Requirements
- Python 3.x
- Libraries: matplotlib, seaborn, pandas, numpy

## Installation
To set up the game environment, ensure that Python 3 is installed on your system. Then, install the required libraries using pip:

## Running the Game
To start the game, run the Python script from your terminal:

## Features
- Customizable board size
- Dynamic addition of snakes and ladders
- Multiplayer support (2-4 players)
- Graphical representation of the board, player moves, and frequency of landing on each square
- Option to save and resume games

## Game Play
1. Start a new game or resume a saved game.
2. If starting a new game, specify the board size and the number and positions of snakes and ladders.
3. Enter the number of players and their names.
4. Players take turns rolling the dice and moving their pieces on the board.
5. The game records each move and provides visual feedback through plots.
6. The first player to reach the last square wins the game.

## Saving and Resuming Games
- At any point during the game, players can choose to save the current state.
- Saved games are stored in a JSON file.
- Players can resume a saved game by selecting the 'resume' option at the start and providing the filename of the saved game state.

## Author
Suraj Sachan