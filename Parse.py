#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from bs4 import BeautifulSoup


# In[ ]:


url = 'https://www.house.kg/kupit-kvartiru?'

# Отправляем GET-запрос на сервер
response = requests.get(url)

# Парсим HTML-код страницы с помощью BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Находим все элементы объявлений на странице
objects = soup.find("div", class_="listings-wrapper")
objects.find_all('div', class_ = 'left-image')

lincs = objects.find_all('div', class_ = 'left-image')
sub_url = []
for i in lincs:
  sub_url.append(i.find('a')['href'])

urls = []
for i in sub_url:
  urls.append("https://www.house.kg" + i)


# In[ ]:


url = ''
allPage = ['https://www.house.kg/kupit-kvartiru?']
for i in range(1,1001):
  allPage.append('https://www.house.kg/kupit-kvartiru?page='+str(i))

sub_url = []
urls = []
for i in allPage:
  url = i
  response = requests.get(url)
  soup = BeautifulSoup(response.text, "html.parser")
  objects = soup.find("div", class_="listings-wrapper")
  lincs = objects.find_all('div', class_ = 'left-image')

  for j in lincs:
    sub_url.append(j.find('a')['href'])
  for q in sub_url:
    if ("https://www.house.kg" + q) not in urls:
      urls.append("https://www.house.kg" + q)


lDict = []
for i in urls:
  url1 = i
  var = requests.get(url1)
  var1 = BeautifulSoup(var.text, "html.parser")
  objc = var1.find_all('div',class_="info-row")
  labeL = []
  s = []
  for i in objc:
    labeL.append(i.find('div',class_='label').text.strip())
  for i in objc:
    s.append(i.find('div',class_='info').text.strip())
  mdict = {i:j for i,j in zip(labeL,s)}
  if 'Безопасность' in mdict:
    mdict['Безопасность'] = mdict['Безопасность'].replace(' ','').replace('кодовыйзамок','кодовый замок').replace('решеткинаокнах','решетки на окнах').split(',')
  if 'Разное' in mdict:
    mdict['Разное'] = mdict['Разное'].replace(' ','').replace('пластиковыеокна','пластиковые окна').replace('пудобноподбизнес','удобно под бизнес').replace('новаясантехника','новая сантехника').replace('неугловая','неугловая').replace('комнатыизолированы','комнаты изолированы').replace('встроеннаякухня','встроенная кухня').replace('кладовка','кладовка').replace('тихийдвор','тихий двор').split(',')
  lDict.append(mdict)


# In[ ]:


lDict


# In[ ]:


import pandas as pd
import numpy as np
df = pd.DataFrame(lDict)
df.to_csv('housekg.csv', index=False)


# In[ ]:




