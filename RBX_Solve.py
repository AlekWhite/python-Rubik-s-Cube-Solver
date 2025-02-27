"""
This file is focused on solving the cube by analyzing simulated moves.
It follows the "Fridrich First two layers" method of solving.
"""
import ast, random, time, tkinter as tk, RBX_Cube, config, RBX_Sender
from threading import Thread
from termcolor import colored

# reference material
# https://ruwix.com/the-rubiks-cube/advanced-cfop-fridrich/first-two-layers-f2l/

""" ----------------- Solve -----------------  """

# compressed color data to be independent of rotation
def compressBlock(activeBlock):
    compressedBlock = []

    for i in range(len(activeBlock)):
        compressedData = 0
        for j in range(len(activeBlock[i])):
            compressedData += pow((activeBlock[i][j] + 1), 4)
        compressedBlock.append(compressedData)

    return compressedBlock

# finds the ideal moves for each activeBlock (step 1)
def findIdealMoves(activeBlock, blockIndex):

    # finds moves for 1 or 2 common axis
    def findMoveWithAxis(indexData, baseBlock):

        move = []

        # determines if move is solved
        if baseBlock[blockIndex] == config.solvedBlock[blockIndex]:
            return [-2, -2, -2]

        # tests potential moves
        for i in range(3):
            for j in range(3):
                testedBlock = RBX_Cube.simMove(axis=i, val=indexData[i], mag=j, baseBlock=baseBlock)
                # finds which move satisfies the blockIndex
                if testedBlock[blockIndex] == config.solvedBlock[blockIndex]:
                    move = [i, indexData[i], j]

        # if no moves are correct, the move is considered to be indeterminate
        if not move:
            move = [-4, -4, -4]

        return move

    # var setup
    indexData = RBX_Cube.getIndexData(blockIndex)
    blockCmp = compressBlock(activeBlock)
    currentIndexData = RBX_Cube.getIndexData(blockCmp.index(config.solvedBlockCmp[blockIndex]))
    testedBlocks = [[], [], []]
    move = []

    # returns [-2, -2, -2] if solved
    if activeBlock[blockIndex] == list(config.solvedBlock[blockIndex]):
        return [[[-2, -2, -2]]]

    # finds sequences of moves
    # repeat for each axis
    for i in range(3):
        # repeat for each mag
        for j in range(3):

            # test moves to find mag
            testedBlocks[i].append(RBX_Cube.simMove(axis=i, val=currentIndexData[i], mag=j, baseBlock=activeBlock))
            testedCmp = compressBlock(testedBlocks[i][j])
            simIndexData = RBX_Cube.getIndexData(testedCmp.index(config.solvedBlockCmp[blockIndex]))

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
findIdealMoves(config.block, 0)

# solves the white-cross (step 1)
def solveWhiteCross():

    # finds the ideal move for WC
    def findBestMove():

        ind = [1, 3, 4, 5, 7]

        # analyzes simBlocks to select the best move
        def getParameters(baseBlock):

            typeParameters = [0, 0, 0, 0]
            for i in range(len(ind)):

                # var setup
                currentInd = compressBlock(baseBlock).index(config.solvedBlockCmp[ind[i]])
                currentIndData = RBX_Cube.getIndexData(currentInd)
                IndexData = RBX_Cube.getIndexData(ind[i])

                # finds common axis
                shardedAxis = []
                for j in range(3):
                    if currentIndData[j] == IndexData[j]:
                        shardedAxis.append(j)

                # determines of the colors have the right rotation
                match = False
                if baseBlock[currentInd] == config.solvedBlock[ind[i]]:
                    match = True

                # evaluates match to find num of moves
                if len(shardedAxis) == 3:
                    typeParameters[0] += 1
                elif ((len(shardedAxis) == 2) and match) or ((len(shardedAxis) == 1) and not match):
                    typeParameters[1] += 1
                else:
                    typeParameters[2] += 1

            # identifies if the block solves the center
            if simBlock[4] == config.solvedBlock[4]:
                typeParameters[3] += 1

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
        parameters = []
        idealMoves = []
        for i in range(len(ind)):

            # gets moves sequences
            moves = findIdealMoves(activeBlock=config.block, blockIndex=ind[i])

            # repeat for each sequence of moves
            for j in range(len(moves)):
                if [-4, -4, -4] not in moves[j]:
                    if moves[j] != [[-2, -2, -2]]:

                        # generates simBlocks
                        if list([-2, -2, -2]) not in moves[j]:
                            intermediateBlock = list(
                                RBX_Cube.simMove(moves[j][0][0], moves[j][0][1], moves[j][0][2], config.block))
                            simBlock = RBX_Cube.simMove(moves[j][1][0], moves[j][1][1], moves[j][1][2],
                                                        baseBlock=intermediateBlock)
                        else:
                            simBlock = RBX_Cube.simMove(moves[j][0][0], moves[j][0][1], moves[j][0][2],
                                                        baseBlock=config.block)

                        # gets info on simBlock and, assembles idealMoves list
                        idealMoves.append(moves[j])
                        parameters.append(getParameters(simBlock))

        # checks if the cross is solved
        solved = True
        for i in range(5):
            if config.block[ind[i]] != config.solvedBlock[ind[i]]:
                solved = False
        if solved:
            print(colored("SOLVED (woo)", "green"))
            return [-2, -2, -2]

        # solves rotation problem
        rotationError = True
        blockCmp = compressBlock(config.block)
        for i in range(5):
            if blockCmp[ind[i]] != config.solvedBlockCmp[ind[i]]:
                rotationError = False
        if rotationError:
            print("rotation error")
            return [-3, -3, -3]

        """
        # print statements
        for i in range(len(idealMoves)):
            print(str(idealMoves[i]) + " " + str(parameters[i]))
        """

        # finds moves that solve the center
        potentialMoves = []
        potentialParameters = []
        for i in range(len(idealMoves)):
            if (parameters[i][3] == 1) and (idealMoves[i][0] != config.inverseMove):
                potentialMoves.append(idealMoves[i])
                potentialParameters.append(parameters[i])

        # ensure potentialMoves/Parameters is not equal to []
        if not potentialMoves:
            for i in range(len(idealMoves)):
                if idealMoves[i][0] != config.inverseMove:
                    potentialMoves.append(idealMoves[i])
                    potentialParameters.append(parameters[i])

        # finds moves that maximizes the amount of zero-Moves
        refinedLists = findExtreme(0, 0)
        potentialMoves = refinedLists[0]
        potentialParameters = refinedLists[1]

        # finds moves that minimize the amount of one-Moves
        refinedLists = findExtreme(1, 2)
        potentialMoves = refinedLists[0]
        potentialParameters = refinedLists[1]

        # finds moves that minimize the amount of two-Moves+
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
            # print(potentialMoves[maxInd])

        return potentialMoves[maxInd][0]

    print("-------- SOLVING WHITE CROSS --------")
    holderBlock = list(config.block)
    counter = 0
    config.moveSequence = []
    while True:

        # loops find best move until solved
        solved = False
        for i in range(15):

            move = findBestMove()

            # exits when solved
            if move == [-2, -2, -2]:
                solved = True
                break

            # rotates in place
            elif move == [-3, -3, -3]:
                ind = [1, 3, 5, 7]
                for k in range(len(ind)):

                    # ignores solved ind's
                    if config.block[ind[k]] == config.solvedBlock[ind[k]]:
                        continue
                    # var setup
                    currentInd = compressBlock(config.block).index(config.solvedBlockCmp[ind[k]])
                    currentIndData = RBX_Cube.getIndexData(currentInd)
                    # gets axis
                    axis = 0
                    if (ind[k] == 1) or (ind[k] == 7):
                        axis = 2
                    # gets mag
                    mag = 0
                    if (ind[k] == 1) or (ind[k] == 5):
                        mag = 2
                    # assembly
                    RBX_Cube.cycle(axis, currentIndData[axis], 0)
                    RBX_Cube.cycle(1, 1, mag)
                    RBX_Cube.cycle(axis, currentIndData[axis], 0)

                solved = True
                break

            # runs normal moves
            else:
                RBX_Cube.cycle(move[0], move[1], move[2])


        # exits if solved
        if solved:
            break

        print("rerun")
        # if the solve process failed, attempted to solve again
        config.block = list(holderBlock)
        config.moveSequence = []
        allMoves = [[0, 0, 0], [0, 1, 0], [0, 2, 0], [0, 0, 1], [0, 1, 1], [0, 2, 1], [0, 0, 2], [0, 1, 2], [0, 2, 2],
                    [1, 0, 0], [1, 1, 0], [1, 2, 0], [1, 0, 1], [1, 1, 1], [1, 2, 1], [1, 0, 2], [1, 1, 2], [1, 2, 2],
                    [2, 0, 0], [2, 1, 0], [2, 2, 0], [2, 0, 1], [2, 1, 1], [2, 2, 1], [2, 0, 2], [2, 1, 2], [2, 2, 2]]
        RBX_Cube.cycle(allMoves[counter][0], allMoves[counter][1], allMoves[counter][2])
        counter += 1
        config.cycles = 1
        config.reRuns += 1

# solves the centers in 1 move (step 1.5)
def solveCenters():
    print("-------- SOLVING CENTERS --------")
    if config.block[10] != config.solvedBlock[10]:

        # gets mag for rotation
        for i in range(3):
            simBlock = RBX_Cube.simMove(1, 1, i, config.block)
            if simBlock.index(config.solvedBlock[10]) == 10:
                mag = i

        RBX_Cube.cycle(1, 1, mag)

    print(colored("SOLVED (woo)", "green"))

# finds the ideal seqs to solve one edge corner pairs (step 2)
def findF2LSeqs(block=config.block, mainIndex=0):

    #print(f" \n {mainIndex} ")

    indC = [0, 2, 6, 8]
    indE = [9, 11, 15, 17]

    # gets basic info on the current state of a specified piece
    def getCurrentPieceInfo(index, block):
        blockCmpP = compressBlock(block)
        currentIndCorP = blockCmpP.index(config.solvedBlockCmp[indC[index]])
        currentIndDataCorP = RBX_Cube.getIndexData(currentIndCorP)
        currentIndEdgP = blockCmpP.index(config.solvedBlockCmp[indE[index]])
        currentIndDataEdgP = RBX_Cube.getIndexData(currentIndEdgP)
        return [blockCmpP, currentIndCorP, currentIndDataCorP, currentIndEdgP, currentIndDataEdgP]

    # aligns pieces above there ideal location
    def attemptBasicAlignment(index, block):

        data = getCurrentPieceInfo(index, block)
        blockCmpP = data[0]
        currentIndDataCorP = data[2]
        currentIndDataEdgP = data[4]
        indEUpper = [[19, 21], [19, 23], [21, 25], [23, 25]]

        # ignores solved inds
        if (blockCmpP[indC[index] + 18] == config.solvedBlockCmp[indC[index]]) and \
           ((block[indEUpper[index][0]] == config.solvedBlock[indE[index]]) or
           block[indEUpper[index][1]] == config.solvedBlock[indE[index]]):
            return [False, [[]]]

        # aligns corner, if both are on top OR the edge has the right position
        if (currentIndDataCorP[1] == 2) and ((currentIndDataEdgP[1] == 2) or
           (blockCmpP[indE[index]] == config.solvedBlockCmp[indE[index]])):
            for k in range(3):
                simBlock = RBX_Cube.simMove(1, 2, k, block)
                simBlockCmp = compressBlock(simBlock)
                if simBlockCmp[indC[index] + 18] == config.solvedBlockCmp[indC[index]]:
                    prepSeq = [1, 2, k]
                    return [True, prepSeq]
            return [False, [[]]]

        # aligns edge, if corner has wrong rotation but right position
        elif ((currentIndDataEdgP[1] == 2) and (currentIndDataCorP[1] == 0)) and \
             (blockCmpP[indC[index]] == config.solvedBlockCmp[indC[index]]):
            for k in range(3):
                simBlock = RBX_Cube.simMove(1, 2, k, block)
                if (simBlock[indEUpper[index][0]] == config.solvedBlock[indE[index]])\
                        or simBlock[indEUpper[index][1]] == config.solvedBlock[indE[index]]:
                    prepSeq = [1, 2, k]
                    return [True, prepSeq]
            return [False, [[]]]

        # return false, if the alignment dose not apply
        else:
            return [False, []]

    # moves pieces to top and then aligns them
    def attemptAdvanceAlignment(index, block, type, finalize=True):
        # type 0 for corner movement, 1 for edge movement

        data = getCurrentPieceInfo(index, block)
        currentIndDataCorP = data[2]
        currentIndDataEdgP = data[4]
        if type == 0:
            subject = currentIndDataCorP
        else:
            subject = currentIndDataEdgP

        if currentIndDataCorP[0] != currentIndDataEdgP[0]:
            prepSeq = [[0, subject[0], 2-subject[2]]]
        else:
            prepSeq = [[2, subject[2], 2-subject[0]]]
        simBlock = RBX_Cube.simMove(prepSeq[0][0], prepSeq[0][1], prepSeq[0][2], block)

        mag = 1
        for h in range(3):
            tempBlock = list(RBX_Cube.simMove(1, 2, h, simBlock))
            data = getCurrentPieceInfo(index, tempBlock)
            if (list(data[4])[prepSeq[0][0]] != prepSeq[0][1]) and (list(data[2])[prepSeq[0][0]] != prepSeq[0][1]):
                mag = h

        prepSeq.append([1, 2, mag])
        prepSeq.append([prepSeq[0][0], prepSeq[0][1], 2 - prepSeq[0][2]])
        simBlock = RBX_Cube.simMove(1, 2, mag, simBlock)

        if finalize:
            results = attemptBasicAlignment(index, simBlock)
            if results[0]:
                prepSeq.append(results[1])

        return prepSeq

    # puts the block into a state were its compatible with the standard algorithm's
    def prepBlock(index):

        prepSeq = []

        # a basic alignment is attempted
        results = attemptBasicAlignment(index, block)
        if results[0] or (results[1] == [[]]):
            prepSeq.append(results[1])

        # ignores all case 6 situations
        elif (currentIndEdg == indE[index]) and (currentIndCor == indC[index]):
            pass

        # aligns edge, if corner has wrong position and rotation
        elif (currentIndDataEdg[1] == 2) and (currentIndDataCor[1] == 0):
            prepSeq = attemptAdvanceAlignment(index, block, 0)

        # moves edge to top, if has the wrong position
        elif (currentIndDataEdg[1] == 1) and (currentIndDataCor[1] == 2):
            prepSeq = attemptAdvanceAlignment(index, block, 1)

        # moves both to top
        elif (currentIndDataEdg[1] == 1) and (currentIndDataCor[1] == 0):
            seq1 = attemptAdvanceAlignment(index, block, 0, False)
            seq2 = (attemptAdvanceAlignment(index, block, 1, False))
            if seq1 == seq2:
                prepSeq = seq1
            else:
                prepSeq = [seq1[0], seq1[1], seq1[2], seq2[0], seq2[1], seq2[2]]
            simBlock = block
            for h in range(len(prepSeq)):
                simBlock = RBX_Cube.simMove(prepSeq[h][0], prepSeq[h][1], prepSeq[h][2], simBlock)
            results = attemptBasicAlignment(index, simBlock)
            if results[0]:
                prepSeq.append(results[1])

        # other invalid forms (should be none (i hope))
        else:
            print("PREPMOVE FAIL")
            print(f"block {block}")


        # sims prepSeq, and sends it to be evaluated
        if (prepSeq != [[]]) and prepSeq and (prepSeq != [[[]]]):
            tempBlock = block
            for h in range(len(prepSeq)):
                #print(f"len {len(prepSeq)} h-{h}")
                tempBlock = RBX_Cube.simMove(prepSeq[h][0], prepSeq[h][1], prepSeq[h][2], tempBlock)
            return [tempBlock, prepSeq]
        else:
            return [block, prepSeq]

    # gets basic vars
    data = getCurrentPieceInfo(mainIndex, block)
    currentIndCor = data[1]
    currentIndDataCor = data[2]
    currentIndEdg = data[3]
    currentIndDataEdg = data[4]

    # ignores solves inds
    if (block[indC[mainIndex]] == config.solvedBlock[indC[mainIndex]]) and \
       (block[indE[mainIndex]] == config.solvedBlock[indE[mainIndex]]):
        return [config.block, [[]]]

    # gets prepMove
    results = prepBlock(index=mainIndex)
    mainBlock = results[0]
    prepSeq = []
    modifiedBlock = block
    if mainBlock != block:
        prepSeq = results[1]

        # gets block after prepSeq
        for j in range(len(prepSeq)):
            modifiedBlock = RBX_Cube.simMove(prepSeq[j][0], prepSeq[j][1], prepSeq[j][2], modifiedBlock)

    # gets pattern number
    data = getCurrentPieceInfo(mainIndex, modifiedBlock)
    newData = [data[1], modifiedBlock[data[1]], data[3], modifiedBlock[data[3]]]
    patternInd = config.F2LPAT[mainIndex].index(newData)


    # finds seq
    oldBlock = list(mainBlock)
    mainSeq = config.F2LSEQ[mainIndex][patternInd]
    if mainSeq != [-1, -1, -1]:
        # sims the seq
        for h in range(len(mainSeq)):
            mainBlock = RBX_Cube.simMove(mainSeq[h][0], mainSeq[h][1], mainSeq[h][2], mainBlock)
        # vets block
        if (mainBlock[indC[mainIndex]] == config.solvedBlock[indC[mainIndex]]) and (mainBlock[indE[mainIndex]] == config.solvedBlock[indE[
            mainIndex]]):
            passed = True
        else:
            passed = False
    else:
        passed = False

    # assembles final seq
    if passed:
        finalSeq = prepSeq + mainSeq
        #print(f"PASSED IN MAIN with len {len(finalSeq)}")
        return [mainBlock, finalSeq]
    else:
        print(f"FAILED IN MAIN with final block {oldBlock} pattId {patternInd} prepSeq {prepSeq} mainSeq {mainSeq} ind {mainIndex}")
        return [config.block, []]

# solves the first two layers (step 2)
def solveF2L():
    print("-------- SOLVING F2L ----------------")
    for g in range(4):

        seqs = []
        scores = []

        for i in range(4):
            #print(f"-------- running index {i} --------")
            score = 0
            results = findF2LSeqs(config.block, i)
            seqs.append(results[1])
            if results[1] and (results[1][0] != []) and (results[1][0] != []):
                score += len(results[1])
                for j in range(4):
                    results2 = findF2LSeqs(results[0], j)
                    if results2[1]:
                        score += 2*len(results2[1])
                    else:
                        score += 50
            else:
                score = 10000000
            scores.append(score)

        #print statements
        """
        for i in range(4):
            print(f"seq {seqs[i]} score {scores[i]}")
        """

        maxScoreInd = scores.index(sorted(scores)[0])
        bestSeq = list(seqs[maxScoreInd])
        #print(f"best seq {seqs[maxScoreInd]}")

        if bestSeq and (bestSeq != [[]]):
            for i in range(len(bestSeq)):
                RBX_Cube.cycle(bestSeq[i][0], bestSeq[i][1], bestSeq[i][2])
    print(colored("SOLVED (woo)", "green"))

# orientates the last layer (step 3)
def solveOLL():

    print("-------- SOLVING OLL ----------------")

    # gets pattern
    def getPatternData(block=config.block):
        pattern = [block[18][0], block[21][0], block[24][0],
                   block[24][2], block[25][1], block[26][2],
                   block[26][0], block[23][0], block[20][0],
                   block[20][2], block[19][1], block[18][2],
                   block[18][1], block[19][0], block[20][1],
                   block[21][1], block[22][0], block[23][1],
                   block[24][1], block[25][0], block[26][1]]
        for i in range(len(pattern)):
            if pattern[i] != 3:
                pattern[i] = -1
        return list(pattern)

    # ignores solved pats
    pattern = getPatternData()
    if pattern == [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3]:
        print("SOLVED (woo)")
        return [[-2, -2, -2]]

    # finds prep move and main seq
    passed = False
    holderBlock = config.block
    for i in range(4):
        pattern = getPatternData(holderBlock)
        if pattern in config.OLLPAT:
            ind = config.OLLPAT.index(pattern)
            seq = config.OLLSEQ[ind]
            prepMove = [1, 2, i-1]
            passed = True
            break
        holderBlock = RBX_Cube.simMove(1, 2, 0, holderBlock)

    # runs the seq
    if passed:
        if -1 not in prepMove:
            RBX_Cube.cycle(prepMove[0], prepMove[1], prepMove[2])
        for i in range(len(seq)):
            RBX_Cube.cycle(seq[i][0], seq[i][1], seq[i][2])
        print(colored("SOLVED (woo)", "green"))
    else:
        print(f"\n \n \n \n FAILED IN OLL with \n  {config.block} \n \n \n")

# permutates the last layer (step 4)
def solvePLL():

    # gets the pattern with block
    def getPatternData(block):

        pattern = []
        solvedPat = [882, 257, 1553, 881, 256, 1552, 962, 337, 1633]
        direction = [[2, 6, 8], [5, 7, 3], [8, 6, 0], [1, 5, 7], [], [7, 3, 1], [0, 2, 8], [3, 1, 5], [6, 0, 2]]
        blockCmp = compressBlock(block)
        for i in range(9):
            idealIndex = solvedPat.index(blockCmp[i + 18])
            if idealIndex not in direction[i]:
                pattern.append(-1)
            else:
                pattern.append(idealIndex)
        return pattern

    print("-------- SOLVING PLL ----------------")
    # gets the patterns for all 4 rotations of the top layer
    patterns = []
    weights = []
    baseBlock = config.block

    # gets all patterns

    for i in range(4):

        # ignores solved blocks
        if baseBlock == config.solvedBlock:
            if i != 0:
                RBX_Cube.cycle(1, 2, i - 1)
            print("100% SOLVE (WOO)")
            return [[-2, -2, -2]]

        # evaluates baseBlock patterns
        solves = 0
        patterns.append(getPatternData(baseBlock))
        for j in range(len(patterns[i])):
            if patterns[i][j] == -1:
                solves += 1
        weights.append(solves)
        baseBlock = list(RBX_Cube.simMove(1, 2, 0, baseBlock))
    #print(patterns)

    # gets all valid patterns
    pointers = []
    rotationInds = [2, 5, 8, 1, 4, 7, 0, 3, 6]
    for i in range(len(patterns)):
        pattern = patterns[i]
        for j in range(4):
            #print(f" {i} {j} {pattern}")
            if pattern in config.PLLPAT:
                pointers.append([j, config.PLLPAT.index(pattern)])
                #return pointers
                break
            else:
                pattern = [pattern[6], pattern[3], pattern[0], pattern[7], pattern[4], pattern[1], pattern[8],
                           pattern[5], pattern[2]]
                for k in range(len(pattern)):
                    if pattern[k] != -1:
                        pattern[k] = rotationInds[pattern[k]]
        pointers.append([-1, -1])
    #print(pointers)

    # get shortest valid seq
    lengths = []
    for i in range(len(pointers)):
        if -1 in pointers[i]:
            lengths.append(100)
            continue
        seq = config.PLLSEQ[pointers[i][0]][pointers[i][1]]
        lengths.append(len(seq))
    patternInd = lengths.index(sorted(lengths)[0])
    finalSeq = config.PLLSEQ[pointers[patternInd][0]][pointers[patternInd][1]]
    prepMove = [1, 2, patternInd-1]
    #print(lengths)

    #print(f"{finalSeq}")
    tempBlock = list(config.block)
    if -1 not in prepMove:
        RBX_Cube.cycle(1, 2, prepMove[2])
    for i in range(len(finalSeq)):
        RBX_Cube.cycle(finalSeq[i][0], finalSeq[i][1], finalSeq[i][2])
    if config.block == config.solvedBlock:
        print(colored("100% SOLVED (woo)", "green"))
    else:
        print("FAILED")
        print(f" \n \n {pointers[patternInd][0]} {pointers[patternInd][1]} \n {pattern} {finalSeq} {prepMove} {tempBlock} \n \n \n \n \n ")

# formats the final seq to comply with physical constraints
def finalizeSeq():

    # rearranges move to reflect current rotation
    def rotateMove(move, rotationFactor):

        # ignore 0-rotation
        seed = move
        if rotationFactor == 0:
            return move

        # ignore same axis rotation
        if (rotationFactor >= 1) and (rotationFactor <= 3) and (move[0] == 0):
            return move
        if (rotationFactor >= 4) and (rotationFactor <= 6) and (move[0] == 1):
            return move
        if (rotationFactor >= 7) and (rotationFactor <= 9) and (move[0] == 2):
            return move

        # get invert factor
        invertFactor = [3, 2, 1][int((rotationFactor - 1) / 3)]

        # main conversion method1
        if (rotationFactor == 5) or (rotationFactor == 2) or (rotationFactor == 8):
            move = [move[0], 2 - move[1], 2 - move[2]]

        # main conversion method2
        elif ((rotationFactor == 4) and (move[0] == 0)) or ((rotationFactor == 6) and (move[0] == 2)) or \
                ((rotationFactor == 3) and (move[0] == 1)) or ((rotationFactor == 1) and (move[0] == 2)):
            move = [invertFactor - move[0], move[1], 2 - move[2]]

        # main conversion method3
        elif ((rotationFactor == 7) and (move[0] == 0)) or ((rotationFactor == 9) and (move[0] == 1)):
            move = [invertFactor - move[0], 2 - move[1], 2 - move[2]]

        # main conversion method4
        elif ((rotationFactor == 9) and (move[0] == 0)) or ((rotationFactor == 7) and (move[0] == 1)):
            move = [invertFactor - move[0], move[1], move[2]]

        # main conversion method5
        else:
            move = [invertFactor - move[0], 2 - move[1], move[2]]

        # print(f" before {seed} after {move} {invertFactor} {rotationFactor}")
        return move

    # finds substitute moves and rotations
    tempSeq = []
    #print(config.moveSequence)
    for i in range(len(config.moveSequence)):
        if config.moveSequence[i][1] == 1:
            newSeq = []
            rotVal = [[], [0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 2], [2, 1], [2, 0]].index(
                [config.moveSequence[i][0], config.moveSequence[i][2]])
            newSeq.append([-rotVal, -rotVal, -rotVal])
            newSeq.append([config.moveSequence[i][0], 0, 2 - config.moveSequence[i][2]])
            newSeq.append([config.moveSequence[i][0], 2, 2 - config.moveSequence[i][2]])
            for j in range(len(newSeq)):
                tempSeq.append(newSeq[j])
        else:
            tempSeq.append(config.moveSequence[i])

    # divides the seq into smaller segments with different rotations
    dividedSeq = []
    leftEndIndex = 0
    for i in range(len(tempSeq)):
        if (tempSeq[i][0] < 0) or (i == len(tempSeq) - 1):
            dividedSeq.append([])
            for j in range(i - leftEndIndex):
                dividedSeq[len(dividedSeq) - 1].append(tempSeq[j + leftEndIndex])
            leftEndIndex = i
    dividedSeq[len(dividedSeq) - 1].append(config.moveSequence[len(config.moveSequence) - 1])

    # applies the rotations as the accumulated
    stackedRotations = []
    # repeat for each seq in dividedSeq
    for i in range(len(dividedSeq)):
        if i != 0:

            #print(f"\nactive seqseq {dividedSeq[i]}")
            rotVal = [[], [0, 0], [0, 1], [0, 2], [1, 0], [1, 1], [1, 2], [2, 2], [2, 1], [2, 0]].index([dividedSeq[i][1][0], dividedSeq[i][1][2]])
            dividedSeq[i][0] = [-rotVal, -rotVal, -rotVal]
            stackedRotations.append(rotVal)

            # repeat for all accumulated rotations
            for j in range(len(stackedRotations)):
                rotationFactor = stackedRotations[len(stackedRotations) - (j + 1)]

                # applies the various rotations to the divided seq
                newDividedSeqSeq = []
                for k in range(len(dividedSeq[i])):
                    if k != 0:
                        newDividedSeqSeq.append(rotateMove(dividedSeq[i][k], abs(rotationFactor)))
                    else:
                        newDividedSeqSeq.append(dividedSeq[i][0])
                dividedSeq[i] = list(newDividedSeqSeq)
                #print(f" rf {rotationFactor} {newDividedSeqSeq}")

    # finalizes the seq
    seq = []
    for i in range(len(dividedSeq)):
        for j in range(len(dividedSeq[i])):
            if dividedSeq[i][j][0] >= 0:
                seq.append(dividedSeq[i][j])

    # validates the seq
    holderBlock = config.seedBlock
    for i in range(len(seq)):
        holderBlock = RBX_Cube.simMove(seq[i][0], seq[i][1], seq[i][2], holderBlock)
    config.block = holderBlock
    RBX_Cube.render()
    displayBlock = config.getDisplayBlock(holderBlock)
    passed = True
    for i in range(len(displayBlock)):
        for j in range(len(displayBlock[i])):
            if displayBlock[i][j] != displayBlock[i][0]:
                passed = False
    if passed:
        print(f"\nFINAL SEQ (the magic list of numbers) {seq}")
        RBX_Sender.updateMoves(moveSeq=seq, overwrite=True)
        print(colored("Prepared to execute SEQ", "cyan"))
        #RBX_Sender.sendSeq()
    else:
        print(f"\nFAILED WITH {seq}")
    return seq

# main loop
def cmd():

    #debug tool
    def move(seq):
        for i in range(len(seq)):
            RBX_Cube.cycle(seq[i][0], seq[i][1], seq[i][2])

    seq = []

    print("\nVALID COMMANDS "
          "\n"
          "\n--- VIRTUAL MOVES ---"
          "\nto cycle an individual move enter the axis of rotation (x->0, y->1, z->2), "
          "\nthe value along the axis (0, 1, 2) and the angle (0->90,1->180,2->270), Examples '000' '120' "
          "\nmove 'list' - runs all moves in the defined list "
          "\n"
          "\n--- SOLVE COMPONENTS ---"
          "\nrun - shuffles, solves, gets seq, saves seq "
          "\nshuf - randomly shuffles the cube "
          "\nsolve - solves the whole cube "
          "\nsolveWCC - completes the first step, runs solveWhiteCross() & solveCenters() "
          "\nsolveF2L - completes the second step, runs solveF2L()"
          "\nsolveOLL - completes the third step, runs solveOLL()"
          "\nsolvePLL - completes the fourth step, runs solvePLL"
          "\ngetSeq - runs finalizeSeq() to optimize final list of moves"
          "\n"
          "\n--- DATA GETTERS & SETTERS ---"
          "\ngetBlock - returns the current block (config.block)"
          "\nsetBlock 'block' - sets config.block to the defined block"
          "\n"
          "\n--- CONTROL ---"
          "\nsaveBlock - appends 'CubeData//Block.txt' with config.block "
          "\nclearMoves - empties 'CubeData//Moves.txt' "
          "\noverwriteMoves - replaces CubeData//Moves.txt with seq"
          "\nexeMoves - tells the machine to execute all moves in 'CubeData//Moves.txt'"
          "\nexeMove - tells to machine to execute a specific move "
          "\n")

    while True:

        RBX_Cube.render()
        print("")
        x = input(colored("enter command: ", "cyan"))

        if x == "shuf":
            RBX_Cube.shuffle()
            print(f"SEED BLOCK {config.block}")

        # sender commands
        elif x == "saveBlock":
            RBX_Sender.updateBlock()

        elif x == "updateMoves":
            RBX_Sender.updateMoves(moveSeq=seq)

        elif x == "clearMoves":
            RBX_Sender.updateMoves(clear=True)

        elif x == "overwriteMoves":
            RBX_Sender.updateMoves(moveSeq=seq, overwrite=True)

        elif x == "exeMoves":
            RBX_Sender.sendSeq()

        elif x == "exeMove":
            RBX_Sender.sendSingleMove()

        # solve commands
        elif x == "solve":
            solveWhiteCross()
            solveCenters()
            solveF2L()
            solveOLL()
            solvePLL()
            seq = finalizeSeq()

        elif x == "run":
            RBX_Cube.shuffle()
            print(f"SEED BLOCK {config.seedBlock}")
            time.sleep(1)
            RBX_Cube.render()
            solveWhiteCross()
            solveCenters()
            solveF2L()
            solveOLL()
            solvePLL()
            seq = finalizeSeq()

        elif x == "solveF2L":
            solveF2L()

        elif x == "solveOLL":
            solveOLL()

        elif x == "solvePLL":
            solvePLL()

        elif x == "solveWCC":
            solveWhiteCross()
            solveCenters()

        elif x == "getBlock":
            print(config.block)

        elif "setBlock" in x:
            config.block = ast.literal_eval(x[9:])
            RBX_Cube.render()

        elif "move" in x:
            move(ast.literal_eval(x[5:]))

        elif x == "getSeq":
            seq = finalizeSeq()


        else:
            try:
                RBX_Cube.cycle(int(x[0]), int(x[1]), int(x[2]))
            except:
                print("INVALID")
if not config.N0_RENDER:
    cmd()
RBX_Sender.updateBlock()

