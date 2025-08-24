import os

cells = {}
cells2 = {}
cell = "⬜"
cell_ship = "⬛"
cell_hit = "🟥"
cell_miss = "🟨"


letters = ["A","B","C","D","E","F","G","H","I","J"]
letters_to_num = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":10}
numbers = [0,1,2,3,4,5,6,7,8,9]
os.system('cls')

def create_grid(side):
    global cells, cells2
    num = 1
    for row in range(1, 11):
        for col in range(1, 11):           
            if side == 0:
                cells[num] = [col, row, 0]
            elif side == 1:
                cells2[num] = [col, row, 0]
            num += 1

def grid(side):
    global cells, cells2
    print("    ", end='')
    for letter in letters:
        print(letter, end='  ')
    print()
    num = 1
    for i in cells:
        if (i-1) % 10 == 0:
            print(f"{cells[i][1]:>2} ", end='') 
        if cells[i][2] == 0:
            print(' ' + cell,end='')
        elif cells[i][2] == 1:
            print(' ' + cell_ship,end='')
        elif cells[i][2] == 2:
            print(' ' + cell_hit,end='')
        elif cells[i][2] == 3:
            print(' ' + cell_miss,end='')
        if i % 10 == 0:
            print() 

def is_adjacent_cells_clear(board, row, col, length, orientation):
    for i in range(-1, length + 1):
        for j in range(-1, 2):
            r = row + (i if orientation == 'V' else j)
            c = col + (j if orientation == 'V' else i)
            if 1 <= r <= 10 and 1 <= c <= 10:
                cell_index = (r - 1) * 10 + c
                if board[cell_index][2] != 0:
                    return False
    return True

max_amount = {1:4, 2:3, 3:2, 4:1}
plased_ships = {1:0, 2:0, 3:0, 4:0}

def ship_placement():
    while True:
        grid(0)
        length = int(input("Enter the length of the ship (1-4): "))
        if length not in [1, 2, 3, 4]:
            print("Invalid length. Please enter a number between 1 and 4.")
            continue
        if plased_ships[length] >= max_amount[length]:
            print(f"You have already placed the maximum number of ships of length {length}.")
            continue
        orientation = input("Enter orientation (H for horizontal, V for vertical): ").upper()
        if orientation not in ['H', 'V']:
            print("Invalid orientation. Please enter H or V.")
            continue
        pos = input("Enter the starting position of the ship (a1, b3, etc.): ").upper()
        col_letter = pos[0]
        row_number = int(pos[1:])
        col_num = letters_to_num.get(col_letter, 0)
        if int(pos[1]) in numbers:
            try:
                if int(pos[2]) in numbers:
                    pos_id = (int(pos[0]+pos[1])-1)*10+letters_to_num[pos[0].upper()]
            except:
                pos_id = (int(pos[1])-1)*10+letters_to_num[pos[0].capitalize()]
        if 1 > pos_id > 100:
            print("Invalid position. Please enter a valid position (a1, b3, etc.).")
            continue
        if orientation == 'H':
            if 0 >= col_num + length - 1 > 10:
                print("Ship goes out of bounds. Please try again.")
                continue
            if is_adjacent_cells_clear(cells, row_number, col_num, length, orientation) is False:
                print("Ship overlaps or is adjacent to another ship. Please try again.")
                continue
            for i in range(length):
                cell_index = pos_id + i
                cells[cell_index][2] = 1
        else:  # orientation == 'V'
            if row_number + length - 1 > 10:
                print("Ship goes out of bounds. Please try again.")
                continue
            if is_adjacent_cells_clear(cells, row_number, col_num, length, orientation) is False:
                print("Ship overlaps or is adjacent to another ship. Please try again.")
                continue
            for i in range(length):
                cell_index = pos_id + i * 10
                cells[cell_index][2] = 1
        plased_ships[length] += 1
        break

create_grid(0)
create_grid(1)
ship_placement()
grid(1)
grid(0)
print(cells)
