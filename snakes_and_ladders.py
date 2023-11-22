
import random
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class GameBoard:
    def __init__(self, size):
        self.size = size
        self.snakes = {}
        self.ladders = {}

    def add_snake(self, start, end):
        self.snakes[start] = end

    def add_ladder(self, start, end):
        self.ladders[start] = end

class Player:
    def __init__(self, name, board_size):
        self.name = name
        self.position = 0
        self.board_size = board_size

    def move(self, steps):
        new_position = self.position + steps
        if new_position <= self.board_size * self.board_size:  
            self.position = new_position

class Game:
    def __init__(self, board, players):
        self.board = board
        self.players = players
        self.current_player = 0
        self.move_log = []
        self.winner = None

    def roll_dice(self):
        return random.randint(1, 6)

    def play_turn(self):
        if self.winner is not None:
            return  # Game has ended

        player = self.players[self.current_player]
        roll = self.roll_dice()
        player.move(roll)
        self.check_snake_or_ladder(player)
        self.move_log.append((player.name, player.position))

        self.log_move_to_file(player.name, roll, player.position)

        # Check for winner
        if player.position == self.board.size * self.board.size:
            self.winner = player.name
            print(f"Player {player.name} wins the game by reaching {self.board.size * self.board.size}!")
            return

        self.current_player = (self.current_player + 1) % len(self.players)

    def log_move_to_file(self, player_name, roll, new_position, filename="game_moves.txt"):
        with open(filename, "a") as file:
            file.write(f"Player {player_name} rolled a {roll} and moved to position {new_position}\n")

    def dump_game_history(self, filename="game_history.txt"):
        with open(filename, "w") as file:
            for player_name, position in self.move_log:
                file.write(f"Player {player_name} moved to position {position}\n")

    def check_snake_or_ladder(self, player):
        position = player.position
        if position in self.board.snakes:
            player.position = self.board.snakes[position]
        elif position in self.board.ladders:
            player.position = self.board.ladders[position]

    def save_game(self, filename):
        with open(filename, 'w') as file:
            game_state = {
                "board_size": self.board.size,
                "snakes": self.board.snakes,
                "ladders": self.board.ladders,
                "players": {player.name: player.position for player in self.players},
                "current_player": self.current_player,
                "move_log": self.move_log
            }
            json.dump(game_state, file)

    def load_game(self, filename):
        with open(filename, 'r') as file:
            game_state = json.load(file)
            self.board = GameBoard(game_state["board_size"])
            self.board.snakes = game_state["snakes"]
            self.board.ladders = game_state["ladders"]
            self.players = [Player(name) for name in game_state["players"]]
            for player in self.players:
                player.position = game_state["players"][player.name]
            self.current_player = game_state["current_player"]
            self.move_log = game_state["move_log"]

    def plot_board(self):
        # Define colors for the players
        player_colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown']
        
        # Create a figure and axis for the plot
        fig, ax = plt.subplots(figsize=(10, 10))

        # Draw the grid manually based on board size
        for x in range(self.board.size):
            for y in range(self.board.size):
                ax.add_patch(plt.Rectangle((x, y), 1, 1, fill=None, alpha=1, edgecolor='black'))

        # Function to convert board position to x, y coordinates for a dynamic board size
        def position_to_coordinates(pos):
            x = (pos - 1) % self.board.size
            y = self.board.size - 1 - (pos - 1) // self.board.size
            if y % 2 == 1:  # Adjust for zigzag pattern
                x = self.board.size - 1 - x
            return x, y

        # Plotting snakes and ladders with lines
        for start, end in self.board.snakes.items():
            start_x, start_y = position_to_coordinates(start)
            end_x, end_y = position_to_coordinates(end)
            ax.plot([start_x + 0.5, end_x + 0.5], [start_y + 0.5, end_y + 0.5],
                    color='red', linewidth=5, marker='o', markersize=10, markerfacecolor='red')

        for start, end in self.board.ladders.items():
            start_x, start_y = position_to_coordinates(start)
            end_x, end_y = position_to_coordinates(end)
            ax.plot([start_x + 0.5, end_x + 0.5], [start_y + 0.5, end_y + 0.5],
                    color='green', linewidth=5, marker='o', markersize=10, markerfacecolor='green')

        # Plotting the path for each player
        for index, player in enumerate(self.players):
            player_positions = [move[1] for move in self.move_log if move[0] == player.name]
            path_x, path_y = [], []
            for pos in player_positions:
                x, y = position_to_coordinates(pos)
                path_x.append(x + 0.5)
                path_y.append(y + 0.5)
                # If a snake or ladder was encountered, draw a line to the start and another line from the end
                if pos in self.board.snakes or pos in self.board.ladders:
                    snake_ladder_end = self.board.snakes.get(pos, self.board.ladders.get(pos))
                    end_x, end_y = position_to_coordinates(snake_ladder_end)
                    ax.plot([x + 0.5, end_x + 0.5], [y + 0.5, end_y + 0.5], 
                            color=player_colors[index % len(player_colors)], linewidth=2, linestyle='--')
            # Draw continuous line for player's path
            ax.plot(path_x, path_y, marker='o', markersize=5, linewidth=2, color=player_colors[index % len(player_colors)])

        # Numbering the squares
        for pos in range(1, self.board.size * self.board.size + 1):
            x, y = position_to_coordinates(pos)
            ax.text(x + 0.5, y + 0.5, str(pos), horizontalalignment='center', verticalalignment='center')

        # Set the limits and aspect of the plot to ensure squares are actually square-shaped
        ax.set_xlim(0, self.board.size)
        ax.set_ylim(0, self.board.size)
        ax.set_aspect('equal')

        plt.title('Snakes and Ladders Board')
        plt.show()
    def plot_moves(self):
        plt.figure(figsize=(10, 5))
        for player in self.players:
            player_moves = [move[1] for move in self.move_log if move[0] == player.name]
            plt.plot(player_moves, label=player.name)
        plt.xlabel('Turn')
        plt.ylabel('Position')
        plt.title('Player Moves')
        plt.legend()
        plt.show()
        
    def plot_landing_frequency(self):
        landing_counts = np.zeros((self.board.size, self.board.size))

        # Function to convert position to board coordinates
        def position_to_coordinates(pos):
            x = (pos - 1) % self.board.size
            y = self.board.size - 1 - (pos - 1) // self.board.size
            if y % 2 == 1:  # Adjust for zigzag pattern
                x = self.board.size - 1 - x
            return x, y

        # Count landings
        for _, pos in self.move_log:
            x, y = position_to_coordinates(pos)
            landing_counts[y, x] += 1

        # Create heatmap
        plt.figure(figsize=(10, 10))
        sns.heatmap(landing_counts, annot=True, fmt=".0f", cmap="YlGnBu", cbar=False)

        # Adding title and labels
        plt.title('Frequency of Landing on Each Square')
        plt.xlabel('Column')
        plt.ylabel('Row')
        plt.show()

def main():
    # Ask if the user wants to start a new game or resume a saved game
    choice = input("Do you want to start a new game or resume a saved game? (new/resume): ").lower()

    if choice == 'resume':
        try:
            filename = input("Enter the filename of the saved game: ")
            with open(filename, 'r') as file:
                game_state = json.load(file)
                size = game_state["board_size"]
                board = GameBoard(size)
                board.snakes = game_state["snakes"]
                board.ladders = game_state["ladders"]
                players = [Player(name, size) for name in game_state["players"]]
                for player in players:
                    player.position = game_state["players"][player.name]
                game = Game(board, players)
                game.current_player = game_state["current_player"]
                game.move_log = game_state["move_log"]
                print(f"Resumed game. It's {players[game.current_player].name}'s turn.")
        except Exception as e:
            print(f"Failed to resume game: {e}")
            return
    else:
        while True:
            try:
                size = int(input("Enter the size of the game board (e.g., 10 for a 10x10 board): "))
                if size <= 0:
                    raise ValueError("The size must be a positive integer.")
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a positive integer.")

        board = GameBoard(size)

        # Function to safely get integer input
        def get_int_input(prompt, min_value=None, max_value=None):
            while True:
                try:
                    value = int(input(prompt))
                    if (min_value is not None and value < min_value) or (max_value is not None and value > max_value):
                        raise ValueError(f"Value must be between {min_value} and {max_value}.")
                    return value
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter a valid integer.")

        # Add snakes
        num_snakes = get_int_input("Enter the number of snakes: ", 0)
        for _ in range(num_snakes):
            while True:
                try:
                    start, end = map(int, input("Enter the start and end points of a snake (e.g., '16,6'): ").split(','))
                    if start <= end or start > size*size or end < 1:
                        raise ValueError("Invalid snake position.")
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter valid start and end points.")

            board.add_snake(start, end)

        # Add ladders
        num_ladders = get_int_input("Enter the number of ladders: ", 0)
        for _ in range(num_ladders):
            while True:
                try:
                    start, end = map(int, input("Enter the start and end points of a ladder (e.g., '9,31'): ").split(','))
                    if start >= end or start < 1 or end > size*size:
                        raise ValueError("Invalid ladder position.")
                    break
                except ValueError as e:
                    print(f"Invalid input: {e}. Please enter valid start and end points.")

            board.add_ladder(start, end)

        # Add players
        num_players = get_int_input("Enter the number of players (2-4): ", 2, 4)
        players = [Player(input(f"Enter name of player {i+1}: "), size) for i in range(num_players)]
        game = Game(board, players)

    # Main gameplay loop
    while game.winner is None:
        print(f"\n{game.players[game.current_player].name}'s turn.")
        input("Press enter to roll the dice.")
        game.play_turn()
        print(f"Rolled a {game.players[game.current_player-1].position % 6 + 1}. "
              f"Moved to position {game.players[game.current_player-1].position}.")

        # Save option
        if input("Do you want to save the game? (y/n): ").lower() == 'y':
            game.save_game("game_state.json")
            print("Game saved.")

    # End of game handling
    if game.winner:
        game.save_game("game_state.json")
        game.dump_game_history()
        print(f"Game over! {game.winner} wins!")

    # Plotting results
    game.plot_board()
    game.plot_moves()
    game.plot_landing_frequency()

if __name__ == "__main__":
    main()
