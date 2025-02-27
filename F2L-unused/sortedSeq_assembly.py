"""
Currently non functioning, this scrip was used to assemble
the "F2LSEQ" list in "config.py" based on the info in "pairs.txt" and "F2Lsequences.txt"
"""

import ast

mainList = []
for i in range(4):
    with open("patterns.txt", "r") as file:
        lines = file.readlines()
        patternList = ast.literal_eval(lines[i])

    with open("pairs.txt", "r") as file:
        lines = file.readlines()
        dataList = ast.literal_eval(lines[i])

    with open("F2Lsequences.txt", "r") as file:
        lines = file.readlines()
        seqList = ast.literal_eval(lines[i])

    patternInds = []
    sortedData = []
    sortedSeqs = []

    for j in range(len(dataList)):
        sortedData.append([])
        patternInds.append(dataList[j][0])

    patternInds = sorted(patternInds)
    for j in range(len(dataList)):
        sortedData[patternInds.index(dataList[j][0])] = dataList[j]

    for j in range(len(sortedData)):
        if sortedData[j]:
            if sortedData[j][1] != -1:
                print(list(seqList[sortedData[j][1]]))
                sortedSeqs.append(list(seqList[sortedData[j][1]]))
            else:
                sortedSeqs.append(list([-1, -1, -1]))

    """
    for j in range(len(sortedSeqs)):
        print(f"{sortedData[j]} {sortedSeqs[j]}")
    """
    mainList.append(sortedSeqs)
print(mainList)
