import random
import time
import tkinter as tk
from threading import Thread


# http://ozcubegirl.com/rubikscubesolution.html

# raw input data (may need to be rotated )
raw = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2, ],
       [3, 3, 3, 3, 3, 3, 3, 3, 3], [4, 4, 4, 4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5, 5, 5, 5]]


""" -------------- GUI -------------- """

# colors - green-0  white-1  blue-2   yellow-3   red-4   orange-5
colors = ["#00cc00","#ffffff","#0099ff","#ffff00","#ff0000","#fc8403"]

# tk junk
def GUIthread(name):

    global root, canvas
    root = tk.Tk()
    root.geometry('500x500')
    canvas = tk.Canvas(root, height=500, width=500, bg="#262626")
    canvas.pack()
    root.resizable(False, False)
    root.title("2d view")
    root.mainloop()

# 2d render of raw data
renders = 0
def render():

    global raw, renders


    for child in canvas.winfo_children():
        if (str(child)[len(str(child))-1] == 0 and renders == 1) or (str(child)[len(str(child))-1] == 0 and renders == 1):
            print(child)
            child.destroy()

    for i in range(6):
        cords = [[150, 150, 150, 150, 65, 235], [75, 160, 245, 330, 160, 160]]
        for i1 in range(9):
            F = tk.Frame(canvas, bg=colors[raw[i][i1]], width=25, height=25, name= "2d-view-frame" + str(i1) + str(i) + "num" + str(renders))
            if i1 < 3:
                F.place(x=cords[0][i] + i1*25, y=cords[1][i])
            elif i1 < 6:
                F.place(x=cords[0][i] + (i1-3)*25, y=cords[1][i] + 25)
            elif i1 < 9:
                F.place(x=cords[0][i] + (i1-6)*25, y=cords[1][i] + 50)

    dataManagement(1)
    renders += 1
    if renders == 2:
        renders = 0


# starts gui thread
threadGUI = Thread(target=GUIthread, args="1")
threadGUI.start()
time.sleep(0.1)

""" ---------- Block Management ---------- """

# preps data
inverseMove = [-1, -1, -1]
def dataManagement(type):

    global block, raw, solvedBlock, solvedRaw, solvedBlockCmp, oldBlocks


    # type 0 = raw -> activeBlock
    if type == 0:
        # *assumes specific rotation
        block = [[raw[4][2], raw[1][0], raw[0][6]], [raw[1][1], raw[0][7]], [raw[5][0], raw[1][2], raw[0][8]], [raw[4][5], raw[1][3]], [raw[1][4]], [raw[5][3], raw[1][5]], [raw[4][8], raw[1][6], raw[2][0]], [raw[1][7], raw[2][1]], [raw[5][6], raw[1][8], raw[2][2]],
                [raw[4][1], raw[0][3]], [raw[0][4]], [raw[5][1], raw[0][5]], [raw[4][4]], [], [raw[5][4]], [raw[4][7], raw[2][3]], [raw[2][4]], [raw[5][7], raw[2][5]],
                [raw[4][0], raw[3][6], raw[0][0]], [raw[3][7], raw[0][1]], [raw[5][2], raw[3][8], raw[0][2]], [raw[4][3], raw[3][3]], [raw[3][4]], [raw[5][5], raw[3][5]], [raw[4][6], raw[3][0], raw[2][6]], [raw[3][1], raw[2][7]], [raw[5][8], raw[3][2], raw[2][8]]]

    # type 1 = activeBlock -> raw
    if type == 1:
        raw = list([[block[18][2], block[19][1], block[20][2], block[9][1], block[10][0], block[11][1], block[0][2],block[1][1], block[2][2], ],
               [block[0][1], block[1][0], block[2][1], block[3][1], block[4][0], block[5][1], block[6][1], block[7][0],block[8][1], ],
               [block[6][2], block[7][1], block[8][2], block[15][1], block[16][0], block[17][1], block[24][2],block[25][1], block[26][2], ],
               [block[24][1], block[25][0], block[26][1], block[21][1], block[22][0], block[23][1], block[18][1],block[19][0], block[20][1], ],
               [block[18][0], block[9][0], block[0][0], block[21][0], block[12][0], block[3][0], block[24][0], block[15][0],block[6][0], ],
               [block[2][0], block[11][0], block[20][0], block[5][0], block[14][0], block[23][0], block[8][0], block[17][0], block[26][0], ]])

    # fully solved lists
    solvedBlock = [[4, 1, 0], [1, 0], [5, 1, 0], [4, 1], [1], [5, 1], [4, 1, 2], [1, 2], [5, 1, 2],
        [4, 0], [0], [5, 0], [4], [], [5], [4, 2], [2], [5, 2],
        [4, 3, 0], [3, 0], [5, 3, 0], [4, 3], [3], [5, 3], [4, 3, 2], [3, 2], [5, 3, 2]]

    solvedRaw = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [1, 1, 1, 1, 1, 1, 1, 1, 1], [2, 2, 2, 2, 2, 2, 2, 2, 2, ],
        [3, 3, 3, 3, 3, 3, 3, 3, 3], [4, 4, 4, 4, 4, 4, 4, 4, 4], [5, 5, 5, 5, 5, 5, 5, 5, 5]]

    solvedBlockCmp = [642, 17, 1313, 641, 16, 1312, 722, 97, 1393, 626, 1, 1297, 625, 0, 1296, 706, 81, 1377, 882, 257,
                      1553, 881, 256, 1552, 962, 337, 1633]
dataManagement(0)

# returns 3d cords and type
def getIndexData(index):

    # type 0 -> corner, 1 -> edge, 2 -> center
    if (index != 13) and (index != 10) and (index != 12) and (index != 4) and (index != 14) and (index != 16) and (index != 22):
        type = index % 2
    else:
        type = 2

    # gets 3d coordinates
    x = ((index - (int(index / 9)*9)) % 3)
    y = int(index / 9)
    z = int((index - (int(index / 9)*9)) / 3)
    return [x, y, z, type]

""" ---------- Moves Management ---------- """

# completes a move and returns data
def simMove(axis, val, mag, baseBlock=block):

    #print("sim " + str(axis) + " " + str(val) + " " + str(mag))
    #print("simed " + str(compressBlock(baseBlock)))

    # finds critical points
    criticalPoints = []
    movedCOL = []
    for i in range(len(baseBlock)):
        if getIndexData(i)[axis] == val:
            criticalPoints.append(i)
            movedCOL.append(baseBlock[i])
    movedPOS = list(criticalPoints)

    # repeat the rotation process based on desired out come
    for i in range(mag+1):

        # rotates position
        movedPOS = [movedPOS[6], movedPOS[3], movedPOS[0], movedPOS[7], movedPOS[4], movedPOS[1], movedPOS[8], movedPOS[5], movedPOS[2]]
        movedCOL = [movedCOL[6], movedCOL[3], movedCOL[0], movedCOL[7], movedCOL[4], movedCOL[1], movedCOL[8], movedCOL[5], movedCOL[2]]

        # rotates colors
        for j in range(len(movedCOL)):

            # corner color rotation
            newColors = list(movedCOL[j])
            if ((j == 0) or (j == 2) or (j == 6) or (j == 8)) and (len(newColors) == 3):
                if axis == 0:
                    newColors = [newColors[0], newColors[2], newColors[1]]
                if axis == 1:
                    newColors = [newColors[2], newColors[1], newColors[0]]
                if axis == 2:
                    newColors = [newColors[1], newColors[0], newColors[2]]

            # edge color rotation
            if (len(newColors) == 2) and ((val == 1) or (axis == 1)):
                newColors = [newColors[1], newColors[0]]
            movedCOL[j] = list(newColors)

    simBlock = list(baseBlock)
    for i in range(len(baseBlock)):
        for j in range(len(criticalPoints)):
            if i == criticalPoints[j]:
                simBlock[i] = movedCOL[j]

    return simBlock

# moves segments of the cube
def cycle(axis, val, magnitude):
    global block, inverseMove
    newBlock = simMove(axis, val, magnitude, block)
    block = list(newBlock)
    inverseMove = [axis, val, 3-(1+magnitude)]

# compressed color data to be independent of rotation
def compressBlock(activeBlock):
    compressedBlock = []

    for i in range(len(activeBlock)):
        compressedData = 0
        for j in range(len(activeBlock[i])):
            compressedData += pow((activeBlock[i][j] + 1), 4)
        compressedBlock.append(compressedData)

    return compressedBlock

# finds the ideal moves for each activeBlock
def findIdealMoves(activeBlock, blockIndex):

    # finds moves for 1 or 2 common axis
    def findMoveWithAxis(indexData, baseBlock):

        move = []

        # determines if move is solved
        if baseBlock[blockIndex] == solvedBlock[blockIndex]:
            return [-2, -2, -2]

        # tests potential moves
        for i in range(3):
            for j in range(3):
                testedBlock = simMove(axis=i, val=indexData[i], mag=j, baseBlock=baseBlock)
                # finds which move satisfies the blockIndex
                if testedBlock[blockIndex] == solvedBlock[blockIndex]:
                    move = [i, indexData[i], j]

        # if no moves are correct, the move is considered to be indeterminate
        if not move:
            move = [-4, -4, -4]

        return move

    # var setup
    indexData = getIndexData(blockIndex)
    blockCmp = compressBlock(activeBlock)
    currentIndexData = getIndexData(blockCmp.index(solvedBlockCmp[blockIndex]))
    testedBlocks = [[], [], []]
    move = []

    # returns [-2, -2, -2] if solved
    if activeBlock[blockIndex] == solvedBlock[blockIndex]:
        return [[[-2, -2, -2]]]

    # finds sequences of moves
    # repeat for each axis
    for i in range(3):
        # repeat for each mag
        for j in range(3):

            # test moves to find mag
            testedBlocks[i].append(simMove(axis=i, val=currentIndexData[i], mag=j, baseBlock=activeBlock))
            testedCmp = compressBlock(testedBlocks[i][j])
            simIndexData = getIndexData(testedCmp.index(solvedBlockCmp[blockIndex]))

            # determines if the move simplified the problem
            commonAxis = 0
            for k in range(3):
                if simIndexData[k] == indexData[k]:
                    commonAxis += 1

            if commonAxis == 3:
                move.append([[i, currentIndexData[i], j], [-2, -2, -2]])

            # finds the next move in the sequence
            if commonAxis >= 1:
                move.append([[i, currentIndexData[i], j], findMoveWithAxis(indexData=simIndexData, baseBlock=testedBlocks[i][j])])


    return move
findIdealMoves(block, 0)

# finds THE! ideal move
def solve():

    # analyzes simBlocks to select the best move
    def getParameters(baseBlock):


        typeParameters = [0, 0, 0, 0]

        # gets the ideal moves for the new block
        moves = []
        for i in range(len(ind)):
            moves.append(findIdealMoves(activeBlock=baseBlock, blockIndex=ind[i]))

        # identifies if the block solves the center
        if baseBlock[4] == solvedBlock[4]:
            typeParameters[3] += 1

        # repeat for each piece
        for i in range(len(moves)):

            # looks for solved pieces
            if moves[i] == [[[-2, -2, -2]]]:
                typeParameters[0] += 1
            else:

                # repeat for each move
                for k in range(len(moves[i])):
                    # looks for one-moves
                    if [-2, -2, -2] in moves[i][k]:
                        typeParameters[1] += 1
                        break
                    # looks for two-moves
                    elif k == len(moves[i])-1:
                        typeParameters[2] += 1

        return typeParameters

    # finds min/max of specified parameter
    def findExtreme(type, parameter):
        # type = 1 for min, type = 0 for max

        parameterVals = []
        tempMoves = []
        tempParameters = []

        # assembles list of specified parameters
        for i in range(len(potentialParameters)):
            parameterVals.append(potentialParameters[i][parameter])

        # finds extreme value (min/max)
        if type == 1:
            extremeVal = min(parameterVals)
        else:
            extremeVal = max(parameterVals)

        # tests if each parameter reached the extreme value
        for i in range(len(potentialParameters)):
            if potentialParameters[i][parameter] == extremeVal:
                tempMoves.append(potentialMoves[i])
                tempParameters.append(potentialParameters[i])

        return [tempMoves, tempParameters]

    # gets moves sequences
    ind = [1, 3, 4, 5, 7]
    parameters = []
    idealMoves = []
    for i in range(len(ind)):

        # gets moves sequences
        moves = findIdealMoves(activeBlock=block, blockIndex=ind[i])

        # repeat for each sequence of moves
        for j in range(len(moves)):
            if [-4, -4, -4] not in moves[j]:
                if moves[j] != [[-2, -2, -2]]:

                    # assembles idealMoves list
                    idealMoves.append(moves[j])

                    # generates simBlocks
                    if list([-2, -2, -2]) not in moves[j]:
                        intermediateBlock = list(simMove(moves[j][0][0], moves[j][0][1], moves[j][0][2], block))
                        simBlock = simMove(moves[j][1][0], moves[j][1][1], moves[j][1][2], baseBlock=intermediateBlock)
                    else:
                        simBlock = simMove(moves[j][0][0], moves[j][0][1], moves[j][0][2], baseBlock=block)

                    # gets info on simBlock
                    parameters.append(getParameters(simBlock))

    # checks if the cross is solved
    solved = True
    for i in range(5):
        if block[ind[i]] != solvedBlock[ind[i]]:
            solved = False
    if solved:
        #print("SOLVED (woo)")
        return [-2, -2, -2]

    # solves rotation problem (WIP)
    rotationError = True
    blockCmp = compressBlock(block)
    for i in range(5):
        if blockCmp[ind[i]] != solvedBlockCmp[ind[i]]:
            rotationError = False
    if rotationError:
        #print("rotation error")
        return [-3, -3, -3]

    # finds moves that solve the center
    potentialMoves = []
    potentialParameters = []
    for i in range(len(idealMoves)):
        if (parameters[i][3] == 1) and idealMoves[i][0] != inverseMove:
            potentialMoves.append(idealMoves[i])
            potentialParameters.append(parameters[i])

    # ensure potentialMoves/Parameters is not equal to []
    if not potentialMoves:
        for i in range(len(idealMoves)):
            if idealMoves[i][0] != inverseMove:
                potentialMoves.append(idealMoves[i])
                potentialParameters.append(parameters[i])

    # finds moves that maximizes the amount of zero-Moves
    refinedLists = findExtreme(0, 0)
    potentialMoves = refinedLists[0]
    potentialParameters = refinedLists[1]

    # finds moves that minimize the amount of one-Moves
    refinedLists = findExtreme(0, 2)
    potentialMoves = refinedLists[0]
    potentialParameters = refinedLists[1]

    # finds moves that minimize the amount of two-Moves
    refinedLists = findExtreme(1, 3)
    potentialMoves = refinedLists[0]
    potentialParameters = refinedLists[1]

    # finds the frequency of each move
    frequency = []
    for i in range(len(potentialMoves)):
        frequency.append(0)
        for j in range(len(idealMoves)):
            if idealMoves[j][0] == potentialMoves[i][0]:
                frequency[i] += 1

    maxInd = frequency.index(max(frequency))

    return potentialMoves[maxInd][0]

""" -------------- Testing --------------- """
# randomizes cube
def shuffle():
    for i in range(random.randint(45, 50)):
        cycle(random.randint(0, 2), random.randint(0, 2), random.randint(0, 2))


# spams solve/cycle
def test():
    for i in range(20):
        move = solve()
        if (move == [-2, -2, -2]) or (move == [-3, -3, -3]):
            return True, i
        else:
            cycle(move[0], move[1], move[2])
    return False, i

def testingLoop():

    global block
    passed = 0
    totalTime = 0
    numOfMoves = 0
    recoveryMoves = 0
    needRecovery = 1

    for i in range(10000):

        start = time.monotonic()
        # runs test
        shuffle()
        holderBlock = block
        results = test()
        hasPassed = results[0]

        # if test fails retry with rand move
        if not hasPassed:
            needRecovery += 1
            while True:
                # reruns test
                block = list(holderBlock)
                cycle(random.randint(0, 2), random.randint(0, 2), random.randint(0, 2))
                results = test()
                hasPassed = results[0]
                recoveryMoves += 1

                # evaluates results
                if hasPassed:
                    passed += 1
                    numOfMoves += results[1] + 1
                    break

        else:
            passed += 1
            numOfMoves += results[1]

        totalTime += time.monotonic() - start
        AvgTime = totalTime / (i+1)
        AvgNumOfMoves = numOfMoves / (i+1)
        AvgRecovery = recoveryMoves / needRecovery

        # records results
        with open("tempTestngData.txt", "w") as file:
            data = [str(i) + " num of completed test \n", str(AvgTime) + " avg time \n",
                    str(AvgNumOfMoves) + " avg num of moves \n", str(AvgRecovery) + " avg num of recovery moves \n",
                    str(needRecovery) + " needed recovery  \n"]
            file.writelines(data)
        file.close()


""" -------------------------------------- """

# temp loop for testing
while True:

    render()
    print("")
    x = input("enter command: ")

    if x == "shuf":
        shuffle()
    elif x == "solve":
       solve()
    elif x == "test":
       test()
    elif x == "start":
       testingLoop()
    elif "idm " in x:
       findIdealMoves(block, int(x[4]))
    elif "sim " in str(x):
        print(simMove(int(x[4]), int(x[5]), int(x[6]), block))
    else:
        cycle(int(x[0]),int(x[1]),int(x[2]))

