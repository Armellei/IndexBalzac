#sorts all names in tri.txt in alphabetical order :]

with open('tri.txt', 'r') as r:
    for line in sorted(r):
        print(line, end='\r')
