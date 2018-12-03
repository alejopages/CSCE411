#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

get_ipython().run_line_magic('matplotlib', 'inline')
get_ipython().run_line_magic('run', 'load_data.ipynb')


# In[2]:


word_count = get_word_counts() #TAKE OUT STORE DATA IN FUNCTIONS IN CASE CHANGES OF DATABASE
stock_prices = get_stock_prices()

word_data = pd.DataFrame(data=word_count, columns=['id', 'word', 'count', 'date'])
stock_data = pd.DataFrame(data=stock_prices, columns=['id', 'openprice', 'closeprice', 'date'])


# In[3]:


word_data.head()


# In[4]:


stock_data.head()


# In[5]:


'''
print("Max stock data: {}".format(np.max(stock_data['date'])))
print("Max tweet date: {}".format(np.max(word_data['date'])))
'''


# In[6]:


# Accumulate tweets from weekends and holidays to the next open stock market day
'''
last_stock_date = np.max(stock_data['date'])
word_data.drop(labels=word_data.loc[word_data['date'] > last_stock_date], axis=1)
'''
while(pd.unique(word_data['date'].isin(stock_data['date'])).shape[0] > 1):
    word_data.loc[~word_data['date'].isin(stock_data['date']), 'date'] += dt.timedelta(days=1) 


# In[7]:


## Getting Percentage stock increase by word count

agg = pd.merge(stock_data, word_data, how='right', on='date', sort=True, suffixes=('_stock', '_word'))
agg.head()


# In[8]:


stats = pd.DataFrame(pd.unique(agg['word']), columns=['word'])
stats.head()


# In[9]:


# stats.loc[stats['word'] == 'no', 'count'] = 2
np.sum(agg.loc[agg['word'] == 'no', 'count'])

# LONG OPERATION:
stats['count'] = stats['word'].apply(lambda x: np.sum(agg.loc[agg['word'] == x, 'count']))


# In[10]:


stats['perc_inc'] = stats['word'].apply(lambda x: np.sum(agg.loc[(agg['word'] == x) & (agg['closeprice'] - agg['openprice'] >= 0), 'count']))
stats['perc_inc'] = stats.apply(lambda x: x['perc_inc'] / x['count'], axis=1)
stats.head()


# In[ ]:





# In[ ]:




