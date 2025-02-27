"""
This file is used for large scale testing and collects data regarding the
efficiency and effectiveness of different functions
"""
import ast
import RBX_Cube
import RBX_Solve
import time
import config
from threading import Thread

TEST_NUM = 50000

# gui stuff
def getsStats(args):
    while True:
        # gets data from file
        fullData = []
        with open("tempTestngData.txt", "r+") as file:
            lines = file.readlines()
            totalTests = float(lines[0])
            for i in range(len(lines)):
                if i == 0:
                    totalTests = float(lines[0])
                    fullData.append(totalTests)
                elif i != 1:
                    fullData.append(round((float(lines[i]) / totalTests), 4))
                else:
                    fullData.append(round(((float(lines[i]) / totalTests) * 100), 4))
        RBX_Cube.displayStats(fullData)
        time.sleep(5)
threadGUI = Thread(target=getsStats, args="1")

# main loop
def mainTestingLoop(args):
    failed = 0
    for i in range(TEST_NUM):

        # shuffles cube
        RBX_Cube.shuffle()

        # resets stat vars
        seedBlock = list(config.block)
        config.reRuns = 0
        config.cycles = 0

        # starts timer
        start = time.monotonic()

        # solves white cross
        RBX_Solve.solveWhiteCross()
        RBX_Solve.solveCenters()

        # gets data on moves needed to solve white-cross
        config.crossCycles = config.cycles
        config.cycles = 0

        # solves f2l and gets data
        RBX_Solve.solveF2L()
        config.f2lCycles = config.cycles
        config.cycles = 0

        # solves OLL
        RBX_Solve.solveOLL()

        # solves PLL
        RBX_Solve.solvePLL()

        # gets final seq
        RBX_Solve.finalizeSeq()

        # stops timer
        end = time.monotonic() - start

        # categorizes blocks
        if not validate(config.block):
            print(f"\n \n \n  FAILED \n {seedBlock} \n \n \n ")
            time.sleep(60*10)
        # writes data to file
        fullData = [1, config.reRuns, config.f2lCycles + config.crossCycles + config.cycles, config.f2lCycles, config.crossCycles, end]
        newlines = ""
        with open("tempTestngData.txt", "r+") as file:
            lines = file.readlines()
            for k in range(6):
                newlines += str((float(lines[k]) + fullData[k])) + "\n"
            #print(newlines)
        with open("tempTestngData.txt", "r+") as file:
            file.write(str(newlines))

# ensues the block was solved
def validate(block):
    displayBlock = config.getDisplayBlock(block)
    passed = True
    for i in range(len(displayBlock)):
        for j in range(len(displayBlock[i])):
            if displayBlock[i][j] != displayBlock[i][0]:
                passed = False
    return passed

# starts threads
threadLoop = Thread(target=mainTestingLoop, args="1")
threadLoop.start()
time.sleep(5)
threadGUI.start()
