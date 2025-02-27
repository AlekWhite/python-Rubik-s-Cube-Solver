"""
sends data from the the solver to the Arduino script
"""

import ast
import serial, time
import RBX_Cube
import config
from termcolor import colored


# https://create.arduino.cc/projecthub/ansh2919/serial-communication-between-python-and-arduino-e7cce0

#arduino = serial.Serial(port='COM4', baudrate=115200, timeout=.1)
arduino = None
key = [[0, 0], [2, 0], [0, 2], [2, 2], [1, 0], [1, 2]]

# puts config.block in "CubeData//Block.txt"
def updateBlock():
    """
    with open("CubeData//Block.txt", "a") as file:
        file.write(str(config.block) + "\n")"""
    print(colored("SAVED-BLOCK", "magenta"))

# modifies data in "CubeData//Moves.txt"
def updateMoves(moveSeq=None, overwrite=False, clear=False):

    # removes all data from "CubeData//Moves.txt"
    if overwrite or clear:
        with open("CubeData//Moves.txt", "w") as file:
            file.write("")
        print(colored("Removed all data from CubeData//Moves.txt", "magenta"))

    # appends "CubeData//Moves.txt" with moveSeq
    if moveSeq and (not clear):
        with open("CubeData//Moves.txt", "a") as file:
            for i in range(len(moveSeq)):
                file.write(str(moveSeq[i]) + "\n")
        print(colored(f"Appended data to CubeData//Moves.txt with", "magenta"))

# sends an int to the arduino
def sendToHardware(x):
    pass
    #arduino.write(bytes(str(x), 'utf-8'))
    #time.sleep(0.05)
    #data = arduino.readline()
    #print(f"SENT {data}")

# sends data from "CubeData//Moves.txt" to the Arduino script
def sendSeq():

    # gets moves from "CubeData//Moves.txt"
    seq = []
    with open("CubeData//Moves.txt", "r") as file:
        allData = file.readlines()
    for i in range(len(allData)):
        seq.append(ast.literal_eval(allData[i][:len(allData[i])-1]))
    #print(f"Data from CubeData//Moves.txt \n {seq}")

    # gets Arduino compatible seq
    ArduinoSeq = []
    for i in range(len(seq)):
        servoNum = key.index([seq[i][0], seq[i][1]]) + 10
        ArduinoSeq.append([servoNum, seq[i][2]])
    #print(f"Prepared to send \n {ArduinoSeq}")

    # buffers the seq while sending
    x = input(colored("Enter 'Y' to confirm: ", "cyan"))
    if x == "Y":
        print("\n")
        for i in range(len(ArduinoSeq)):
            sendToHardware(str(ArduinoSeq[i][0]))
            time.sleep(0.1)
            sendToHardware(str(ArduinoSeq[i][1]))
            time.sleep(0.5)
        updateBlock()
    else:
        print(colored("submission canceled", "red"))

# sends a single move to the Arduino script
def sendSingleMove():
    raw = input(colored("Enter Move: ", "cyan"))
    servoNum = key.index([int(raw[0]), int(raw[1])]) + 10
    print(f"Prepared to send \n {[servoNum, raw[2]]}")
    x = input(colored("enter 'Y' to confirm: ", "cyan"))
    if x == "Y":
        print("\n")
        sendToHardware(servoNum)
        time.sleep(0.1)
        sendToHardware(raw[2])
        RBX_Cube.cycle(int(raw[0]), int(raw[1]), int(raw[2]))
        updateBlock()
        updateMoves(moveSeq=[int(raw[0]), int(raw[1]), int(raw[2])])
    else:
        print(colored("submission canceled", "red"))


# testing loop
"""
while True:
    sendSingleMove()
"""


