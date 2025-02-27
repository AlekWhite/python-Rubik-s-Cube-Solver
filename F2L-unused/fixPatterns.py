"""
fixed parts of the F2LSEQ list
"""

import config
import RBX_Cube
import ast

indC = [0, 2, 6, 8]
indE = [9, 11, 15, 17]


# compressed color data to be independent of rotation(from RBX_SOLVE.py)
def compressBlock(activeBlock):
    compressedBlock = []

    for i in range(len(activeBlock)):
        compressedData = 0
        for j in range(len(activeBlock[i])):
            compressedData += pow((activeBlock[i][j] + 1), 4)
        compressedBlock.append(compressedData)

    return compressedBlock

def fix(block, ref, seqInd, preSeq):

    # gets potential invalid seqs
    with open("F2Lsequences.txt", "r+") as file:
        mainSeqs = ast.literal_eval(file.readlines()[ref])
    invalidSeqs = []
    newSeqs = []
    for i in range(len(mainSeqs)):
        if ([1, 0, 0] in mainSeqs[i]) or ([1, 0, 1] in mainSeqs[i]) or ([1, 0, 2] in mainSeqs[i]):
            invalidSeqs.append(mainSeqs[i])
        else:
            newSeqs.append(mainSeqs[i])

    for h in range(len(invalidSeqs)):
        invalidSeq = invalidSeqs[h]

        # sims prepMove
        correctSeq = []
        simBlock = block
        if preSeq:
            for i in range(len(preSeq)):
                simBlock = RBX_Cube.simMove(preSeq[i][0], preSeq[i][1], preSeq[i][2], simBlock)

        # gets correct portion of invalidSeq
        for i in range(len(invalidSeq)):
            if (invalidSeq[i][0] == 1) and (invalidSeq[i][1] == 0):
                break
            correctSeq.append(invalidSeq[i])
        correctSeq.append([1, 2, invalidSeq[len(correctSeq)][2]])


        # sims correct portion of invalidSeq
        for i in range(len(correctSeq)):
            simBlock = RBX_Cube.simMove(correctSeq[i][0], correctSeq[i][1], correctSeq[i][2], simBlock)

        passed = False
        for i in range(len(newSeqs)):

            # sims potential solution
            testBlock = simBlock
            for j in range(len(newSeqs[i])):
                testBlock = RBX_Cube.simMove(newSeqs[i][j][0], newSeqs[i][j][1], newSeqs[i][j][2], testBlock)

            # vets block
            if (testBlock[indC[ref]] == config.solvedBlock[indC[ref]]) and (testBlock[indE[ref]] == config.solvedBlock[indE[ref]]):

                # appends correctSeq
                for k in range(len(newSeqs[i])):
                    correctSeq.append([newSeqs[i][k][0], newSeqs[i][k][1], newSeqs[i][k][2]])
                passed = True

        if passed:
            print(f"PASSED FIX {correctSeq}")
            config.F2LSEQ[ref][seqInd] = list(correctSeq)
            config.invalidPats[ref].remove(seqInd)
            break



