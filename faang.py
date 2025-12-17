#faang.py 
# Author: Cathal Redmond
# Date: 17 Dec 2025

# import required modules 
import yfinance as yf
import time
import datetime as dt
import pandas as pd
from pathlib import Path
import os
import matplotlib.pyplot as plt

# define program start time and dates for use in calculations 
start= time.time()
today = dt.date.today()
yesterday = today - dt.timedelta(days=1)
fivedaysago = today - dt.timedelta(days=5)

# Convert dates to string type data as is required by the yf.download function
strtoday = str(today)
strfivedaysago =str(fivedaysago)

# Define a list of stocks to track
ticker_list =['META','AAPL','AMZN','NFLX','GOOG']

# define the prices tuple
prices = ('Open', 'High', 'Low', 'Close', 'Volume')

# Define path to root file
datadir = "./data/"# Problem 1: Data from yfinance

def get_data():


    # Execute the yf.download operation and populating the data into a dataframe.  
    data =yf.download( 
        start= strfivedaysago,
        end= strtoday,
        interval= '15m',
        tickers = ticker_list,
        threads=True,
        group_by='ticker',
        auto_adjust = True,
        )
    return data

#call the function to get the data
data = get_data()

# Get date and time information for file name into the correct format
now = dt.datetime.now()
filename = now.strftime("%Y%m%d-%H%M%S")

# Write data to csv file. 
data.to_csv(datadir+filename+".csv", sep=',')

# This segment allows for monitoring the time taken to complete the execution of the program. 
print ('The program takes ', time.time()-start,'seconds.')


# List all files in the directory data 
list_of_files = os.listdir(datadir)

#sort the list to display the newest file in sorted order
list_of_files.sort(reverse = True)

# assign a variable name to the file selected as the latest file 
recent_file = list_of_files[0]

#Define a function Plot_data() to read the most recent data file and plot the closing prices of each stock
# Read the most recent data file into a dataframe
df = pd.read_csv(f'./data/{recent_file}', header=[0, 1], index_col=0)

#remove errors from dataframe
df.dropna(inplace=True)

# convert the datetime to string format
df.index = pd.to_datetime(df.index)
df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')

def Plot_data():
    # Plot the closing prices of each stock
    plt.figure(figsize=(12,6))
    for ticker in ticker_list:
        plt.plot(df.index, df[(ticker, 'Close')], label=ticker)
    
    plt.xlabel('DateTime')
    plt.ylabel('Closing Price')
    plt.title('Closing Prices of Stocks Over Time')
    plt.legend()
    plt.xticks(rotation=80)
    plt.tight_layout()
    plt.savefig('closing_prices_chart.png', bbox_inches='tight')
    plt.show()

# Call the Plot_data function to execute the plotting
Plot_data()

# create a new dataframe for the closing prices
close_df = pd.DataFrame()
for ticker in ticker_list:
    close_df[ticker] = df[ticker]['Close']