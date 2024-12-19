from ucimlrepo import fetch_ucirepo
import pandas as pd
import time

start_time = time.time()
# fetch dataset 
#connect_4 = fetch_ucirepo(id=26) 
  
# data (as pandas dataframes) 
#x = connect_4.data.features 
#y = connect_4.data.targets 

data = pd.read_csv("connect-4.data")

# expects line to be a 42 long array with 'b's (blanks), 'x's (first player, computer) and 'o's (second player, user)
def visualizeLine(line, title = ""):
    print(title)
    for i in range(6, 0, -1):
        nextline = str(i)
        for j in range(7):
            nextchar = line[j*6 + i-1]
            if nextchar == 'b':
                nextchar = '.'
            nextline += ' ' + nextchar
        print(nextline)
    print("  " + " ".join(str(chr(i+97)) for i in range(7)))

# expects line to be a 42 long array with 'b's (blanks), 'x's (first player, computer) and 'o's (second player, user)
# find all positions that are 1 move away in the database
def findConnectedPositions(line):
    # find all valid positions to put a x or o
    # valid positions are all blank on row 1, or any blank above an x or o that is on row 1-5
    connectedPositions = []
    # first find all valid positions to put a x or o
    validIndices = []
    for i in range(7):
        if line[i*6] == 'b':
            validIndices.append(i*6)
        for j in range(1,6):
            if line[j + i*6] == 'b':
                if line[j-1 + i*6] != 'b':
                    validIndices.append(j + i*6)
                break
    
    # count how many x's and o's
    countx = line.count('x')
    counto = line.count('o')
    
    # TEMP uncomment if you want to see valid positions
    #for index in validIndices:
    #    line[index] = '#'
    #visualizeLine(line,  "Valid Highlighted")
    #print("num x: " + str(countx))
    #print("num o: " + str(counto))
    
    # if they are equal, it is x's turn, otherwise there is 1 more x, and it is o's turn
    if countx == counto:
        # look for position + x
        for index in validIndices:
            checkLine = line.copy()
            checkLine[index] = 'x'
            # find line in data that match checkLine
            csvL = ""
            for i in checkLine:
                csvL += i + ","
            csvL = csvL[:-1]
            visualizeLine(checkLine, csvL)
            
        pass
    elif countx > counto:
        # look for position + o
        pass
    else:
        print("ERROR: Invalid position.")
        print("num x: " + str(countx))
        print("num o: " + str(counto))
        system.exit(1)
    print(connectedPositions)


#l = data.loc[100].to_list()
#visualizeLine(l, "Base")
#findConnectedPositions(l)

# THERE IS NOT A SINGLE INDEX WHERE IT IS o's TURN, IT IS ALWAYS x's
for i in range(0, len(data)):
    l = data.loc[i].to_list()
    xc = l.count('x')
    oc = l.count('o')
    if (xc>oc):
        print(i)

# TODO: find the closest win, and get there
# have to also notice how close the computer is to a win
# if the computer wins a tree, then it has -100 value
# maybe assign a value to every position, so all the program has to do is pick the neighboring move with the highest value

end_time = time.time()
runtime = end_time - start_time
print("Runtime:", runtime, "seconds")