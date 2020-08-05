import os
from random import choice

from time import sleep

heuristic = 1 #choose wich heuristic to run code with that, you can pick 1 or 2 or 3,
#  *Full exaplantion about this var in my report*


class Block:
    bList = []

    def __init__(self, x, y, obs=False):
        self.x = x
        self.y = y
        self.h = 0
        self.H = 0
        self.obs = obs
        self.obj = None
        self.mushroom = None
        self.dict = {"Up": None, "Down": None, "Left": None, "Right": None}
        Block.bList.append(self)

    # def __eq__(self, x, y):
    #     if self.x == x and self.y == y:
    #         return True
    #     else:
    #         return False
    def __repr__(self):
        if self.obj != None:
            return "Mri"
        elif self.mushroom != None:
            return self.mushroom.cl
        elif self.obs:
            return "X"
        else:
            return "-"


class Mario:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.red = False
        self.blue = False
        self.pState = None
        self.pAction = None
        self.result = []


class Mushroom:
    mList = []
    hideMushrom = 0

    def __init__(self, x, y, cl):
        self.x = x
        self.y = y
        self.cl = cl
        Mushroom.mList.append(self)


adress = "/Users/mohammadsadra/Desktop/AUT/Artificial Intelligence/Mario/Mario.txt"
f = open(os.path.expanduser(adress), "r")

line = f.readline()
n = int(line)

line = f.readline()
m = int(line)
Matrix = [[0 for x in range(n + 1)] for y in range(m + 1)]
for i in range(1, n + 1):
    for j in range(1, m + 1):
        Matrix[i][j] = Block(i, j)

line = f.readline().split(" ")
x = int(line[0])
y = int(line[1])
mario = Mario(x, y)
Matrix[x][y].obj = mario

line = f.readline()
k = int(line)

for i in range(0, k):
    line = f.readline().split(" ")
    x = int(line[0])
    y = int(line[1])
    red = Mushroom(x, y, "red")
    Matrix[x][y].mushroom = red

for i in range(0, k):
    line = f.readline().split(" ")
    x = int(line[0])
    y = int(line[1])
    blue = Mushroom(x, y, "blue")
    Matrix[x][y].mushroom = blue
Mushroom.hideMushrom = len(Mushroom.mList)

while True:
    line = f.readline()
    if line == "\n":
        break
    line = line.split(" ")
    x = int(line[0])
    y = int(line[1])
    obs = Matrix[x][y].obs = True


def printTable():
    i = m
    while i >= 1:
        for j in range(1, n + 1):
            print(Matrix[j][i], end=" ")
        i -= 1
        print()
    # sleep(5)


def goalTest():
    if mario.blue and mario.red:
        return True
    else:
        return False


def findMin(list):
    min = list[0]
    for child in list:
        if min > child:
            min = child
    return min


def findMax(list):
    max = list[0]
    for child in list:
        if max < child:
            max = child
    return max


def Right():
    if mario.x + 1 <= n:
        Matrix[mario.x][mario.y].obj = None
        mario.pState = Matrix[mario.x][mario.y]
        mario.x += 1
        Matrix[mario.x][mario.y].obj = mario
        mario.pAction = "Right"
    else:
        blk = Block(0, 0, True)
        blk.h = 1000000
        blk.H = 1000000
        Matrix[mario.x][mario.y].dict["Right"] = blk


def Up():
    if mario.y + 1 <= m:
        Matrix[mario.x][mario.y].obj = None
        mario.pState = Matrix[mario.x][mario.y]
        mario.y += 1
        Matrix[mario.x][mario.y].obj = mario
        mario.pAction = "Up"
    else:
        blk = Block(0, 0, True)
        blk.h = 1000000
        blk.H = 1000000
        Matrix[mario.x][mario.y].dict["Up"] = blk


def Left():
    if mario.x - 1 >= 1:
        Matrix[mario.x][mario.y].obj = None
        mario.pState = Matrix[mario.x][mario.y]
        mario.x -= 1
        Matrix[mario.x][mario.y].obj = mario
        mario.pAction = "Left"
    else:
        blk = Block(0, 0, True)
        blk.h = 1000000
        blk.H = 1000000
        Matrix[mario.x][mario.y].dict["Left"] = blk


def Down():
    if mario.y - 1 >= 1:
        Matrix[mario.x][mario.y].obj = None
        mario.pState = Matrix[mario.x][mario.y]
        mario.y -= 1
        Matrix[mario.x][mario.y].obj = mario
        mario.pAction = "Down"
    else:
        blk = Block(0, 0, True)
        blk.h = 1000000
        blk.H = 1000000
        Matrix[mario.x][mario.y].dict["Down"] = blk


def lrtaCost(state, action):
    if state.dict.get(action) == None:
        # print(action)
        # print(state.h)
        # print()
        return state.h
    else:
        if not state.dict.get(action).obs:
            # print(action)
            # print(state.dict.get(action).H + 1)
            # print()
            return state.dict.get(action).H + 1
        else:
            # print(action)
            # print(1000000)
            # print()
            return 1000000


def computeHuristic(i):
    if i == 1:
        return Mushroom.hideMushrom
    if i == 2:
        tmpList = []
        for mush in Mushroom.mList:
            tmpList.append(abs(mush.x - mario.x) + abs(mush.y - mario.y))
        return findMin(tmpList)
    if i == 3:
        tmpList = []
        for i in range(0, len(Mushroom.mList)):
            for j in range(i, len(Mushroom.mList)):
                tmpList.append(
                    abs(Mushroom.mList[i].x - Mushroom.mList[j].x) + abs(Mushroom.mList[i].y - Mushroom.mList[j].y))
        return findMax(tmpList)


print("First time")
printTable()
counter = 0
while True:
    counter += 1
    print(counter, end=" : \n")
    if goalTest():
        print("Goal State :))")
        break

    if Matrix[mario.x][mario.y].H == 0:
        Matrix[mario.x][mario.y].h = computeHuristic(heuristic)
        Matrix[mario.x][mario.y].H = Matrix[mario.x][mario.y].h
        mario.result.append(Matrix[mario.x][mario.y])
        if Matrix[mario.x][mario.y].mushroom != None:
            if Matrix[mario.x][mario.y].mushroom.cl == "red":
                Mushroom.hideMushrom -= 1
                mario.red = True
                Matrix[mario.x][mario.y].mushroom = None
                for mush in Mushroom.mList:
                    if mush.x == mario.x and mush.y == mario.y:
                        Mushroom.mList.remove(mush)
                        break
            elif Matrix[mario.x][mario.y].mushroom.cl == "blue":
                Mushroom.hideMushrom -= 1
                mario.blue = True
                Matrix[mario.x][mario.y].mushroom = None
                for mush in Mushroom.mList:
                    if mush.x == mario.x and mush.y == mario.y:
                        Mushroom.mList.remove(mush)
                        break

    if mario.pState != None:
        Matrix[mario.pState.x][mario.pState.y].dict[mario.pAction] = Matrix[mario.x][mario.y]
        temp = [lrtaCost(mario.pState, "Up"), lrtaCost(mario.pState, "Down"), lrtaCost(mario.pState, "Left"),
                lrtaCost(mario.pState, "Right")]
        mario.pState.H = findMin(temp)

    newAction = [lrtaCost(Matrix[mario.x][mario.y], "Up"), lrtaCost(Matrix[mario.x][mario.y], "Down"),
                 lrtaCost(Matrix[mario.x][mario.y], "Left"),
                 lrtaCost(Matrix[mario.x][mario.y], "Right")]
    min = findMin(newAction)

    randomList = []

    if lrtaCost(Matrix[mario.x][mario.y], "Right") == min:
        randomList.append("Right")
    if lrtaCost(Matrix[mario.x][mario.y], "Left") == min:
        randomList.append("Left")
    if lrtaCost(Matrix[mario.x][mario.y], "Up") == min:
        randomList.append("Up")
    if lrtaCost(Matrix[mario.x][mario.y], "Down") == min:
        randomList.append("Down")
    print()
    print("Min List:")
    print(randomList)
    randomAction = choice(randomList)
    print("Action:")
    print(randomAction)
    if randomAction == "Up":
        Up()
    elif randomAction == "Down":
        Down()
    elif randomAction == "Right":
        Right()
    elif randomAction == "Left":
        Left()
    printTable()
    print()
