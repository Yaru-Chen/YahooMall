# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 22:32:26 2018

@author: user
"""

import jieba.posseg as pseg
import json
import re
import pandas as pd
import numpy as np

data = pd.read_csv('C:/Users/user/Desktop/mall.csv')
data = data[data['num']>0]
output = pd.DataFrame()
for c in data['category'].unique():
    datatmp = data[data['category']==c].reset_index()
    datatmp['tmp'] = datatmp['title'].apply(lambda x:pseg.cut(x)) #jieba.cut_for_search(x)
    hash_adj = {}; hash_n = {}
    for r in np.arange(datatmp.shape[0]):
        seg_list = datatmp.loc[r,'tmp']
        for i in seg_list:
            if (i.flag in ['Ag','a']) and (i.word in hash_adj):
                hash_adj[i.word] += datatmp.loc[r,'num']
            elif (i.flag in ['Ag','a']):
                hash_adj[i.word] = datatmp.loc[r,'num']
            elif (i.flag in ['an','Ng','n','ns','nr','nt','nz']) and (i.word in hash_n):
                hash_n[i.word] += datatmp.loc[r,'num']
            elif (i.flag in ['an','Ng','n','ns','nr','nt','nz']):
                hash_n[i.word] = datatmp.loc[r,'num']
                
    if hash_n!={}:
        df_n = pd.DataFrame({'category':c,'key':list(hash_n.keys()), 'count':list(hash_n.values())})
        df_n['key'] = df_n['key'].apply(lambda x:re.sub('[A-Za-z0-9\！\=\*\＊\、\＋\:\;\–\?\|\$\▼\!\■\『\』\，\☆\↘\‧\~\《\》\[\]\ ◤\◢\’\．\／\/\【\】\(\)\+\#\◆\★\.\s-]', '', x))
        df_n = df_n[(df_n['key']!='') & (df_n['count']>0)].sort_values(['count'],ascending = False).reset_index()
        df_n['parts'] = 'n'
        output = output.append(df_n.loc[np.arange(min(df_n.shape[0],15)),['category','key','count','parts']])
        
    if hash_adj!={}:
        df_adj = pd.DataFrame({'category':c,'key':list(hash_adj.keys()), 'count':list(hash_adj.values())})
        df_adj['key'] = df_adj['key'].apply(lambda x:re.sub('[A-Za-z0-9\！\=\*\＊\、\＋\:\;\–\?\|\$\▼\!\■\『\』\，\☆\↘\‧\~\《\》\[\]\ ◤\◢\’\．\／\/\【\】\(\)\+\#\◆\★\.\s-]', '', x))
        df_adj = df_adj[(df_adj['key']!='') & (df_adj['count']>0)].sort_values(['count'],ascending = False).reset_index()
        df_adj['parts'] = 'adj'
        output = output.append(df_adj.loc[np.arange(min(df_adj.shape[0],10)),['category','key','count','parts']])
    
    
output.to_csv('BestSellItem.csv', index=False, encoding='cp950')