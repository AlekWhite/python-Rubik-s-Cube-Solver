import config
import RBX_Cube
allpats = []

# compressed color data to be independent of rotation
def compressBlock(activeBlock):
    compressedBlock = []

    for i in range(len(activeBlock)):
        compressedData = 0
        for j in range(len(activeBlock[i])):
            compressedData += pow((activeBlock[i][j] + 1), 4)
        compressedBlock.append(compressedData)

    return compressedBlock

def getPatternData(block=config.block):

    pattern = []
    solvedPat = [882, 257, 1553, 881, 256, 1552, 962, 337, 1633]
    direction = [[2, 6, 8], [5, 7, 3], [8, 6, 0], [1, 5, 7], [], [7, 3, 1], [0, 2, 8], [3, 1, 5], [6, 0, 2]]
    blockCmp = compressBlock(block)
    for i in range(9):
        idealIndex = solvedPat.index(blockCmp[i+18])
        if idealIndex not in direction[i]:
            pattern.append(-1)
        else:
            pattern.append(direction[i].index(idealIndex))
    return pattern

PLLPAT = [[8, -1, 0, -1, -1, -1, -1, -1, 2],[-1, -1, 8, -1, -1, -1, 2, -1, 6],[-1, -1, -1, 7, -1, 3, -1, 5, -1],[-1, -1, -1, 5, -1, 7, -1, 2, -1], [-1, 7, -1, 5, -1, 3, -1, 1, -1],[-1, -1, 8, 5, -1, 3, -1, -1, 2],[2, 3, 0, 1, -1, -1, -1, -1, -1],[-1, -1, 8, -1, -1, 7, -1, 5, 2],[8, 5, -1, -1, -1, 5, -1, -1, 0], [6, 5, 0, 1, -1, 3, 2, -1, -1], [6, 7, 0, 1, -1, -1, 2, 3, -1],[8, -1, -1, 7, -1, 3, 0, 5, 6], [6, 7, 0, 1, -1, -1, 2, 3, -1], [-1, -1, -1, 5, -1, 3, 8, -1, 6], [-1, 3, -1, 1, -1, 7, -1, 5, -1],[8, 3, -1, 1, -1, -1, -1, -1, 0],  [8, 7, -1, -1, -1, -1, -1, 1, 0], [-1, 7, 6, -1, -1, -1, 2, 1, -1], [6, -1, 8, -1, -1, -1, 0, -1, 2]]

def test3():

    for h in range(4):
        for i in range(len(testing.OLDPLLSEQ[h])):

            holderBlock = config.block
            for j in range(len(testing.OLDPLLSEQ[h][i])):
                holderBlock = RBX_Cube.simMove(testing.OLDPLLSEQ[h][i][j][0], testing.OLDPLLSEQ[h][i][j][1], testing.OLDPLLSEQ[h][i][j][2], holderBlock)
            if holderBlock == config.solvedBlock:
                inds = test2()
                print(inds)
                config.PLLSEQ[inds[0][0]][inds[0][1]] = testing.OLDPLLSEQ[h][i]
                break