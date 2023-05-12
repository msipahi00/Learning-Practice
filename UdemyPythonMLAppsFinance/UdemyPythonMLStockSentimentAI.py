
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

#import tensorflow modules


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
    
    return ' '.join(result) 

stock_df['Text Without Punctuation'] = stock_df['Text'].apply(remove_punc)
stock_df['Text Without Stopwords'] = stock_df['Text Without Punctuation'].apply(preprocess)

def create_wordcloud(df): 
    plt.figure(figsize = (20,20))
    wc = WordCloud(max_words=1000, width=800, height=400).generate(' '.join(stock_df[ stock_df['Sentiment'] == 1]['Text Without Stopwords']))
    plt.imshow(wc)
    plt.show()
#create_wordcloud(stock_df)

def find_max_word_len(df):
    maxlen = -1 
    
    for doc in df['Text Without Stopwords']:
        if maxlen > len(nltk.word_tokenize(doc)):
            continue
        else: 
            maxlen = len(nltk.word_tokenize(doc))
    print(maxlen)

def find_num_words(df): 
    return sum([len(nltk.word_tokenize(x)) for x in df['Text Without Stopwords']])


#create histogram for length distribution 
def create_histogram_length(df): 
    length = [len(nltk.word_tokenize(x)) for x in df['Text Without Stopwords']]
    fig = px.histogram(x = length, nbins = 50)
    fig.show()

print(find_num_words(stock_df))