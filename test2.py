import os

cells = {}
cells2 = {}
cell = "⬜"
cell_ship = "⬛"
cell_hit = "🟥"
cell_miss = "🟨"


letters = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":10}
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

def convert(a):
    if int(a[1]) in numbers:
        try:
            if int(a[2]) in numbers:
                return str((int(a[1]+a[2])-1)*10+letters[a[0].capitalize()])
        except:
            return str((int(a[1])-1)*10+letters[a[0].capitalize()])

create_grid(0)
create_grid(1)
while True:
    a = convert(input())
    print(a)
    cells[int(a)][2] = 3
    grid(0)

# print(cells)
