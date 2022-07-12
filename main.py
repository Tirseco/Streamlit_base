# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 13:47:21 2022

@author: yvesw
"""


import streamlit as st
import pandas as pd
import numpy as np

import bingo_game as bg
import scipy.stats as scStat

# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


def addPlayersNumbers(dataFrame):
    outListOfList = []
    for row in dataFrame.iterrows():
        outListOfList.append(list(row[1]))
        
    for column in dataFrame.columns:
        outListOfList.append(list(dataFrame[column]))
        
        
    return outListOfList


def obtainZscores(alpha):
    return scStat.norm.ppf(alpha)

def bernoulliInterval(sampleEstimate, alpha, numberOfDraws):
    lowerZscore = obtainZscores(alpha/2)
    upperZscore = obtainZscores(1-alpha/2)
    
    lowerBound = sampleEstimate + lowerZscore*np.sqrt((sampleEstimate*(1-sampleEstimate))/numberOfDraws)
    upperBound = sampleEstimate + upperZscore*np.sqrt((sampleEstimate*(1-sampleEstimate))/numberOfDraws)
    
    return lowerBound, upperBound
    

header = st.container()
playerContainer = st.container()

gameInterFace = st.container()

def castListToInt(textList):
    outList = []
    for element in textList:
        outList.append(int(element))
        
    return outList
        

with header:
    st.title('Welcome to my GUI')
    
# Using "with" notation
with st.sidebar:
    inputFile = st.file_uploader("Upload Excel input")
    
    # randomSeed = st.number_input('Random Seed', min_value=0, max_value=9999999999, value = int(), step = 1)
    numberOfPaths = st.radio(
        "Number of Paths",
        (100, 1000, 10000, 100000)
    )
    
    drawnNumbers = st.multiselect('Already Drawn',np.arange(1,100))
    
    confidenceLevel = st.radio(
        "Confidence Level",
        (0.99, 0.95, 0.90)
    )
    
    
def hihglightSelected(cell_value):

    highlight = 'background-color: darkorange;'
    default = ''

    if type(cell_value) in [float, int]:
        if cell_value in drawnNumbers:
            return highlight
    return default

def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')
   
def convert_to_excel(df):
    return df.to_excel().encode('utf-8')
    
with playerContainer:
    c1, c2 = st.columns(2)
    with c1:
        st.header('Player One')
        available = np.arange(1,100)
        firstRow = st.multiselect('1st Row P1', available, np.arange(1,6))
        # available = availableList = list(set(available) - set(firstRow))
        secondRow = st.multiselect('2nd Row P1', available, np.arange(6,11))
        thirdRow = st.multiselect('3rd Row P1', available, np.arange(11,16))
        fourthRow = st.multiselect('4th Row P1', available, np.arange(16,21))
        fifthRow = st.multiselect('5th Row P1', available, np.arange(21,26))
        

        # playerOneData.applymap(hihglightSelected)
        # st.dataframe(playerOneData)
        
    with c2:
        st.header('Player Two')
        firstRowPlayerTwo = st.multiselect('5th Row P2', available, np.arange(26,31))
        secondRowPlayerTwo = st.multiselect('5th Row P2', available, np.arange(31,36))
        thirdRowPlayerTwo = st.multiselect('5th Row P2', available, np.arange(36,41))
        fourthRowPlayerTwo = st.multiselect('5th Row P2', available, np.arange(41,46))
        fifthRowPlayerTwo = st.multiselect('5th Row P2', available, np.arange(46,51))
        # if st.button('Load from List', key = 'Player Two'):
            
        
            
    loadingCheckBox = st.checkbox('Load from List', key='Player One')        
    if loadingCheckBox:
        with c1:
            playerOneData = pd.DataFrame([
                firstRow,
                secondRow,
                thirdRow,
                fourthRow,
                fifthRow
                ], columns=['One', 'Two', 'Three', 'Four','Five'])
            playerOneFrame = st.dataframe(playerOneData.style.applymap(hihglightSelected))
        
        with c2:    
            playerTwoData = pd.DataFrame([
                firstRowPlayerTwo,
                secondRowPlayerTwo,
                thirdRowPlayerTwo,
                fourthRowPlayerTwo,
                fifthRowPlayerTwo
                ], columns=['One', 'Two', 'Three', 'Four','Five'])
            playerTwoFrame = st.dataframe(playerTwoData.style.applymap(hihglightSelected))
            
    # playerTwoData.applymap(hihglightSelected)
    with c1:
        if inputFile is not None and loadingCheckBox==False:
            loadingCheckBox = False
            playerTwoData = pd.read_excel(inputFile, 'PlayerTwo')
            playerTwoFrame = st.dataframe(playerTwoData.style.applymap(hihglightSelected))
    
    with c2:    
        if inputFile is not None and loadingCheckBox==False:
                playerOneData = pd.read_excel(inputFile, 'PlayerOne')
                playerOneFrame = st.dataframe(playerOneData.style.applymap(hihglightSelected))
    

# with playerOneContainer:
# with playerTwoContainer:
    
    
with gameInterFace:
    if st.button('Play Game'):
        playerOne = bg.Player('Player One', addPlayersNumbers(playerOneData))
        playerTwo = bg.Player('Player Two', addPlayersNumbers(playerTwoData))
        
        gameToPlay = bg.BingoGame('Interactive Game')
        gameToPlay.addPlayer(playerOne)
        gameToPlay.addPlayer(playerTwo)
        # gameToPlay.randomSeed = randomSeed
        gameToPlay.generatePaths(0, 99, numberOfPaths, drawnNumbers)
        
        if True:
            gameToPlay.playBulk()
            
            playerOneWins = gameToPlay.winnerList.count('Player One')
            playerTwoWins = gameToPlay.winnerList.count('Player Two')
            draws = gameToPlay.winnerList.count('Draw')
            
            playerOneWinsPercentage = playerOneWins/numberOfPaths*100
            playerTwoWinsPercentage = playerTwoWins/numberOfPaths*100
            drawsPercentage =  draws/numberOfPaths*100
                        
            playerOneConfidenceInterval = bernoulliInterval(playerOneWinsPercentage/100, 1-confidenceLevel, numberOfPaths)
            playerTwoConfidenceInterval = bernoulliInterval(playerTwoWinsPercentage/100, 1-confidenceLevel, numberOfPaths)
                        
            
            st.text('Ran with ' + str(numberOfPaths) + " Paths")
            st.text('Ran with' + str(drawnNumbers) + " already drawn")
            st.text('Player one Won ' + str(playerOneWins) +" (" + str(round(playerOneWinsPercentage,2)) + "%)" + ' Games')
            
            st.text('Player one ' + str(round((confidenceLevel)*100,2)) + ' % confidence Interval ' + str(round(playerOneConfidenceInterval[0]*100,2)) + "%" + " to " + str(round(playerOneConfidenceInterval[1]*100,2)) + "%" )
                    
            st.text('Player two  Won ' + str(playerTwoWins) +" (" + str(round(playerTwoWinsPercentage,2)) + "%)"  + ' Games')
            st.text('Player two ' + str(round((confidenceLevel)*100,2)) + ' % confidence Interval ' + str(round(playerTwoConfidenceInterval[0]*100,2)) + "%" +" to " + str(round(playerTwoConfidenceInterval[1]*100,2)) + "%")
            st.text('Number of draws ' + str(draws) +" (" + str(drawsPercentage) + "%)" + ' Games')
            summaryFrame = pd.DataFrame([[playerOneWinsPercentage, playerTwoWinsPercentage, drawsPercentage]],
                                        columns = ['Player One %', 'Player Two %', 'Draws %'])
            
            summaryFrame.index = ['% of Total']
            st.bar_chart(summaryFrame.transpose())
            # st.text(gameToPlay.winnerList)
            gameDF = gameToPlay.summariseResults()
            st.dataframe(gameDF.head(100))
        
        csv = convert_df_to_csv(gameDF)
        
        st.download_button('Download Summary', data =csv, file_name='Summary Bingo Results.csv', mime = 'text/csv', )
        

