
FILE = open("test.txt", "r")

lines = FILE.readlines()

#print(lines[254])

for line in lines:
    
    print(line)


FILE.close()