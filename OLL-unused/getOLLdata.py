import config, RBX_Cube, ast
allPats = []
mainPast = []
mainSeqs = []

# converts block to pattern
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

# sims every seq for a given pattern and records correct seq pattern combination
def testAllSeqs():
    passed = False

    pattern = getPatternData(config.block)
    patInd = config.OLLPAT.index(pattern)
    print(f"patternId {patInd} {pattern}")

    with open("../OLLsequences.txt", "r+") as file:
        lines = file.readlines()[3]
        seqs = (ast.literal_eval(lines))

    baseBlock = config.block
    for i in range(len(seqs)):
        holderBlock = baseBlock
        for k in range(len(seqs[i])):
            holderBlock = RBX_Cube.simMove(seqs[i][k][0], seqs[i][k][1], seqs[i][k][2], holderBlock)
        simedPat = getPatternData(holderBlock)
        if simedPat == [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 3, 3, 3, 3, 3, 3, 3, 3, 3]:
            print(f"PASSED {seqs[i]} {pattern} {patInd}")
            seq = seqs[i]
            passed = True
            break

    if (passed) and (pattern not in mainPats):
        mainPats.append(pattern)
        mainSeqs.append(seq)
    print(f"OLLpats {len(mainPats)} {mainPats}")
    print(f"OLLseqs {len(mainSeqs)} {mainSeqs}")


