import os
os.system('cls')
letters = {"A":1,"B":2,"C":3,"D":4,"E":5,"F":6,"G":7,"H":8,"I":9,"J":10}
numbers = [0,1,2,3,4,5,6,7,8,9]

cells = {}
shifrator = {}
num = 1
num2 = 1

def convert(a):
    if int(a[1]) in numbers:
        try:
            if int(a[2]) in numbers:
                print(str((int(a[1]+a[2])-1)*10+letters[a[0].capitalize()]))
        except:
            print(str((int(a[1])-1)*10+letters[a[0].capitalize()]))

    
