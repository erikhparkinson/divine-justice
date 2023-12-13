# 👉 Run "./connect" (or "connect.cmd" on Windows) in the terminal to get started

import numpy as np
from matplotlib import pyplot as plt

def flipDim(obj):
    result = obj.copy()
    result["x"] = -obj["x"]
    result["y"] = -obj["y"]
    return result

def flipMove(move):
    if move == "north":
        return "south"
    if move == "south":
        return "north"
    if move == "east":
        return "west"
    if move == "west":
        return "east"
    return "none"

class Bot:
    def __init__(self, config):
        print("Hello World!", config)
        self.config = config
        self.lastBall = None
        self.momentum = 0

    def getNextYInc(self):
        if self.momentum > 0:
            return 1.5 + 2*self.momentum
        else:
            return 1.5

    def getNextYDec(self):
        if self.momentum < 0:
            return -1.5 + 2*self.momentum
        else:
            return -1.5
    
    def updateMomentum(self, move):
        if move == "north":
            if self.momentum > 0:
                self.momentum += 1
            else:
                self.momentum = 1
        elif move == "south":
            if self.momentum < 0:
                self.momentum -= 1
            else:
                self.momentum = -1
        else:
            self.momentum = 0

    def moveEast(self, paddle, ball, isEast):
        print("paddle", paddle["x"], paddle["y"])
        print("ball", ball["x"], ball["y"])

        if self.lastBall:
            ballApproaching = self.lastBall['x'] > ball['x']
            if ballApproaching:
                #Predict location if ball is moving towards me
                xDiff = self.lastBall['x'] - ball['x']
                yDiff = self.lastBall['y'] - ball['y']
                xDiff2 = paddle['x'] - ball['x']
                predictedY = ball['y'] + yDiff * xDiff2 / xDiff
                print("Predict", predictedY)
            else:
                #Go to the middle
                predictedY = 0
            #Move north or south if it gets me closer to the predicted location
            myDiff = predictedY - paddle['y']
            if abs(paddle['y'] + self.getNextYInc() - predictedY) < abs(myDiff):
                result = "north"
            elif abs(paddle['y'] + self.getNextYDec() - predictedY) < abs(myDiff):
                result = "south"
            #Play near the net!
            elif not ballApproaching:
                result = "west"
            else: #Wait for all to come to me
                result = "none"
        else: #Start by moving to net
            result = "west"
        #Track data and return
        self.lastBall = ball
        self.updateMomentum(result)
        return result

    def move(self, eastPaddle, westPaddle, ball):
        # Determine which paddle you control.
        if self.config["paddle"] == "east":
            return self.moveEast(eastPaddle, ball, True)
        else:
            return flipMove(self.moveEast(flipDim(westPaddle), flipDim(ball), False))

    def end(self, eastPaddle, westPaddle, ball):
        print("Good game!")
        
