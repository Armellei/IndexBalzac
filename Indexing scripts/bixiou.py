#sorts all names in tri.txt in alphabetical order :]

tri = open('tri.txt')
with open('tri.txt', 'r') as r:
    for line in sorted(r):
        print(line, end='\r')
tri.close()