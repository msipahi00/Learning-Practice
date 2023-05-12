
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
import nltk
import re
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
import gensim
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
import plotly.express as px
import string
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix


#import tensorflow modules
import tensorflow as tf
from tensorflow.keras.preprocessing.text import one_hot,Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Embedding, Input, LSTM, Conv1D, MaxPool1D, Bidirectional, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.utils import to_categorical


stock_df = pd.read_csv('/Users/marksipahimalani/Desktop/Learning-Practice/UdemyPythonMLAppsFinance/stock_sentiment.csv')

def remove_punc(s): 
    return ''.join([char for char in s if char not in string.punctuation])

def preprocess(message): 
    stop_words = stopwords.words('english')
    stop_words.extend(['https','from', 'subject', 're', 'edu', 'use', 'will', 'aap', 'co', 'day', 'user', 'stock', 'today', 'week', 'year'])
    result = []
    for token in gensim.utils.simple_preprocess(message):
        if len(token) >= 3 and token not in stop_words: 
            result.append(token)
    
    return result 

stock_df['Text Without Punctuation'] = stock_df['Text'].apply(remove_punc)
stock_df['Text Without Stopwords'] = stock_df['Text Without Punctuation'].apply(preprocess)
stock_df['Text Without Stopwords Joined'] = stock_df['Text Without Stopwords'].apply(lambda x: ' '.join(x))

def create_wordcloud(df): 
    plt.figure(figsize = (20,20))
    wc = WordCloud(max_words=1000, width=800, height=400).generate(' '.join(stock_df[ stock_df['Sentiment'] == 1]['Text Without Stopwords']))
    plt.imshow(wc)
    plt.show()
#create_wordcloud(stock_df)

def find_max_word_len(df):
    maxlen = -1 
    
    for doc in df['Text Without Stopwords Joined']:
        if maxlen > len(nltk.word_tokenize(doc)):
            continue
        else: 
            maxlen = len(nltk.word_tokenize(doc))

    return maxlen

def find_num_words(df):

    word_list = []
    for row in df['Text Without Stopwords']:
        for word in row: 
            word_list.append(word)
    
    word_list = list(set(word_list))
    return word_list, len(word_list)



#create histogram for length distribution 
def create_histogram_length(df): 
    length = [len(nltk.word_tokenize(x)) for x in df['Text Without Stopwords']]
    fig = px.histogram(x = length, nbins = 50)
    fig.show()

def create_data(df, tot_words, maxlen): 
    x = df['Text Without Stopwords']
    y = df['Sentiment']
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size = 0.1)
    print(x_train.shape)
    print(y_train.shape)
    tokenizer = Tokenizer(num_words = tot_words)
    tokenizer.fit_on_texts(x_train)
    train_sequences = tokenizer.texts_to_sequences(x_train)
    test_sequences = tokenizer.texts_to_sequences(x_test)
    padded_train = pad_sequences(train_sequences, maxlen = maxlen)
    padded_test = pad_sequences(test_sequences, maxlen = maxlen)
    y_train_cat = to_categorical(y_train, 2)
    y_test_cat = to_categorical(y_test, 2)

    return padded_train, padded_test, y_train_cat, y_test_cat

def build_model(): 
    model = Sequential()
    model.add(Embedding(total_words, output_dim = 512))
    model.add(LSTM(250))
    model.add(Dense(128, activation = 'relu'))
    model.add(Dropout(0.3))
    model.add(Dense(2, activation = 'softmax'))
    model.compile(optimizer = 'adam', loss = 'categorical_crossentropy', metrics = ['acc'])
    print(model.summary())

    return model

def train_model(model, x_train, y_train): 
    model.fit(
        x_train, y_train, 
        batch_size = 32, 
        validation_split = 0.2,
        epochs = 2
    )

def make_pred(model, x_test, y_test):
    pred = model.predict(x_test)
    prediction = []
    original = [] 
    for i in pred: 
        prediction.append(np.argmax(i))
    for i in y_test: 
        original.append(np.argmax(i))

    acc = accuracy_score(original, prediction)
    cm = confusion_matrix(original, prediction)
    plt.figure(figsize = (5,5))
    g = sns.heatmap(cm, annot = True)
    plt.show()    

        
    

    



total_words = find_num_words(stock_df)[1]
pad_train, pad_test, y_train_cat, y_test_cat = create_data(stock_df, total_words, find_max_word_len(stock_df))
mod = build_model()
train_model(mod, pad_train, y_train_cat)
make_pred(mod, pad_test, y_test_cat)