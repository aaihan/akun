#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np


# In[3]:


df = pd.read_excel('house_kg.xlsx')
df.columns


# In[4]:


df.drop(['Телефон', 'Санузел', 'Канализация',
       'Питьевая вода', 'Электричество', 'Газ'], axis=1, inplace=True)


# In[ ]:


df.head()


# In[ ]:


df.shape


# In[ ]:


df.info()


# In[ ]:


df.describe()


# In[5]:


col = df.columns
col_res = [i for i in col if (df[i].notnull().sum()/df.shape[0]) > 0.3]


# In[6]:


df = df[col_res]


# In[ ]:





# In[7]:


df.dropna(subset = ['Площадь участка'], inplace = True)


# In[8]:


df['Площадь участка'] = [float(i.split()[0]) for i in df['Площадь участка']]


# In[9]:


df['Площадь участка'].describe()


# In[ ]:





# In[ ]:





# In[10]:


df['Price_sq'] = df['USD_price']/df['Площадь участка']
dfn = df[ (df['Price_sq']>df['Price_sq'].quantile(0.1)) & (df['Price_sq']<df['Price_sq'].quantile(0.9)) ]


# In[11]:


col_com = ['газ','свет','канализация','вода','отопление']
dfn['Коммуникации'] = dfn['Коммуникации'].fillna('0')

for col in col_com:
  dfn[col.capitalize()] = dfn['Коммуникации'].map(lambda i: 1 if col in i else 0)
dfn.info()


# In[ ]:





# In[ ]:





# In[ ]:





# In[12]:


dfn['describe'].fillna('0',inplace = True)
dfn['документы'] = [1 if 'красная книга' in i.lower() or 'кызыл китеп' in i.lower() or 'зеленая книга' in i.lower() else 0 for i in dfn['describe']]
dfn.head


# In[13]:


dfn[dfn['документы']==1].shape


# In[ ]:





# In[ ]:





# In[14]:


dfn.groupby('Газ').agg({'USD_price':['mean','median'], 'Price_sq':['mean','median']})


# In[15]:


dfn.columns


# In[16]:


dfn.groupby('Канализация').agg({'USD_price':['mean','median'], 'Price_sq':['mean','median']})


# In[ ]:





# In[ ]:





# In[ ]:





# In[17]:


q1 = df.Price_sq.quantile(.33)
q2 = df.Price_sq.quantile(.66)
bins = [df.Price_sq.min(),q1,q2,df.Price_sq.max()]
labels = ['cheap','medium','expensive']


# In[18]:


dfn['Category'] = pd.cut(df.Price_sq, bins = bins, labels = labels)


# In[ ]:





# In[ ]:





# In[19]:


dfn.groupby('Category',as_index = False).agg({'Площадь участка':['mean','median']})


# In[ ]:





# In[20]:


df.groupby('Тип предложения',as_index=False).agg({'USD_price':['mean','median'], 'Price_sq':['mean','median']})


# In[ ]:


#from agent more expensive


# In[ ]:





# In[21]:


dfn.columns


# In[22]:


dfn['exchange rate'] = dfn['KGS_price ']/dfn['USD_price']


# In[ ]:


dfn['exchange rate']


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:


#visualization


# In[26]:


df.columns


# In[65]:


import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

import seaborn as sns

fig, ax = plt.subplots(2,1,figsize=(4,5))
sns.histplot(data = dfn, y ='Category', ax = ax[0])
sns.histplot(data = dfn, y = 'Местоположение', ax = ax[1])


# In[71]:


nom_col = ['Газ','Свет','Канализация','Вода','Отопление','документы']
icount = [dfn[i].sum() for i in nom_col]
df0 = pd.DataFrame({'communication':nom_col,'count':icount})
df0.sort_values('count',ascending = False, inplace = True)


# In[76]:


plt.subplots(figsize=(4,4))
sns.barplot(data = df0, x = 'count',y = 'communication')


# In[78]:


plt.subplots(figsize=(15,4))
sns.boxplot(data = dfn, x = 'USD_price', y = 'Местоположение')


# In[79]:


plt.subplots(figsize=(15,4))
sns.boxplot(data = dfn, x = 'Price_sq', y = 'Category')


# In[84]:


f, ax = plt.subplots(figsize = (10,5))
sns.scatterplot(x = dfn.USD_price, y = dfn['Площадь участка'], hue = dfn['Местоположение'])


# In[86]:


sns.lmplot(data = dfn, x = 'USD_price', y = 'Площадь участка',hue = 'Category')


# In[96]:


df1 = dfn.groupby('Местоположение', as_index = False).agg({'Price_sq':'mean'}).sort_values('Price_sq',ascending = False)
sns.barplot(data = dfn ,x ='Price_sq',y = 'Местоположение' )


# In[99]:


cm = dfn.corr()
sns.heatmap(cm)


# In[101]:


pd.get_dummies(dfn['Местоположение'])


# In[106]:


#dfn = pd.concat([dfn,pd.get_dummies(dfn['Местоположение'])],axis = 1).drop('Местоположение', axis = 1)
dfn.columns


# In[109]:


sns.heatmap(dfn.corr())

