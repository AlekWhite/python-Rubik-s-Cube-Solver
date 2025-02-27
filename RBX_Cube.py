"""
This file is concerned with modeling the rubix-cube in terms of usable lists and functions,
it also models how the cube moves, and runs the 2d view display.
"""

import random
import time
import tkinter as tk
import config
import RBX_Sender
from threading import Thread
from termcolor import colored


""" -------------- GUI -------------- """

# colors - green-0  white-1  blue-2   yellow-3   red-5   orange-4
colors = ["#00cc00", "#ffffff", "#0099ff", "#ffff00", "#fc8403", "#ff0000"]


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

# makes 2d view
renders = 0
def render():

    if config.N0_RENDER:
        return

    global renders

    for child in canvas.winfo_children():
        if (str(child)[len(str(child))-1] == 0 and renders == 1) or (str(child)[len(str(child))-1] == 0 and renders == 1):
            print(child)
            child.destroy()

    displayBlock = config.getDisplayBlock(config.block)
    for i in range(6):
        cords = [[150, 150, 150, 150, 65, 235], [75, 160, 245, 330, 160, 160]]
        for i1 in range(9):
            F = tk.Frame(canvas, bg=colors[displayBlock[i][i1]], width=25, height=25, name="2d-view-frame" + str(i1) + str(i) + "num" + str(renders))
            if i1 < 3:
                F.place(x=cords[0][i] + 47 + i1*25, y=cords[1][i])
            elif i1 < 6:
                F.place(x=cords[0][i] + 47 + (i1-3)*25, y=cords[1][i] + 25)
            elif i1 < 9:
                F.place(x=cords[0][i] + 47 + (i1-6)*25, y=cords[1][i] + 50)

    renders += 1
    if renders == 2:
        renders = 0

# shows testing stats in real time
def displayStats(data):

    text = [" - totalTest", " - reRuns%", " - avg totalCycles", " - avg F2LCycles", " - avg crossCycles", " - avg time"]

    for child in canvas.winfo_children():
        child.destroy()

    for i in range(len(data)):
        L = tk.Label(canvas, width=30, height=1, bg="#262626", font=('Consolas', 12), text=str(data[i])+text[i], name="stats" + str(i))
        L.place(x=20, y=10+(30*i))

# starts gui thread
global canvas
threadGUI = Thread(target=GUIthread, args="1")
threadGUI.start()
time.sleep(0.1)
render()

""" ---------- Cube Management ---------- """

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

# moves segments of the cube
def cycle(axis, val, magnitude):
    if axis == -2:
        return
    config.cycles += 1
    config.moveSequence.append([axis, val, magnitude])
    newBlock = simMove(axis, val, magnitude, config.block)
    config.block = list(newBlock)
    render()
    config.inverseMove = [axis, val, 3-(1+magnitude)]
    if not config.N0_RENDER:
        print(colored("-------- cycled " + str(axis) + " " + str(val) + " " + str(magnitude) + " --------", "yellow"))

# completes a move and returns data
def simMove(axis, val, mag, baseBlock=config.block):

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

    # repeat the rotation process based on desired outcome
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

# simulates how colors change with a move
def simColorRotation(axis, mag, colors, type):

    # type 0 -> corner, 1 -> edge
    newColors = colors

    # repeat based on mag
    for i in range(mag+1):

        # corner rotation
        if type == 0:
            if axis == 0:
                newColors = [newColors[0], newColors[2], newColors[1]]
            if axis == 1:
                newColors = [newColors[2], newColors[1], newColors[0]]
            if axis == 2:
                newColors = [newColors[1], newColors[0], newColors[2]]

        # edge rotation
        if type == 1:
            newColors = [newColors[1], newColors[0]]

    return newColors

# simulates how position changes with a move
def simPositionalChange(axis, val, mag, baseBlock=config.block):
    # finds critical points
    criticalPoints = []
    for i in range(len(baseBlock)):
        if getIndexData(i)[axis] == val:
            criticalPoints.append(i)
    movedPOS = list(criticalPoints)

    # repeat the rotation process based on desired outcome
    for i in range(mag + 1):
        # rotates position
        movedPOS = [movedPOS[6], movedPOS[3], movedPOS[0], movedPOS[7], movedPOS[4], movedPOS[1], movedPOS[8],
                    movedPOS[5], movedPOS[2]]
    return movedPOS

# randomizes cube
def shuffle():
    seq = []
    for i in range(random.randint(45, 50)):
        val = random.randint(0, 2)
        while val == 1:
            val = random.randint(0, 2)
        seq.append([random.randint(0, 2), val, random.randint(0, 2)])
        cycle(seq[i][0], seq[i][1], seq[i][2])
    print("------------ completed shuffle ------------")
    config.seedBlock = config.block
    render()
    RBX_Sender.updateMoves(moveSeq=seq, overwrite=True)
    print(colored("Prepared to execute Shuffle", "cyan"))
    RBX_Sender.sendSeq()
