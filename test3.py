import random, time

cell_symbols = {
    0: '⬜',  # clear
    1: '🟨',  # miss
    2: '⬛',  # ship
    3: '🟥',  # damaged
}

def is_adjacent_cells_clear(board, row, col):
    """Check if all adjacent cells (including diagonals) are clear (0)."""
    row_idx = "abcdefghij".index(row)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr_idx = row_idx + dr
            nc = col + dc
            if 0 <= nr_idx < 10 and 1 <= nc <= 10:
                nr = "abcdefghij"[nr_idx]
                if getattr(board, f"{nr}{nc}") == 2:
                    return False
    return True

class Cell:
    def __init__(self):
        for i in range(1, 11):
            for col in "abcdefghij":
                setattr(self, f"{col}{i}", 0)

def print_board(board, title="Board", reveal_ships=True):
    print(title)
    print('   ' + ' '.join("A B C D E F G H I J".split()))
    for row_num in range(1, 11):
        print(f"{row_num:2} ", end='')
        row_symbols = []
        for col in "abcdefghij":
            val = getattr(board, f"{col}{row_num}")
            # Hide enemy ships if not hit
            if not reveal_ships and val == 2:
                val = 0
            row_symbols.append(cell_symbols.get(val, '?'))
        print(' '.join(row_symbols))

max_ships = {1: 4, 2: 3, 3: 2, 4: 1}

def place_ship(board, placed_ships):
    while True:
        try:
            ship_size = int(input("Enter ship size (1-4): "))
            if ship_size not in [1, 2, 3, 4]:
                print("Invalid size. Please enter a number between 1 and 4.")
                continue

            if placed_ships[ship_size] >= max_ships[ship_size]:
                print(f"Maximum number of ships of size {ship_size} already placed.")
                continue

            orientation = input("Enter orientation (h for horizontal, v for vertical): ").lower()
            if orientation not in ['h', 'v']:
                print("Invalid orientation. Please enter 'h' or 'v'.")
                continue

            start_cell = input("Ships are placed from left to right and from up to bottom\nEnter starting cell (e.g., a1, b5): ").lower()
            if len(start_cell) < 2 or start_cell[0] not in "abcdefghij" or not start_cell[1:].isdigit() or not (1 <= int(start_cell[1:]) <= 10):
                print("Invalid cell. Please enter a valid cell like 'a1' or 'j10'.")
                continue

            row = start_cell[0]
            col = int(start_cell[1:])

            can_place = True
            for i in range(ship_size):
                r = row
                c = col + i if orientation == 'h' else col
                r = chr(ord(row) + i) if orientation == 'v' else row
                if c > 10 or r > 'j' or getattr(board, f"{r}{c}") != 0 or not is_adjacent_cells_clear(board, r, c):
                    can_place = False
                    break

            if not can_place:
                print("Cannot place ship here. It may overlap or go out of bounds.")
                continue

            for i in range(ship_size):
                r = row
                c = col + i if orientation == 'h' else col
                r = chr(ord(row) + i) if orientation == 'v' else row
                setattr(board, f"{r}{c}", 2)

            placed_ships[ship_size] += 1
            print_board(board, "Your board")
            break

        except Exception as e:
            print(f"Error: {e}. Please try again.")

def random_place_ships(board, placed_ships):
    placed_ships.clear()
    placed_ships.update({1: 0, 2: 0, 3: 0, 4: 0})
    attempts = 0
    while sum(placed_ships.values()) < 10 and attempts < 1000:
        ship_size = random.choice([s for s in [1,2,3,4] if placed_ships[s] < max_ships[s]])
        orientation = random.choice(['h', 'v'])
        row = random.choice("abcdefghij")
        col = random.randint(1, 10)
        can_place = True
        for i in range(ship_size):
            r = row
            c = col + i if orientation == 'h' else col
            r = chr(ord(row) + i) if orientation == 'v' else row
            if c > 10 or r > 'j' or getattr(board, f"{r}{c}") != 0 or not is_adjacent_cells_clear(board, r, c):
                can_place = False
                break
        if can_place:
            for i in range(ship_size):
                r = row
                c = col + i if orientation == 'h' else col
                r = chr(ord(row) + i) if orientation == 'v' else row
                setattr(board, f"{r}{c}", 2)
            placed_ships[ship_size] += 1
        attempts += 1

def mark_diagonals_as_miss(board, row, col):
    """Mark all diagonal cells around (row, col) as miss (1) if they are empty (0)."""
    row_idx = "abcdefghij".index(row)
    diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    for dr, dc in diagonals:
        nr_idx = row_idx + dr
        nc = col + dc
        if 0 <= nr_idx < 10 and 1 <= nc <= 10:
            nr = "abcdefghij"[nr_idx]
            cell = f"{nr}{nc}"
            if getattr(board, cell) == 0:
                setattr(board, cell, 1)

def mark_around_ship_as_miss(board, ship_cells):
    """Mark all cells around the destroyed ship as miss (1), except for ships and destroyed ships."""
    for row, col in ship_cells:
        row_idx = "abcdefghij".index(row)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr_idx = row_idx + dr
                nc = col + dc
                if 0 <= nr_idx < 10 and 1 <= nc <= 10:
                    nr = "abcdefghij"[nr_idx]
                    cell = f"{nr}{nc}"
                    val = getattr(board, cell)
                    if val == 0:
                        setattr(board, cell, 1)

def is_ship_destroyed(board, row, col):
    """Check if the ship at (row, col) is fully destroyed. Return ship cells if destroyed, else False."""
    if getattr(board, f"{row}{col}") != 3:
        return False

    # Check horizontally
    ship_cells = []
    # Left
    c = col
    while c >= 1 and getattr(board, f"{row}{c}") in [2, 3]:
        ship_cells.append((row, c))
        c -= 1
    # Right
    c = col + 1
    while c <= 10 and getattr(board, f"{row}{c}") in [2, 3]:
        ship_cells.append((row, c))
        c += 1

    if len(ship_cells) == 1:
        # Check vertically if it's not a horizontal ship
        ship_cells = []
        # Up
        r_idx = "abcdefghij".index(row)
        while r_idx >= 0 and getattr(board, f"{'abcdefghij'[r_idx]}{col}") in [2, 3]:
            ship_cells.append(('abcdefghij'[r_idx], col))
            r_idx -= 1
        # Down
        r_idx = "abcdefghij".index(row) + 1
        while r_idx < 10 and getattr(board, f"{'abcdefghij'[r_idx]}{col}") in [2, 3]:
            ship_cells.append(('abcdefghij'[r_idx], col))
            r_idx += 1

    for r, c in ship_cells:
        if getattr(board, f"{r}{c}") != 3:
            return False
    return ship_cells

def destroy_ship(board, cell):
    if len(cell) < 2 or cell[0] not in "abcdefghij" or not cell[1:].isdigit() or not (1 <= int(cell[1:]) <= 10):
        print("Invalid cell. Please enter a valid cell like 'a1' or 'j10'.")
        destroy_ship(board, input("Enter a valid cell to destroy: "))

    row = cell[0]
    col = int(cell[1:])

    current_value = getattr(board, f"{row}{col}")
    if current_value == 0:
        setattr(board, f"{row}{col}", 1)  # Miss
        print("Miss!")
        return False
    elif current_value == 2:
        setattr(board, f"{row}{col}", 3)  # Hit
        print("Hit!")
        mark_diagonals_as_miss(board, row, col)
        ship_cells = is_ship_destroyed(board, row, col)
        if ship_cells:
            print("You destroyed an entire ship!")
            mark_around_ship_as_miss(board, ship_cells)
        print_board(board, "Enemy board (your shots)", reveal_ships=False)
        return True
    elif current_value in [1, 3]:
        print("Already targeted this cell.")
        return False
    else:
        print("Unknown cell state.")
        return False
    
def enemy_turn(board):
    if not hasattr(enemy_turn, "targets"):
        enemy_turn.targets = []
    tried = set()
    while True:
        # If there are targets (damaged ship cells), try their adjacents
        if enemy_turn.targets:
            # Get all adjacents of all hit cells, shuffle for randomness
            adjacents = []
            for row, col in enemy_turn.targets:
                row_idx = "abcdefghij".index(row)
                for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                    nr_idx = row_idx + dr
                    nc = col + dc
                    if 0 <= nr_idx < 10 and 1 <= nc <= 10:
                        nr = "abcdefghij"[nr_idx]
                        cell = f"{nr}{nc}"
                        if cell not in tried and getattr(board, cell) in [0,2]:
                            adjacents.append((nr, nc))
            random.shuffle(adjacents)
            if adjacents:
                nr, nc = adjacents[0]
            else:
                # No adjacents left, reset targets (shouldn't happen unless bug)
                enemy_turn.targets = []
                continue
        else:
            # Pick random cell
            while True:
                nr = random.choice("abcdefghij")
                nc = random.randint(1, 10)
                cell = f"{nr}{nc}"
                if cell not in tried and getattr(board, cell) in [0,2]:
                    break

        cell = f"{nr}{nc}"
        tried.add(cell)
        print(f"Enemy attacks {cell}!")
        current_value = getattr(board, cell)
        if current_value == 0:
            setattr(board, cell, 1)
            print("Enemy missed!")
            return  # Always end enemy turn on miss
        elif current_value == 2:
            setattr(board, cell, 3)
            print("Enemy hit your ship!")
            mark_diagonals_as_miss(board, nr, nc)
            print_board(board, "Your board")  # Show board after hit
            time.sleep(1)  # Wait 1 second before next attack
            enemy_turn.targets.append((nr, nc))
            ship_cells = is_ship_destroyed(board, nr, nc)
            if ship_cells:
                print("Enemy destroyed your ship!")
                mark_around_ship_as_miss(board, ship_cells)
                enemy_turn.targets = []  # Ship destroyed, reset hunt
                if all_ships_destroyed(board):
                    return
                print("Enemy gets another attack after destroying your ship!")
                time.sleep(1)
                continue  # Continue enemy turn for one more attack
            # Otherwise, continue to hunt this ship
        # If already targeted, just continue loop

# Initialize attribute for first run
enemy_turn.targets = []

def all_ships_destroyed(board):
    labels = [f"{row}{col}" for row in "abcdefghij" for col in range(1, 11)]
    for label in labels:
        if getattr(board, label) == 2:
            return False
    return True

# --- Game Setup ---

my_board = Cell()
enemy_board = Cell()
my_ships = {1: 0, 2: 0, 3: 0, 4: 0}
enemy_ships = {1: 0, 2: 0, 3: 0, 4: 0}

print_board(my_board, "Your board")

choice = input("Type 'r' to randomize your ship placement or any other key to place manually: ").lower()
if choice == 'r':
    random_place_ships(my_board, my_ships)
    print_board(my_board, "Your board")
else:
    while sum(my_ships.values()) < 10:
        place_ship(my_board, my_ships)

print("Now placing enemy ships...")
random_place_ships(enemy_board, enemy_ships)

print("All ships placed!\nNow for the game itself!")

def print_boards_side_by_side(board1, board2, title1="Your board", title2="Enemy board", reveal_ships1=True, reveal_ships2=False):
    header = '   ' + ' '.join("a b c d e f g h i j".split())
    print(f"{title1:<25}    {title2}")
    print(f"{header}    {header}")
    for row_num in range(1, 11):
        row_symbols1 = []
        row_symbols2 = []
        for col in "abcdefghij":
            val1 = getattr(board1, f"{col}{row_num}")
            val2 = getattr(board2, f"{col}{row_num}")
            if not reveal_ships1 and val1 == 2:
                val1 = 0
            if not reveal_ships2 and val2 == 2:
                val2 = 0
            row_symbols1.append(cell_symbols.get(val1, '?'))
            row_symbols2.append(cell_symbols.get(val2, '?'))
        print(f"{row_num:2} {' '.join(row_symbols1)}    {row_num:2} {' '.join(row_symbols2)}")

# --- Game Loop ---
def game_loop():
    while True:
        print_boards_side_by_side(my_board, enemy_board, "Your board", "Enemy board (your shots)", reveal_ships1=True, reveal_ships2=False)
        player_turn = True
        while player_turn:
            target = input("Enter cell to attack (e.g., a1, b5): ").lower()
            hit = destroy_ship(enemy_board, target)
            if all_ships_destroyed(enemy_board):
                print("All enemy ships destroyed! You win!")
                break
            if hit:
                print("You hit! Shoot again.")
                continue
            else:
                player_turn = False
        enemy_turn(my_board)
        if all_ships_destroyed(my_board):
            print("All your ships destroyed! Enemy wins!")
            break

while True:
    game_loop()
    play_again = input("Play again? (y/n): ").lower()
    if play_again != 'y':
        break
        