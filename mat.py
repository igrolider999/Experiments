vowels = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']
consonants = ["б", "в", "г", "д", "ж", "з", "к", "л", "м", "н","п","р","с","т","ф","х","ч","ш","щ"]

word = "ваня"

def mat():
    global word
    def test1():
        global word
        if word.lower()[0] in vowels:
            word = word.lower()
            if word[0] == 'а':
                word = word[1:]
                print("Хуя" + word)
                exit()
            else:
                if word[0] == 'о':
                    word = word[1:]
                    print("Хуё" + word)
                else:
                    print("Ху" + word)
                exit()
        
    def test2():
        global word
        word = word[1:]
        if word[0] == 'у':
            print('Х' + word)
        else:
            if word[0] in consonants:
                word = word[1:]
                mat()
                    
            else:
                if word[0] == 'а':
                    word = word[1:]
                    if word[0] == 'д':
                        print("Хуя" + word)
                    else:
                        print("Хуй" + word)
                if word[0] in vowels:
                    mat()
                else:
                    mat()
    test1()
    test2()

if __name__ == '__main__':
    mat()