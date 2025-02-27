"""
this was used to solve the white corners, its no longer needed
"""

# finds a sequence to solve a white corner
def findBestCornerSeq(index=-1, activeBlock=config.block):


    # the main method for solving a conner
    def findMainSeq(activeBlock):

        # determines a initial rotation is needed
        colors = activeBlock[currentInd]
        nextInd = ind[i] + 18
        firstMove = [-2, -2, -2]
        if currentInd - 18 != ind[i]:

            # finds the move the places the corner above its ideal spot
            for k in range(3):
                simPos = RBX_Cube.getIndexData(RBX_Cube.simPositionalChange(1, 2, k, activeBlock).index(currentInd))
                if (simPos[0] == RBX_Cube.getIndexData(ind[i])[0]) and (simPos[2] == RBX_Cube.getIndexData(ind[i])[2]):
                    firstMove = [1, 2, k]


        # finds the other color on the x/z axis
        for k in range(3):
            if (colors[k] != 1) and (k != 1):
                if (colors[k] == 0) or (colors[k] == 2):
                    mainColor = 0
                else:
                    mainColor = 2

        # finds the move to aline main-color with secondary-color
        nextIndData = RBX_Cube.getIndexData(nextInd)
        if (nextIndData[0] == nextIndData[2]) and (mainColor == 0):
            secondMove = [1, 2, 2]
        elif (nextIndData[0] != nextIndData[2]) and (mainColor == 2):
            secondMove = [1, 2, 2]
        else:
            secondMove = [1, 2, 0]

        # finds the axis for next move
        if firstMove != -2:
            holderBlock = RBX_Cube.simMove(firstMove[0], firstMove[1], firstMove[2], activeBlock)
        else:
            holderBlock = activeBlock
        newIndData = RBX_Cube.getIndexData(compressBlock(RBX_Cube.simMove(secondMove[0], secondMove[1], secondMove[2],holderBlock)).index(config.solvedBlockCmp[ind[i]]))
        indData = RBX_Cube.getIndexData(ind[i])
        for k in range(3):
            if newIndData[k] == indData[k]:
                axis = 2 - k

        # finds the mag for the next move
        if ((newIndData[0] == 2) and ((newIndData[0] != 2) or (newIndData[2] != 0) or (axis != 0)))\
                or ((newIndData[0] == 0) and (newIndData[2] == 2) and (axis == 0)):
            mag = 2
        else:
            mag = 0
        fifthMove = [axis, indData[axis], mag]

        # assembly
        seq.append(firstMove)
        seq.append(secondMove)
        seq.append([fifthMove[0], fifthMove[1], 2-fifthMove[2]])
        seq.append([secondMove[0], secondMove[1], 2-secondMove[2]])
        seq.append(fifthMove)

    # loop for each ind
    ind = [0, 2, 6, 8]
    blockCmp = compressBlock(activeBlock)
    mainSeq = []

    if index != -1:
        ind = [index]

    for i in range(len(ind)):

        seq = []
        currentInd = blockCmp.index(config.solvedBlockCmp[ind[i]])
        currentIndData = RBX_Cube.getIndexData(currentInd)
        indData = RBX_Cube.getIndexData(ind[i])

        # ignores solved pieces
        if activeBlock[ind[i]] == config.solvedBlock[ind[i]]:
            continue

        # determines if a piece is properly positioned and rotated
        if (currentIndData[1] == 2) and (activeBlock[currentInd][1] != 1):
            # runs main solving method
            findMainSeq(activeBlock)

        # rotates pieces / or moves them to the top
        elif ((currentIndData[0] == indData[0]) and (currentIndData[2] == indData[2])) or (currentIndData[1] == 0):
            # assembly
            seq.append([0, currentIndData[0], 2 - currentIndData[2]])
            seq.append([1, 2, 2])
            seq.append([0, currentIndData[0], currentIndData[2]])

        # align pieces for rotation
        else:
            # gets mag for rotation
            for k in range(3):
                if RBX_Cube.simPositionalChange(1, 2, k, activeBlock).index(currentInd) == ind[i]:
                    seq.append([1, 2, k])
                    break
        mainSeq.append(seq)


    # returns best seq
    #print(f"mainSEQ {mainSeq}")
    for i in range(len(mainSeq)):
        if (len(mainSeq[i]) > 3) or (i == len(mainSeq)-1):
            return mainSeq[i]
    return [[-2, -2, -2]]
# solves the white-corners (step 2)
def solveWhiteCorners():

    print("-------- SOLVING WHITE CORNERS --------")

    while True:
        seq = findBestCornerSeq(activeBlock=config.block)
        RBX_Cube.render()
        # exit when solved
        if seq == [[-2, -2, -2]]:
            break
        # runs seq
        for i in range(len(seq)):
            RBX_Cube.cycle(seq[i][0], seq[i][1], seq[i][2])
            RBX_Cube.render()

    print("SOLVED (woo)")