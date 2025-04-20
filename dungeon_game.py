#dungeon_game.py
from classes.game import Person
from classes.magic import Spell
from classes.inventory import Item
import random
import os
from battle import start_battle, players, enemies


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Create the dungeon grid (5x5)
dungeon = [(x, y) for y in range(5) for x in range(5)]

# Randomly assign monster, door, and player positions
def random_items():
    return random.sample(dungeon, 3)

# Display the dungeon map with player position
def make_dungeon(player_position):
    print("\nDungeon Map:\n")
    for y in range(5):
        row = ""
        for x in range(5):
            if (x, y) == player_position:
                row += "|P"
            else:
                row += "|_"
        row += "|"
        print(row)
    print("")  # Add space after map

# Determine valid moves based on current location
def get_moves(position):
    x, y = position
    moves = []
    if x > 0:
        moves.append("LEFT")
    if x < 4:
        moves.append("RIGHT")
    if y > 0:
        moves.append("UP")
    if y < 4:
        moves.append("DOWN")
    return moves

# Move the player based on input direction
def move_player(position, move):
    x, y = position
    if move == "LEFT":
        return (x - 1, y)
    elif move == "RIGHT":
        return (x + 1, y)
    elif move == "UP":
        return (x, y - 1)
    elif move == "DOWN":
        return (x, y + 1)
    return position

# Main game function
def game_loop():
    monster, door, player = random_items()

    while True:
        clear_screen()
        make_dungeon(player)
        print(f"Your party is currently in room {player}.")
        moves = get_moves(player)
        print(f"You can move: {', '.join(moves)}")
        print("Enter 'QUIT' to exit the game.")

        move = input("Move > ").upper()

        if move == "QUIT":
            print("Thanks for playing!")
            break
        elif move in moves:
            player = move_player(player, move)
            if player == monster:
                clear_screen()
                print("👹 You’ve encountered the enemy room! Prepare for battle!\n")
                
                battle_result = start_battle(players, enemies)  # <- function you define that runs the battle logic
                
                if battle_result == "win":
                    print("🎉 You defeated the enemy!")
                    monster = (-1, -1)  # Remove monster from map
                    input("Press Enter to continue...")
                else:
                    print("💀 The enemy defeated you... GAME OVER.")
                    break
            elif player == door:
                clear_screen()
                print("🎉 You found the door and escaped! YOU WIN!")
                break
        else:
            print("⚠️ Invalid move. Try again.")
            input("Press Enter to continue...")

if __name__ == "__main__":
    game_loop()
