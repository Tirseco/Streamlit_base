# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 23:52:07 2022

@author: yvesw
"""


import numpy as np
import pandas as pd

import random

# random.Random(randomSeed).shuffle(availableList)

def buildBingoPath(startingRange, endRange, alreadyDrawn = [], randomSeed = None):
    fullRange = list(np.arange(startingRange + 1, endRange + 1))
    availableList = list(set(fullRange) - set(alreadyDrawn))
    random.shuffle(availableList)
    outList = alreadyDrawn + availableList
    return dict(zip(outList, fullRange))

def buildMultiplePaths(startingRange, endRange, numberOfPaths, alreadyDrawn = [], randomSeed = None):
    fullRange = list(np.arange(startingRange + 1, endRange + 1))
    availableList = list(set(fullRange) - set(alreadyDrawn))
    outList = []
    for i in range(0, numberOfPaths):
        random.shuffle(availableList)
        fullList = alreadyDrawn + availableList
        outList.append(dict(zip(fullList, fullRange)))
    return outList

def findWinningMove(path, bingoCard):
    winningMoveByList = []

    for rowsAndColumns in bingoCard:
        lastDrawInRowAndColumn = 0 
        
        for element in rowsAndColumns:
            lastDrawInRowAndColumn = max(lastDrawInRowAndColumn, path[element])
        
        winningMoveByList.append(lastDrawInRowAndColumn)

    return min(winningMoveByList)

def createBingoCardFromRowsOrColumns(rowsOrColumns):
        for seize in len(rowsOrColumns):
            rowsOrColumns.append(rowsOrColumns[0][seize],
                                 rowsOrColumns[0][seize],
                                 rowsOrColumns[0][seize],
                                 rowsOrColumns[0][seize],
                                 rowsOrColumns[0][seize])
            
    
class Player():
    def __init__(self, name, bingoNumbersListOfLists = []):
        self.name = name
        self.bingoNumbersListOfLists = bingoNumbersListOfLists
        
    def addRowOrColumn(self,rowOrColum):
        self.bingoNumbersListOfLists.append(rowOrColum)
        
    
            

class BingoGame():
    def __init__(self, ID):
        self.ID = ID
        self.playerList = []
        self.pathList = []
        self.gameCounter = 0
        self.winnerList = []
        self.gameEndingMoveList = []
        self.randomSeed = None

    def addPlayer(self,player):
        self.playerList.append(player)
        
    def addPath(self,path):
        self.pathList.append(path)
        
    def generatePaths(self, startingRange, endRange, numberOfPaths = 100, alreadyDrawn = []):
        self.pathList = (buildMultiplePaths(startingRange, endRange, numberOfPaths, alreadyDrawn))
        # for i in range(0, numberOfPaths):
        #     self.addPath(buildBingoPath(startingRange, endRange,alreadyDrawn))
            
    def playGame(self, path):
        winningMove = np.inf
        status = 'Init_String'
        for player in range(0, len(self.playerList)):
            playerName =  self.playerList[player].name
            potentialWinningMove = findWinningMove(path, self.playerList[player].bingoNumbersListOfLists)
            status = playerName*(bool(potentialWinningMove < winningMove)) + "Draw"*bool((potentialWinningMove == winningMove)) + status*(bool(potentialWinningMove > winningMove)) 
            winningMove = min(winningMove, potentialWinningMove)
            
        self.gameCounter += 1
        
        return status, winningMove
    
    def playBulk(self):
        self.resetGamesPlayed()
        for pathNumber in range(0, len(self.pathList)):
            path = self.pathList[pathNumber]
            status, winningMove = self.playGame(path)
            self.winnerList.append(status)
            self.gameEndingMoveList.append(winningMove)
    
    def resetGamesPlayed(self):
        self.gameCounter = 0
        self.winnerList = []
        self.gameEndingMoveList = []
        
    def resetPlayersCards(self):
        for player in self.playerList:
            self.playerList.bingoNumbersListOfLists = []
        
    def fullReset(self):
        self.playerList = []
        self.winnerList = []
        self.pathList = []
        self.gameCounter = 0
        self.winnerList = []
        self.gameEndingMoveList = []
        
    def summariseResults(self):
        newList = []
        for pathNumber in range(0, len(self.pathList)):
            path = self.pathList[pathNumber]
            newList.append(list(path.keys()))

        minValuePath = min(list(path.keys()))
        maxValuePath = max(list(path.keys()))
                           
        prependFrame = pd.DataFrame([self.winnerList, self.gameEndingMoveList], index =  ['Winning Player', 'Winnig Turn']).transpose()
        outFrame = pd.DataFrame(newList, columns= list(np.arange(minValuePath, maxValuePath +1 )))
        outFrame = pd.concat([prependFrame, outFrame], axis=1)
            
        return outFrame


def quantifyMonteCarloNoise(numberOfPaths, numberOfSimulation):
    playerOneCard = [
                    [1,2,3, 4,5],
                    [6, 7, 8, 9, 11],
                    [11, 12, 13, 14, 15],
                    [16, 17, 18, 19, 20],
                    [21, 22, 23, 24, 25]
                    ]
    playerTwoCard = [
                    [26,27,28, 29,30],
                    [31, 32, 33, 34, 35],
                    [36, 37, 38, 39, 40],
                    [41, 42, 43, 44, 45],
                    [46, 47, 48, 49, 50]
                    ]
    
    playerOne = Player('Player One')
    
    for seize in range(0,len(playerOneCard)):
        playerOneCard.append([playerOneCard[0][seize],
                             playerOneCard[1][seize],
                             playerOneCard[2][seize],
                             playerOneCard[3][seize],
                             playerOneCard[4][seize]])
    
    
    playerOne.bingoNumbersListOfLists = playerOneCard
    playerTwo = Player('Player Two')
    
    for seize in range(0,len(playerTwoCard)):
        playerTwoCard.append([playerTwoCard[0][seize],
                             playerTwoCard[1][seize],
                             playerTwoCard[2][seize],
                             playerTwoCard[3][seize],
                             playerTwoCard[4][seize]])
        
    playerTwo.bingoNumbersListOfLists = playerTwoCard
    
    
    bingoExample = BingoGame('Im a bingo Game')
    bingoExample.addPlayer(playerOne)
    bingoExample.addPlayer(playerTwo)
    
    playerOneProbabilityList = []
    averageEndingMoveList = []
    
    for i in range(0, numberOfSimulation):
        bingoExample.generatePaths(0, 99, numberOfPaths)
        bingoExample.playBulk()
        playerOneProbabilityList.append(bingoExample.winnerList.count('Player One')/numberOfPaths)
        averageEndingMoveList.append(sum(bingoExample.gameEndingMoveList)/numberOfPaths)
        
        
    return playerOneProbabilityList, averageEndingMoveList
        

                    

if __name__ == '__main__':

    playerOne = Player('John')
    rowsPlayerOne = [
                    [33,46,90, 89,76],
                    [36, 48, 17, 1, 51],
                    [28, 62, 52, 84, 2],
                    [19, 68, 95, 3, 71],
                    [21, 29, 59, 34, 75]
                    ]
    for seize in range(0,len(rowsPlayerOne)):
        rowsPlayerOne.append([rowsPlayerOne[0][seize],
                             rowsPlayerOne[1][seize],
                             rowsPlayerOne[2][seize],
                             rowsPlayerOne[3][seize],
                             rowsPlayerOne[4][seize]])
        
    playerOne.bingoNumbersListOfLists = rowsPlayerOne
    
    playerTwo = Player('Sam')
    rowsPlayerTwo = [
                    [58,49,6, 22,96],
                    [48, 69, 33, 10, 87],
                    [12, 86, 46, 42, 34],
                    [32, 20, 31, 24, 1],
                    [71, 47, 39, 25, 23]
                    ]
    for seize in range(0,len(rowsPlayerTwo)):
        rowsPlayerTwo.append([rowsPlayerTwo[0][seize],
                             rowsPlayerTwo[1][seize],
                             rowsPlayerTwo[2][seize],
                             rowsPlayerTwo[3][seize],
                             rowsPlayerTwo[4][seize]])
        
    playerTwo.bingoNumbersListOfLists = rowsPlayerTwo
    
    bingoExample = BingoGame('Im a bingo Game')
    bingoExample.addPlayer(playerOne)
    bingoExample.addPlayer(playerTwo)
    
    drawnNumbers = [60, 48,27,46,28,89,20,25,38,96]
    
    bingoExample.generatePaths(0, 99, 1000, drawnNumbers)
    
    bingoExample.playBulk()
    
    if False:    
        hundredPaths =  quantifyMonteCarloNoise(100, 100)
        pd.DataFrame(hundredPaths).to_excel(r'C:\Users\yvesw\Codes\Web_GUI\100_100_paths.xlsx')
        thousandPaths =  quantifyMonteCarloNoise(1000, 100)
        pd.DataFrame(thousandPaths).to_excel(r'C:\Users\yvesw\Codes\Web_GUI\1000_1000_paths.xlsx')
        thenThousandPaths =  quantifyMonteCarloNoise(10000, 100)
        pd.DataFrame(thenThousandPaths).to_excel(r'C:\Users\yvesw\Codes\Web_GUI\10000_100_paths.xlsx')
        hundredThousandPaths =  quantifyMonteCarloNoise(100000, 100)
        pd.DataFrame(hundredThousandPaths).to_excel(r'C:\Users\yvesw\Codes\Web_GUI\100000_100_paths.xlsx')
        millonPaths =  quantifyMonteCarloNoise(1000000, 100)
        pd.DataFrame(millonPaths).to_excel(r'C:\Users\yvesw\Codes\Web_GUI\1000000_100_paths.xlsx')
