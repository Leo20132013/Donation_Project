# -*- coding: utf-8 -*-
"""
Created on Sat Sep 15 18:48:24 2018

@author: Leo
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import math
import time

def getHTMLText(url, data):
    try:
        r = requests.post(url, data=data)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r
    except:
        return ""

input_path = r'C:\Users\Administrator\Desktop\chouchoubao\BasicInfo.csv'
ret_path = r'C:\Users\Administrator\Desktop\chouchoubao\Backers_Detail.csv'

url_comment = 'https://gogetfunding.com/wp-content/themes/ggf/fpage/fajx.php'

df = pd.read_csv(input_path, encoding='utf-8', dtype={'Project_Code':str, 'Comments':str})

df = df[:1]

records = []
for i in range(len(df)):
    dic = {}
    dic['step'] = 'get_more_blog_msg_commnets'
    dic['lang'] = 'en'
    dic['pre'] = df['Project_Code'][i]
    MaxPage = math.ceil(int(df['Comments'][i])/10)
    for j in range(1, MaxPage+1):
        dic['page'] = j
        html = getHTMLText(url_comment, dic).text
        try:
            soup = BeautifulSoup(html, 'html.parser')
            tag = soup.find_all(attrs={'class':'row'})
            for k in range(len(tag)):
                try:
                    project_code_order = df['Project_Code'][i]+'|'+str((j-1)*10+k+1)
                    comment_id = tag[k]['id']
                    amount_date = tag[k].find_all('p')[-1].string

                    records.append((project_code_order, comment_id, amount_date))
                except:
                    continue
            time.sleep(0.2)
        except:
            continue
    print("\r{:>6.2f}% Done".format((i + 1) * 100 / len(df)), end="")

comt = pd.DataFrame(records, columns=['Pro_Code_Order','Comment_Id','Amount_Date'])
comt.to_csv(ret_path, encoding='utf-8', index=False)
