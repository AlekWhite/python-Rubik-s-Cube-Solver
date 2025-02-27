"""
Assists in the conversation between standard rubixCube notation and
the notation used by this program
"""

import ast

# constant
HEADERS = "ZzRrFfUuLlBbDdzZyYxXMuEu"
INPUT_FILE = "PLLrawmoves.txt"
OUTPUT_FILE = "PLLseqs.txt"

# handles the 4 different reference frames
def moveReferenceFrame(referenceFrame, move):
    if referenceFrame == 1:
        move = [2 - move[0], move[1], 2 - move[2]]
    elif referenceFrame == 2:
        move = [2 - move[0], 2 - move[1], move[2]]
    elif referenceFrame == 3:
        move = [move[0], 2 - move[1], 2 - move[2]]
    print(f"move after reff {move} {referenceFrame}")
    return move

# rearranges move to reflect current rotation
def rotateMove(move, rotationFactor):

    seed = move

    # ignore 0-rotation
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
    invertFactor = [3, 2, 1][int((rotationFactor-1)/3)]

    # moves with a mag of one
    if (rotationFactor == 5) or (rotationFactor == 2) or (rotationFactor == 8):
        move = [move[0], 2 - move[1], 2 - move[2]]

    # main conversion one
    elif ((rotationFactor == 4) and (move[0] == 2)) or ((rotationFactor == 6) and (move[0] == 0)) or \
         ((rotationFactor == 3) and (move[0] == 2)) or ((rotationFactor == 1) and (move[0] == 1)) or \
         ((rotationFactor == 7) and (move[0] == 1)) or ((rotationFactor == 9) and (move[0] == 0)):
        move = [invertFactor - move[0], move[1], 2 - move[2]]

    # invert all
    elif ((rotationFactor == 7) and (move[0] == 0)) or ((rotationFactor == 9) and (move[0] == 1)):
        move = [invertFactor - move[0], 2 - move[1], 2 - move[2]]

    # main conversion two
    else:
        move = [invertFactor - move[0], 2 - move[1], move[2]]


    #print(f" before {seed} after {move} {invertFactor} {rotationFactor}")
    return move

# main conversion method
def convert(referenceFrameHolder, seq):

    # defines each basic move in the default reference frame
    #mainArray= [[front F], [Right R], [Left L ], [Back B ], [Upper U], [Down  D], [Mid   M], [MidE  E]]
    mainArray = [[2, 2, 2], [0, 2, 0], [0, 0, 2], [2, 0, 0], [1, 2, 0], [1, 0, 2], [0, 0, 0], [1, 2, 0]]

    # assembles moves list
    holderSeq = []
    seqNew = []
    for i in range(len(seq)):
        if seq[i] in HEADERS:
            seqNew.append(seq[i])
        elif (seq[i] != " ") and (seq[i] != ")") and (seq[i] != "(") and (seq[i] != "[") and (seq[i] != "]") and (seq[i] != "{") and (seq[i] != "}"):
            seqNew[len(seqNew) - 1] += seq[i]
    seq = seqNew

    # handles general reference frame
    rotation = [8, 2, 6, 0].index(referenceFrameHolder)+10
    if rotation != 0:
        holderSeq.append([-rotation, -rotation, -rotation])

    # turns letters into numbers
    for i in range(len(seq)):

        # handles rotations
        rotationVals = ["*", "x", "x2", "x'", "y", "y2", "y'", "z", "z2", "z'"]
        if seq[i][:2] in rotationVals:
            rotationStr = seq[i][:2]
            if seq[i - 1] in rotationVals:
                rotationStr = seq[i - 1]
            if seq[i + 1] in rotationVals:
                rotationStr = seq[i + 1]
            move = [-rotationVals.index(rotationStr), -rotationVals.index(rotationStr), -rotationVals.index(rotationStr)]
            print(f"rotationVal {rotationVals.index(rotationStr)} given {seq[i][:2]}")
            holderSeq.append(list(move))
            continue

        # main direction axis/val
        if seq[i][0] in "Ff":
            move = list(mainArray[0])
        elif seq[i][0] in "Rr":
            move = list(mainArray[1])
        elif seq[i][0] in "Ll":
            move = list(mainArray[2])
        elif seq[i][0] in "Bb":
            move = list(mainArray[3])
        elif seq[i][0] in "Uu":
            move = list(mainArray[4])
        elif seq[i][0] in "Dd":
            move = list(mainArray[5])
        elif seq[i][0] in "Mm":
            move = list(mainArray[6])
        elif seq[i][0] in "Ee":
            move = list(mainArray[7])

        # prime rule
        if "'" in seq[i]:
            move[2] = 2 - move[2]
        # double prime and 2 rule
        if "2" in seq[i]:
            move[2] = 1

        # double move junk
        if (seq[i][0].islower()) and (seq[i][0] not in "xyz"):
            move = [move[0], 2-move[1], 2-move[2]]
            rotationVal = -(1 + 3*move[0] + (2 - move[2]))
            holderSeq.append(list(move))
            holderSeq.append(list([rotationVal, rotationVal, rotationVal]))
            print(f"{seq[i]} {move} {[rotationVal, rotationVal, rotationVal]}")

        # middle move junk
        elif (seq[i][0] in "Mm") or (seq[i][0] in "Ee"):
            holderSeq.append(list(move))
            holderSeq.append(list([move[0], 2-move[1], move[2]]))
            if seq[i][0] in "Mm":
                rotationVal = -(1 + 3 * move[0] + (2 - move[2]))
            else:
                rotationVal = -(1 + 3 * move[0] + (2 - move[2]))
            holderSeq.append(list([rotationVal, rotationVal, rotationVal]))
            print(f"{seq[i]} {move} {[rotationVal, rotationVal, rotationVal]}")

        # normal moves
        else:
            holderSeq.append(list(move))
            print(f"{seq[i]} {move}")

    print(f"holderSeq {holderSeq}")

    # applies the various rotations and reference frames

    # main way of processing holder seq
    mainSeq = []
    firstPass = True
    tempSeq = list(holderSeq)
    for i in range(len(holderSeq)):
        # applies rotation
        if holderSeq[i][0] < 0:
            for j in range(len(holderSeq)):
                if (j > i) and (holderSeq[j][0] >= 0):
                    if firstPass:
                        holderSeq[j] = moveReferenceFrame(abs(holderSeq[i][0])-10, holderSeq[j])
                    else:
                        print(f"shipping {holderSeq[j]} {j}")
                        holderSeq[j] = rotateMove(holderSeq[j], abs(holderSeq[i][0]))
        else:
            mainSeq.append(holderSeq[i])
        firstPass = False
    holderSeq = list(tempSeq)

    """ all of this is for edge cases :) """
    # applies reference frame
    for i in range(len(holderSeq)):
        holderSeq[i] = moveReferenceFrame(abs(holderSeq[0][0]) - 10, holderSeq[i])
    holderSeq.remove(holderSeq[0])

    # segments the seq based on rotation
    rotationSeq = []
    segmentedSeq = [[]]
    seqCount = 0
    for i in range(len(holderSeq)):
        if holderSeq[i][0] < 0:
            seqCount += 1
            segmentedSeq.append([])
            rotationSeq.append(holderSeq[i])
        else:
            segmentedSeq[seqCount].append(holderSeq[i])

    # finalizes main seq
    if (len(segmentedSeq) == 3) and ([] not in segmentedSeq):
        # yes
        print(f"seq {segmentedSeq}")
        print(f"rot {rotationSeq}")
        mainSeq = []
        tempSeq = []
        for i in range(len(segmentedSeq[0])):
            mainSeq.append(segmentedSeq[0][i])
        for i in range(len(segmentedSeq[1])):
            mainSeq.append(rotateMove(segmentedSeq[1][i], abs(rotationSeq[0][0])))
        for i in range(len(segmentedSeq[2])):
            tempSeq.append(rotateMove(segmentedSeq[2][i], abs(rotationSeq[1][0])))
        print(f"temp {tempSeq}")
        for i in range(len(segmentedSeq[2])):
            mainSeq.append(rotateMove(tempSeq[i], abs(rotationSeq[0][0])))
        return mainSeq
    else:
        return mainSeq

# runs the conversion on all patterns in "INPUT_FILE", returns them in "OUTPUT_FILE"
def apply():
    # gets moves from "rawMoves.txt"
    with open(INPUT_FILE, "r") as file:
        rawMoves = file.readlines()
    mainSeq = [[]]
    for i in range(len(rawMoves)):
        if rawMoves[i] != "\n":
            mainSeq[len(mainSeq)-1].append(rawMoves[i])
        elif len(rawMoves[i]) != 0:
            mainSeq.append([])

    for i in range(len(mainSeq)):
        print(mainSeq[i])

    # runs the conversion
    ref = [0, 2, 6, 8]
    rot = [0, 4, 5, 6]
    dataString = ""
    for i in range(4):
        totalMoves = []
        for k in range(len(mainSeq)):
            print(f"running {mainSeq[k][0][1:]} ref {ref[i]} index {k}")

            # temp         ref[i]
            moves = convert(8, str(mainSeq[k][0][1:]))
            fin = []
            for j in range(len(moves)):
                fin.append(rotateMove(moves[j], rot[i]))
            totalMoves.append(fin)


            print(fin)
            print("\n")
        dataString += str(totalMoves) + "\n"

    print("\n")
    result = convert(referenceFrameHolderINP, seqINP)
    print(f"manual seq --> {result}")
    try:
        print(f"manual seq ind {totalMoves.index(result)}")
    except:
        print("seq not found in converted seq's")

    with open(OUTPUT_FILE, 'r+') as file:
        file.write(dataString)

# manual mode
"""
referenceFrameHolderINP = int(input("enter reff frame (0,2,6,8)"))
seqINP = list(input("enter standard notation"))
print(convert(referenceFrameHolderINP, seqINP))
"""
#apply()