# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 13:47:21 2022

@author: yvesw
"""


import streamlit as st
import pandas as pd
import numpy as np


import bingo_game as bg

# from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode


def addPlayersNumbers(dataFrame):
    outListOfList = []
    for row in dataFrame.iterrows():
        outListOfList.append(list(row[1]))
        
    for column in dataFrame.columns:
        outListOfList.append(list(dataFrame[column]))
        
        
    return outListOfList




header = st.container()
playerContainer = st.container()
# playerOneContainer = st.container()
# playerTwoContainer = st.container()

gameInterFace = st.container()

    

with header:
    st.title('Welcome to my GUI')
    
# Using "with" notation
with st.sidebar:
    inputFile = st.file_uploader("Upload Excel input")
    
    # randomSeed = st.number_input('Random Seed', min_value=0, max_value=9999999999, value = int(), step = 1)
    numberOfPaths = st.radio(
        "Number of Paths",
        (100, 1000, 10000, 100000, 1000000)
    )
    
    drawnNumbers = st.multiselect('Already Drawn',np.arange(1,100))
    
    
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
        # playerOneData.applymap(hihglightSelected)
        # st.dataframe(playerOneData)
        if inputFile is not None:
            playerOneData = pd.read_excel(inputFile, 'PlayerOne')
            st.dataframe(playerOneData.style.applymap(hihglightSelected))
    with c2:
        st.header('Player Two')
        # playerTwoData.applymap(hihglightSelected)
        if inputFile is not None:
            playerTwoData = pd.read_excel(inputFile, 'PlayerTwo')
            st.dataframe(playerTwoData.style.applymap(hihglightSelected))
    

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
            
            playerOneWins = gameToPlay.winnerList.count('')
            playerTwoWins = gameToPlay.winnerList.count('Player Two')
            draws = gameToPlay.winnerList.count('Draw')
            
            playerOneWinsPercentage = playerOneWins/numberOfPaths*100
            playerTwoWinsPercentage = playerTwoWins/numberOfPaths*100
            drawsPercentage =  draws/numberOfPaths*100
            
            st.text('Ran with ' + str(numberOfPaths) + " Paths")
            st.text('Ran with' + str(drawnNumbers) + " already drawn")
            st.text('Player one Won ' + str(playerOneWins) +" (" + str(playerOneWinsPercentage) + "%)" + ' Games')
            st.text('Player two  Won ' + str(playerTwoWins) +" (" + str(playerTwoWinsPercentage) + "%)"  + ' Games')
            st.text('Number of draws ' + str(draws) +" (" + str(drawsPercentage) + "%)" + ' Games')
            summaryFrame = pd.DataFrame([[playerOneWinsPercentage, playerTwoWinsPercentage, drawsPercentage]],
                                        columns = ['Player One %', 'Player Two %', 'Draws %'])
            
            summaryFrame.index = ['% of Total']
            st.bar_chart(summaryFrame.transpose())
            # st.text(gameToPlay.winnerList)
            gameDF = gameToPlay.summariseResults()
            st.dataframe(gameDF)
        
        csv = convert_df_to_csv(gameDF)
        
        st.download_button('Download Summary', data =csv, file_name='Summary Bingo Results.csv', mime = 'text/csv', )
        

# import pandas as pd

# df = pd.DataFrame({
#     "name":         ["alan","beth","charlie","david", "edward"],
#     "age" :         [34,    12,     43,      32,      77],
#     "num_children": [1,     0,      2,       1,       6],
#     "num_pets":     [1,     0,      1,       2,       0],
#     "bank_balance": [100.0, 10.0,   -10.0,   30.0,    30.0]})

# def even_number_background(cell_value):

#     highlight = 'background-color: darkorange;'
#     default = ''

#     if type(cell_value) in [float, int]:
#         if cell_value in drawnNumbers:
#             return highlight
#     return default


    
# st.dataframe(df.style.applymap(even_number_background))
    
    
# st.dataframe(data)
if False:
    gb = GridOptionsBuilder.from_dataframe(data)
    
    grid_response = AgGrid(
        data,
        editable = True,
        reload_data = True,
        data_return_mode=DataReturnMode.AS_INPUT,
        update_mode = GridUpdateMode.MANUAL, 
        key = 'NumeroUno'
    )
    
    dataTwo = grid_response['data']
    
    dataTwo = pd.DataFrame(dataTwo)
    dataTwo.to_excel(workPath, 'Input', index=False)

# data = pd.read_excel(workPath, 'Input')


# st.dataframe(data)

# grid_response_Two = AgGrid(
#     dataTwo,
#     editable = True,
#     reload_data = True,
#     data_return_mode=DataReturnMode.AS_INPUT,
#     update_mode = GridUpdateMode.MANUAL ,
#     key = 'NumberTwo'

# )

# data = grid_response['data']
# selected = grid_response['selected_rows'] 
# df = pd.DataFrame(selected) #Pass the selected rows to a new dataframe df
    
# import streamlit as st
# from st_aggrid import GridOptionsBuilder, AgGrid
# from st_aggrid.shared import GridUpdateMode, DataReturnMode
# import pandas as pd

# vpth = “your path” # path that contains the csv file
# csvfl = “tst.csv” # I used a small csv file containing 2 columns: Name & Amt
# tdf = pd.read_csv(vpth + csvfl) # load csv into dataframe

# gb = GridOptionsBuilder.from_dataframe(data)
# gb.configure_column(“Name”, header_name=(“F Name”), editable=True)
# gb.configure_column(“Amt”, header_name=(“Amount”), editable=True, type=[“numericColumn”,“numberColumnFilter”,“customNumericFormat”], precision=0)

# gridOptions = gb.build()
# dta = AgGrid(data,
# gridOptions=gridOptions,
# reload_data=False,
# height=200,
# editable=True,
# theme="streamlit",
# data_return_mode=DataReturnMode.AS_INPUT,
# update_mode=GridUpdateMode.MODEL_CHANGED)

# st.write("Please change an amount to test this")

# if st.button("Iterate through aggrid dataset"):
#     for i in range(len(dta['data'])): # or you can use for i in range(tdf.shape[0]):
#         st.caption(f"df line: {tdf.loc[i][0]} | {tdf.loc[i][1]} || AgGrid line: {dta[‘data’][‘Name’][i]} | {dta[‘data’][‘Amt’][i]}")
    
#         # check if any change has been done to any cell in any col by writing a caption out
#         if tdf.loc[i]['Name'] != dta['data']['Name'][i]:
#             st.caption(f"Name column data changed from {tdf.loc[i]['Name']} to {dta['data']['Name'][i]}...")
#             # consequently, you can write changes to a database if/as required
    
#         if tdf.loc[i]['Amt'] != dta['data']['Amt'][i]:
#             st.caption(f"Amt column data changed from {tdf.loc[i]['Amt']} to {dta['data']['Amt'][i]}...")

# tdf = dta['data']    # overwrite df with revised aggrid data; complete dataset at one go
# tdf.to_csv(vpth + 'file1.csv', index=False)  # re/write changed data to CSV if/as required
# st.dataframe(tdf)    # confirm changes to df
