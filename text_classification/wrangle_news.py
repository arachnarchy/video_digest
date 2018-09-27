#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 10:00:41 2018

@author: daniel
"""

import pandas as pd
import numpy as np

news1 = pd.read_csv('all-the-news/articles1.csv')
news2 = pd.read_csv('all-the-news/articles2.csv')
news3 = pd.read_csv('all-the-news/articles3.csv')

news_all = news1.append([news2, news3])

## Enter labels and keep only those and the content
right = ['Breitbart', 'Fox News', 'New York Post', 'National Review']
left = ['New York Times', 'Vox', 'Buzzfeed News', 'Talking Points Memo']

news_l = news_all[news_all.publication.isin(left)]
news_r = news_all[news_all.publication.isin(right)]

news_l['label'] = 'left'
news_r['label'] = 'right'

# Only keep min number for each publication
news_l.groupby(['publication'])['label'].count()
news_r.groupby(['publication'])['label'].count()

news_set = pd.concat([news_l, news_r])

nyt = news_set[news_set.publication == 'New York Times'].sample(4000)
vox = news_set[news_set.publication == 'Vox'].sample(4000)
bfn = news_set[news_set.publication == 'Buzzfeed News'].sample(4000)
tpm = news_set[news_set.publication == 'Talking Points Memo'].sample(4000)

bbt = news_set[news_set.publication == 'Breitbart'].sample(4000)
fxn = news_set[news_set.publication == 'Fox News'].sample(4000)
nyp = news_set[news_set.publication == 'New York Post'].sample(4000)
nrv = news_set[news_set.publication == 'National Review'].sample(4000)

news_equal = pd.concat([nyt,vox,bfn,tpm,bbt,fxn,nyp,nrv])

news = news_equal.filter(['label','content'], axis=1)
#news.label.replace('left', 0, inplace=True)
#news.label.replace('right', 1, inplace=True)
news.reset_index(drop=True,inplace=True)

news.to_csv('news.csv')