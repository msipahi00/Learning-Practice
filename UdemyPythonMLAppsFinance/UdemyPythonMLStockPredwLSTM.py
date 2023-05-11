import pandas as pd
import plotly.express as px
from copy import copy
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
import UdemyPythonMLStockCAPM as CAPM
from sklearn.linear_model import Ridge

stock_df = pd.read_csv('/Users/marksipahimalani/Desktop/Learning-Practice/UdemyPythonMLAppsFinance/stock.csv')

stock_vol_df = pd.read_csv('/Users/marksipahimalani/Desktop/Learning-Practice/UdemyPythonMLAppsFinance/stock_volume.csv')

stock_vol_df = stock_vol_df.sort_values(by = ['Date'])
stock_df = stock_df.sort_values(by = ['Date'])

#stock_vol_df.describe()
#stock_df.describe()
#AI learning is split between 100-x training and x testing 

#Concat the date, price, and volume in a single dataframe 
def single_stock(stock_df, vol_df, name): 
    return pd.DataFrame({'Date':stock_df['Date'], 'Close':stock_df[name], 'Volume':vol_df[name]})

#Create a function that organizes the trading data for the next day 
#Scales and separates data 
#input a single stock that has a table of date, price and volume 

def create_training(stock_info, date_offset, percent_train):
    stock_info['Target'] = stock_info['Close'].shift(-date_offset)
    stock_info = stock_info[:-date_offset]
    sc = MinMaxScaler(feature_range=(0,1))
    stock_info_scaled = sc.fit_transform(stock_info.drop(columns = ['Date']))
    x = stock_info_scaled[:, :2] #close and volume 
    y = stock_info_scaled[:, 2:] #target close 
    num = int(percent_train * len(x))

    x_train = x[:num]
    y_train = y[:num]
    x_test = x[num:]
    y_test = y[num:]

    return x, y, x_train, y_train, x_test, y_test, stock_info, stock_info_scaled

AAPL_data = single_stock(stock_df, stock_vol_df, 'AAPL')
vals = create_training(AAPL_data, 1, 0.7)

#create a regression model passing in xtrain, ytrain, alpha 
def regression_model(x, y, x_train, y_train, x_test, y_test, stock_info, stock_info_scaled, al):
    
    model = Ridge(alpha = al)
    model.fit(x_train, y_train)
    lin_reg_acc = model.score(x_test, y_test)
    print('Ridge Regession Score: {}'.format(lin_reg_acc))
    predicted = model.predict(x)

    predicted_prices = []
    for i in predicted: 
        predicted_prices.append(i[0])
    close = []
    for i in stock_info_scaled:
        close.append(i[0])
    
    
    df_predicted = stock_info[['Date']]
    df_predicted['Close'] = close
    df_predicted['Predictions'] = predicted_prices
    CAPM.interactive_plot(df_predicted, 'Original vs. Prediction')

    return df_predicted 

#regression_model(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7], 2)


def LTSM_model(x, y, x_train, y_train, x_test, y_test, stock_info, stock_info_scaled):

    
    #reshape 1d arrays to 3d arrays to feed in the model 
    x_train = x_train[:, :1]
    x_test = x_test[:, :1]
    print('xtrain first', x_train.shape)
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    x = x[:,:1]






    #y_train = y_train[:,:0]
    print('y_train', y_train.shape)
    
    print('xtrain shape', x_train.shape)
    print('xtest shape', x_test.shape)
    #Creating the model 
    print('xtrain shape1', x_train.shape[1], x_train.shape[2])
    inputs = keras.layers.Input(shape = (x_train.shape[1], x_train.shape[2]))
    
    r = keras.layers.LSTM(150, return_sequences = True)(inputs)
    r = keras.layers.Dropout(0.3)(r)
    r = keras.layers.LSTM(150, return_sequences = True)(r)
    r = keras.layers.Dropout(0.3)(r)
    r = keras.layers.LSTM(150)(r)

    outputs = keras.layers.Dense(1, activation = 'linear')(r)
    #Linear for a continuous output like stock price
    model = keras.Model(inputs = inputs, outputs = outputs)
    model.compile(optimizer = 'adam', loss = 'mse')
    print('model summary: ', model.summary())

    history = model.fit(
        x_train, y_train, 
        epochs = 20,
        batch_size = 32, 
        validation_split = 0.2
    )
    print('size x', x.shape)
    

    predictions = model.predict(x)
    test_predictions = []
    close = []

    

    df_predicted = stock_info[1:][['Date']]

    


    for i in range(1, len(predictions)): 
        test_predictions.append(predictions[i][0])
    for i in stock_info_scaled: 
        close.append(i[0])
    
    df_predicted['Predictions'] = test_predictions
    df_predicted['Close'] = close[1:]

    CAPM.interactive_plot(df_predicted, 'Original v. Prediction') 
    
    print('x', x)
    print('x_test', x_train)
    print('y_test', y_train)

    return df_predicted

    
print(LTSM_model(vals[0], vals[1], vals[2], vals[3], vals[4], vals[5], vals[6], vals[7]))
  








