import pandas as pd
import seaborn as sns
import plotly.express as px
from copy import copy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
import plotly.graph_objects as go



#function to normalize stock prices 
def normalize(df): 
    x = df.copy()
    for col in df.columns[1:]:
        x[col] = x[col]/x[col][0]
    return x 

#function to create an interactive plot from dataframe
def interactive_plot(df, title): 
    fig = px.line(title = title)
    for i in df.columns[1:]:
        fig.add_scatter(x = df['Date'], y = df[i], name = i)
    fig.show()

#function to calculate daily return in percent 
def calc_daily(df): 
    daily_return_df = df.copy()

    for stock in df.columns[1:]:
        for day in range(1,len(df)): 
            daily_return_df[stock][day] = ((df[stock][day] - df[stock][day-1]) / df[stock][day-1]) * 100

    for stock in df.columns[1:]:
        daily_return_df[stock][0] = 0.0000 

    return daily_return_df

#function to plot a scatter plot between two selected stocks 
# with linear regression 
def scatter_create(market, stock_one, df_daily_return): 
    df_daily_return.plot(kind = 'scatter', x = market, y = stock_one)
    beta, alpha = find_beta_alpha(df_daily_return[market], df_daily_return[stock_one])
    plt.plot(df_daily_return[market], beta * df_daily_return[market] + alpha, '-', color = 'r')
    plt.show()
    #x should be the sp500 

#After having a scatter plot, we're going to want to solve for the alpha and beta (straight line fit)
#Beta is slope of the line (market return vs stock return)
#Describes the systematic risk or volatility 

def find_beta_alpha(market_daily_r, stock_one_daily_r): 
    beta, alpha  = np.polyfit(x = market_daily_r, y = stock_one_daily_r, deg = 1)
    return beta, alpha 

#calculating the expected return of a stock using CAPM 
#rf is the risk free rate 
def ER_stock(market, stock_one, df_daily_return, rf): 
    rm = df_daily_return[market].mean()*252
    rf = rf
    beta, alpha = find_beta_alpha(df_daily_return[market], df_daily_return[stock_one])
    er = rf + (beta * (rm - rf))

    print('The expected rate of return for {} is {} over the year'.format(stock_one, er))
    return er 

#calculate the return on a total portfolio with weights 
def portfolio_returns(market, tickers, weights, daily_returns, rf):
    ER = {}
    rm = daily_returns[market].mean()*252
    sum = 0 
    for idx, t in enumerate(tickers): 
        er = ER_stock(market, t, daily_returns, rf)
        sum += er*weights[idx]
    
    print('Expected return on portfolio is {}%'.format(sum)) 
    return sum 


#misc 

#Average daily rate of return for sp500 = df_daily_r['sp500'].mean()
#for annual average, multiply by 252
#Assume that risk free rate is zero (can pull from online) 


if __name__ == '__main__':

    stocks_df = pd.read_csv('/Users/marksipahimalani/Desktop/Learning-Practice/stock.csv')
    stock_df = stocks_df.sort_values(by = ['Date'])
    daily_r = calc_daily(stock_df)
    portfolio_returns('sp500', ['AMZN', 'AAPL', 'BA', 'T', 'MGM', 'IBM'], 1/6 * np.ones(6), daily_r, 0)

    #ER_stock('sp500', 'AAPL', daily_r, 0)
    #print(daily_r)
    #scatter_create('sp500', 'AAPL', daily_r)
    #interactive_plot(normalize(stocks_df), 'Normalized Prices')