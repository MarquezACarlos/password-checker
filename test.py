import time

word = "cloud"
curr = time.time()

with open('lists/words.txt') as f:
    if word in f.read():
        print("true")
        end = time.time()

print(end - curr)
