# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 15:32:16 2018

@author: Leo
"""
'''
 .contents可以查看tag中所有的子项
'''
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

def getHTMLText(url):
       try:
              r = requests.get(url)
              r.raise_for_status()
              r.encoding = r.apparent_encoding
              return r
       except:
              return ""

input_path = r'C:\Users\Administrator\Desktop\chouchoubao\ProCode.csv'
ret_path = r'C:\Users\Administrator\Desktop\chouchoubao\BasicInfo.csv'

df = pd.read_csv(input_path, encoding='utf-8', dtype={'Project_Code':str})

df.dropna(axis=0, how='any', inplace=True)
df['Target'] = 'NaN'
df['Actual'] = 'NaN'
df['Progress'] = 'NaN'
df['Backers'] = 'NaN'
df['Comments'] = 'NaN'

df = df[:20]

start_time = time.time()
for i in range(len(df)):
       url = df['Website'][i]
       html = getHTMLText(url).text
       try:
              soup = BeautifulSoup(html, 'html.parser')
              
              target = soup.find_all(attrs={'class':'brokersText-1-1 pb30'})[0].string
              df.at[i, 'Target'] = target
              
              actual = soup.find_all(attrs={'class':'brokercount'})[-1].string
              df.at[i, 'Actual'] = actual
              
              progress = soup.find_all(attrs={'class':'progress-content'})[-1].string
              df.at[i, 'Progress'] = progress
              
              backers = soup.find_all(attrs={'class':'brokercount'})[-2].string
              df.at[i, 'Backers'] = backers
              
              comments = soup.find_all(attrs={'id':'tab3'})[0].span.string
              df.at[i, 'Comments'] = comments
              
              time.sleep(0.5)
              end_time = time.time()
              remain_time = (end_time - start_time) / (i + 1) * (len(df) - (i + 1))
              print("\r{:>6.2f}% Done, Time Remained: {:04}:{:02}:{:02}".format(
                     (i + 1) * 100 / len(df), int(remain_time // 3600), 
                     int(remain_time // 60 % 60), int(remain_time % 60)),
              end="")
       except:
              continue
df.to_csv(ret_path, encoding='utf-8', index=False)