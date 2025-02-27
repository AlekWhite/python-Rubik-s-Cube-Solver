import random
import time
import tkinter as tk
from threading import Thread


# http://ozcubegirl.com/rubikscubesolution.html

# raw input data (may need to be rotated )
raw = [[0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1],[2,2,2,2,2,2,2,2,2,],[3,3,3,3,3,3,3,3,3],[4,4,4,4,4,4,4,4,4],[5,5,5,5,5,5,5,5,5]]


"""
Main todo:

Step 1:
white cross

    find multi move possibilities
    refactor to allow non concrete moves to be entered 


Step 2:
white corners

    everything


Step 3:
patterns

    everything 
"""


""" -------------- GUI -------------- """

# colors - green-0  white-1  blue-2   yellow-3   red-4   orange-5
colors = ["#00cc00","#ffffff","#0099ff","#ffff00","#ff0000","#fc8403"]

# tk junk
def GUIthread(name):

    global root, canvas
    root = tk.Tk()
    root.geometry('700x500')
    canvas = tk.Canvas(root, height=500, width=700, bg="#262626")
    canvas.pack()
    root.resizable(False, False)
    root.title("2d view")
    root.mainloop()

# 2d render of raw data
def render(cp=False):

    global raw

    for i in range(6):
        cords = [[150,150,150,150,75,225],[75,150,225,300,150,150]]
        for i1 in range(9):
            F = tk.Frame(canvas, bg=colors[raw[i][i1]], width=25, height=25)
            if i1 < 3:
                F.place(x=cords[0][i] + i1*25, y=cords[1][i] )
            elif i1 < 6:
                F.place(x=cords[0][i] + (i1-3)*25, y=cords[1][i] + 25 )
            elif i1 < 9:
                F.place(x=cords[0][i] + (i1-6)*25, y=cords[1][i] + 50 )


    dataManagement(1)


    if cp:
        for i in range(0):
            cords = [[150, 150, 150, 150, 75, 225], [75, 150, 225, 300, 150, 150]]
            for i1 in range(9):
                F = tk.Frame(canvas, bg=colors[raw[i][i1]], width=25, height=25)
                if i1 < 3:
                    F.place(x=cords[0][i] + 250 + i1 * 25, y=cords[1][i])
                elif i1 < 6:
                    F.place(x=cords[0][i] + 250 + (i1 - 3) * 25, y=cords[1][i] + 25)
                elif i1 < 9:
                    F.place(x=cords[0][i] + 250 + (i1 - 6) * 25, y=cords[1][i] + 50)


# starts gui thread
threadGUI = Thread(target=GUIthread, args="1")
threadGUI.start()
time.sleep(0.1)


""" ---------- the rest of it ---------- """

# preps data
def dataManagement(type):
    global block, raw, solvedBlock, solvedRaw, solvedBlockCmp


    # type 0 = raw -> block
    if type == 0:
        # *assumes specific rotation
        block = [[raw[4][2], raw[1][0], raw[0][6]], [raw[1][1], raw[0][7]], [raw[5][0], raw[1][2], raw[0][8]], [raw[4][5], raw[1][3]], [raw[1][4]], [raw[5][3], raw[1][5]], [raw[4][8], raw[1][6], raw[2][0]], [raw[1][7], raw[2][1]], [raw[5][6], raw[1][8], raw[2][2]],
                [raw[4][1], raw[0][3]], [raw[0][4]], [raw[5][1], raw[0][5]], [raw[4][4]], [], [raw[5][4]], [raw[4][7], raw[2][3]], [raw[2][4]], [raw[5][7], raw[2][5]],
                [raw[4][0], raw[3][6], raw[0][0]], [raw[3][7], raw[0][1]], [raw[5][2], raw[3][8], raw[0][2]], [raw[4][3], raw[3][3]], [raw[3][4]], [raw[5][5], raw[3][5]], [raw[4][6], raw[3][0], raw[2][6]], [raw[3][1], raw[2][7]], [raw[5][8], raw[3][2], raw[2][8]]]

    # type 1 = block -> raw
    if type == 1:
        raw = list([[block[18][2], block[19][1], block[20][2], block[9][1], block[10][0], block[11][1], block[0][2],block[1][1], block[2][2], ],
               [block[0][1], block[1][0], block[2][1], block[3][1], block[4][0], block[5][1], block[6][1], block[7][0],block[8][1], ],
               [block[6][2], block[7][1], block[8][2], block[15][1], block[16][0], block[17][1], block[24][2],block[25][1], block[26][2], ],
               [block[24][1], block[25][0], block[26][1], block[21][1], block[22][0], block[23][1], block[18][1],block[19][0], block[20][1], ],
               [block[18][0], block[9][0], block[0][0], block[21][0], block[12][0], block[3][0], block[24][0], block[15][0],block[6][0], ],
               [block[2][0], block[11][0], block[20][0], block[5][0], block[14][0], block[23][0], block[8][0], block[17][0], block[26][0], ]])

    # fully solved lists
    solvedBlock = [[4,1,0], [1,0], [5,1,0], [4,1], [1], [5,1], [4,1,2], [1,2], [5,1,2],
            [4,0], [0], [5,0], [4], [], [5], [4,2], [2], [5,2],
            [4,3,0], [3,0], [5,3,0], [4,3], [3], [5,3], [4,3,2], [3,2], [5,3,2]]
    solvedRaw = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2, ],
           [3, 3, 3, 3, 3, 3, 3, 3, 3], [4, 4, 4, 4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5, 5, 5, 5]]
    solvedBlockCmp = [642, 17, 1313, 641, 16, 1312, 722, 97, 1393, 626, 1, 1297, 625, 0, 1296, 706, 81, 1377, 882, 257,
                      1553, 881, 256, 1552, 962, 337, 1633]

# moves segments of the cube
def cycle(axis, val, magnitude):

    # does the move
    movedData = simMove(axis, val, magnitude, -1)
    cp = movedData[0]

    x = []
    for i in range(len(cp)):
        x.append(block[cp[i]])

    # updates block
    for i in range(len(movedData[0])):
        block[movedData[0][i]] = movedData[1][i]

    render(cp=True)

    print("-------- cycled " + str(axis) + " " + str(val) + " " + str(magnitude) + " --------" )

# returns 3d cords and type
def getIndexData(index):

    # type 0 -> corner, 1 -> edge, 2 -> center
    if (index != 13) and (index != 10) and (index != 12) and (index != 4) and (index != 14) and (index != 16) and (index != 22):
        type = index % 2
    else:
        type = 2

    # gets 3d spacial coordinates
    x = ((index - (int(index / 9)*9)) % 3)
    y = int(index / 9)
    z = int((index - (int(index / 9)*9)) / 3)
    return [x, y, z, type]

# completes a move and returns data
def simMove(axis, val, mag, blockIndex):

    # finds critical points
    cp = []
    movedCOL = []
    for i in range(len(block)):
            if getIndexData(i)[axis] == val:
                cp.append(i)
                movedCOL.append(block[i])

    # main rotation pattern implementation
    movedPOS = list(cp)
    realmag = 0
    if blockIndex != -1:
        finalIND = movedPOS.index(idealIndex[blockIndex])
    for i1 in range(mag+1):

        # rotates position
        movedPOS = [movedPOS[6], movedPOS[3], movedPOS[0], movedPOS[7], movedPOS[4], movedPOS[1], movedPOS[8], movedPOS[5], movedPOS[2]]
        movedCOL = [movedCOL[6], movedCOL[3], movedCOL[0], movedCOL[7], movedCOL[4], movedCOL[1], movedCOL[8], movedCOL[5], movedCOL[2]]

        # rotates colors
        for i in range(len(movedCOL)):
            # corner rotation
            newColors = list(movedCOL[i])
            if ((i == 0) or (i == 2) or (i == 6) or (i == 8)) and (len(newColors) == 3):
                if axis == 0:
                    newColors = [newColors[0], newColors[2], newColors[1]]
                if axis == 1:
                    newColors = [newColors[2], newColors[1], newColors[0]]
                if axis == 2:
                    newColors = [newColors[1], newColors[0], newColors[2]]
            # edge rotation
            if (len(newColors) == 2) and ((val == 1) or (axis == 1)):
                newColors = [newColors[1], newColors[0]]
            movedCOL[i] = list(newColors)

        # used to finds mag if need
        if blockIndex != -1:
            if movedPOS.index(blockIndex) == finalIND:
                return realmag, movedCOL[movedPOS.index(blockIndex)]
        realmag += 1

    return cp, movedCOL, movedPOS

# finds the ideal move for each block
def findIdealMoves(block):

    # color data is used to find the move if normal
    def findWithColor():
        # finds axis with color data
        for i in range(len(block[blockIndex])):
            if block[blockIndex][i] == solvedBlock[idealIndex[blockIndex]][i]:
                axis = i
        val = block[blockIndex][axis]
        print("c move @" + str(blockIndex))
        return [axis, val, 0]

    # finds move, if it can be completed in a single move
    def attemptNormalFind():

        # runs movement simulation to get mag
        potentialMoves = []
        for i in range(len(axis)):
            simDATA = simMove(axis[i], indexdata[axis[i]], 999, blockIndex)
            potentialMoves.append([axis[i], indexdata[axis[i]], simDATA[0], simDATA[1]])

        # ensures color data matches
        if len(potentialMoves) == 2:
            if potentialMoves[0][3] == solvedBlock[idealIndex[blockIndex]]:
                finalMove = [potentialMoves[0][0], potentialMoves[0][1], potentialMoves[0][2]]
            elif potentialMoves[1][3] == solvedBlock[idealIndex[blockIndex]]:
                finalMove = [potentialMoves[1][0], potentialMoves[1][1], potentialMoves[1][2]]
            else:
                print("found with color")
                finalMove = findWithColor()
        else:
            finalMove = [potentialMoves[0][0], potentialMoves[0][1], potentialMoves[0][2]]

        # assembly
        moves.append(finalMove)
        return moves

    "complete this"
    def findmultimove():
        pass

    global idealIndex
    moves = []

    # finds ideal index
    # compressed color data to be independent of rotation
    blockCmp = []
    for i in range(len(block)):
        bval = 0
        for i1 in range(len(block[i])):
            bval += (block[i][i1] + 1) * (block[i][i1] + 1) * (block[i][i1] + 1) * (block[i][i1] + 1)
        blockCmp.append(bval)
    idealIndex = []
    for i in range(len(block)):
        idealIndex.append((solvedBlockCmp.index(blockCmp[i])))

    # finds moves
    for blockIndex in range(len(block)):

        # uses xyz to find axis
        indexdata = getIndexData(blockIndex)
        displacement = []
        axis = []
        for i in range(3):
            displacement.append(indexdata[i] - getIndexData(idealIndex[blockIndex])[i])
            if displacement[i] == 0:
                axis.append(i)

        # ignores nonNormal moves
        if (len(axis) != 3) and (axis != []):
            moves = attemptNormalFind()

        # return no move if solved
        elif block[idealIndex[blockIndex]] == solvedBlock[blockIndex]:
            moves.append([-2, -2, -2])

        # return no move if no single move is possible
        else:
            moves.append([-1, -1, -1])


    print("moves " + str(moves))
    return moves

def findCrossDisplacement(crossMove, block):

    if (crossMove != [-1, -1, -1]) and (crossMove != [-2, -2, -2]):

        netDifferance = 0

        # gets new block with sim data
        simData = simMove(crossMove[0], crossMove[1], crossMove[2], -1)
        critical_points = simData[0]

        # forms new block with simData
        simBlock = list(block)
        for i in range(len(block)):
            for j in range(len(critical_points)):
                if critical_points[j] == i:
                    simBlock[i] = simData[1][j]

        # compares simBlock to SolvedBlock to find POS differance
        points = [1, 3, 4, 5, 7]
        for i in range(5):
            if simBlock[points[i]] == solvedBlock[points[i]]:
                netDifferance += 1

        # compares simBlock to SolvedBlock to find MOVES differance

        # finds ideal simIndex
        simBlockCmp = []
        for i in range(len(simBlock)):
            bval = 0
            for j in range(len(block[i])):
                bval += (simBlock[i][j] + 1) * (simBlock[i][j] + 1) * (simBlock[i][j] + 1) * (simBlock[i][j] + 1)
            simBlockCmp.append(bval)
        simIdealIndex = []
        for i in range(len(simBlock)):
            simIdealIndex.append((solvedBlockCmp.index(simBlockCmp[i])))

        moves = 0
        for i in range(5):

            point = points[i]

            part = getIndexData(point)
            idealPart = getIndexData(simIdealIndex[point])

            common_axis = 0
            for j in range(3):
                if part[j] == idealPart[j]:
                    common_axis += 1

            # must move along 3 axis (2 moves needed)
            if common_axis == 0:
                moves += 3
            # must move along 1 or 2 axis (1 or 3 moves needed)
            elif (common_axis == 1) or (common_axis == 2):
                moves += 1
            # solved (0 moves needed)
            elif (common_axis == 3) and (simBlock[i] == solvedBlock[i]):
                moves += 0
            # right position wrong colors (3 moves need)
            else:
                moves += 5

        return [netDifferance, moves]
    return -1

# solves the thing
def solve():

    print("---------- solve -------------------------------------")
    dat = []
    for axis in range(3):
        for val in range(3):
            for mag in range(3):
                move = [axis, val, mag]
                x = findCrossDisplacement(move, block)
                print("move " + str(move) + " disp " + str(x[0]) + " moves " +  str(x[1]))
                dat.append([x[0], x[1], move])

    print("------------")
    top = dat[0][0]
    for i in range(len(dat)):
        if dat[i][0] > top:
            top = dat[i][0]
    for i in range(len(dat)):
        if dat[i][0] == top:
            print("move " + str(dat[i][2]) + " " + str(dat[i][0]) + " " + str(dat[i][1]))
    print("------------")
    top = dat[0][1]
    for i in range(len(dat)):
        if dat[i][1] > top:
            top = dat[i][1]
    for i in range(len(dat)):
        if dat[i][1] == top:
            print("move " + str(dat[i][2]) + " " + str(dat[i][0]) + " " + str(dat[i][1]))

    print("------------------------------------------------------")

    render()


""" --------------testing--------------- """
# randomizes cube
def shuffle():
    for i in range(random.randint(45, 50)):
        cycle(random.randint(0, 2), random.randint(0, 2), random.randint(0, 2))
    print("------------ completed shuffle ------------")
    render()
# moves through each move
def testingloop():

    render()
    for i in range(3):
        for i1 in range(3):
            for i2 in range(3):

                cycle(i, i1, i2)
                render()
                time.sleep(1)

                if i2 == 2:
                    m = 0
                elif i2 == 1:
                    m = 1
                else:
                    m = 2
                cycle(i, i1, m)

def func():

    simBlockCmp = []
    for i in range(len(block)):
        bval = 0
        for j in range(len(block[i])):
            bval += (block[i][j] + 1) * (block[i][j] + 1) * (block[i][j] + 1) * (block[i][j] + 1)
        simBlockCmp.append(bval)
    simIdealIndex = []
    for i in range(len(block)):
        simIdealIndex.append((solvedBlockCmp.index(simBlockCmp[i])))

    for i in range(len(block)):

        part = getIndexData(i)
        idealPart = getIndexData(simIdealIndex[i])

        common_axis = 0
        for j in range(3):
            if part[j] == idealPart[j]:
                common_axis += 1

        print(common_axis)

""" --------------------------------- """
dataManagement(0)
#testingloop()

# temp loop for testing
while True:
    render()
    print("")
    x = input("enter command: ")
    if x == "moves":
        findIdealMoves(block=block)
    elif x == "shuf":
        shuffle()
    elif x == "solve":
       solve()
    elif x == "func":
        func()
    else:
        cycle(int(x[0]),int(x[1]),int(x[2]))
        findIdealMoves(block=block)
