from random import *
from matplotlib import *

day = 1
blobs = dict()
cells = dict()

# want_cells = input("wich format do you want? like 1 is 1x1, 2 is 2x2, etc")
# want_blobs = input("How many blobs do you want? ")
# want_good = input("How many good blobs do you want? ")
# want_bad = input("How many bad blobs do you want? ")

names = ["Petya", "Vasya", "Yarik", "Elichpek", "Amir", "Sanya", "Stepan", "Noname", "Vlad", "Realyarik"]
real_names = ["Petya", "Vasya", "Yarik", "Elichpek", "Amir", "Sanya", "Stepan", "Noname", "Vlad", "Realyarik"]
class Blob:
    # 0 - good, 1 - bad
    def __init__(self):
        global names
        for i in range(1, 11):
            name = choice(names)
            color = choice(["Red", "Blue"])
            setattr(self, f"{name}", color)
            names.remove(name)

podopytniy = Blob()

for x in real_names:
    if x[len(x) - 1] in ['o','a','e','i','u']:
        print(x + "vich")
    else:
        print(x + "ovich")