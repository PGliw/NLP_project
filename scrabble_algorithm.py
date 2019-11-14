import pickle
import time
import lexpy


# bullshit down below
start_time = time.time()
graph = dict()
with open('slownik_mini.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()
    for line in lines:
        if ',' in line:
            words = line.replace(' ', '').split(',')
            for word in words:
                used_letters = ''
                for letter in word:
                    pass
end_time = time.time()
print("done")
print(end_time - start_time)

class Letter:
    def __init__(self, letter, is_b):
        self.letter = letter