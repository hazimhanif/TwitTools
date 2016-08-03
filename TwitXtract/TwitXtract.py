'''
Created on Jul 15, 2016

@author: Hazim
'''

'''
Created on Jun 23, 2016

@author: Hazim
'''


import json
import codecs
import os
import pandas as pd
from pandas.io.json import json_normalize

global features_list
global features_df
global row_count
global label

global colnames
global c

c=0
colnames=[]
label=""
row_count=0

def start():
    global label
    global features_df
    
    features_df = pd.DataFrame()
    
    dir = 'D:/Classify'
    for category in os.listdir(dir):
        if (category=="Blacklist") or (category=="Drop") or (category=="Human") or (category=="Cyborg"):
            continue
        
        label=category
        dir_category = "D:/Classify/%s" % category
        getfolder(dir_category)

def getfolder(dir_category):
    global features_df
    global c
    
    c=0
    for folder in os.listdir(dir_category):
        c+=1
        gettweets(folder,dir_category)
        
        ## C is the number of user
        if c==1:
            break
    
    col = list(features_df.columns.values)
    user_matching = [s for s in col if "user" in s[0:4]]
    tweet_matching = [s for s in col if "tweet" in s[0:5]]
    user_matching.remove('user_id')
    new_col = ['user_id']+user_matching+tweet_matching+['label']
    
    features_df = features_df[new_col]
    features_df.to_csv("D:/dataset_bot_testset.csv",index=False)
    

def gettweets(folder,dir_category):
    global features_list
    global features_df
    global row_count

    filename = "%s/%s/tweets.dump" % (dir_category,folder)
    jfile = codecs.open(filename,'rb','utf-8')
    
    break_counter =0 
    
    for jdoc in jfile:
        print("User: ",c," - Tweets : ",row_count)

        ##break counter is tweet count
        if break_counter==100:
            break

        jvar = json.loads(jdoc)
        
        flat = flatten_json(jvar)
        norm=json_normalize(flat)
        
        features_df = pd.concat([features_df, norm], ignore_index=True)
        break_counter+=1

        if "label" not in list(features_df):
            features_df['label'] = str("NA")
        
        features_df.loc[row_count,'label']=label
        features_df.fillna("NA",inplace=True)
        
        row_count+=1
    
def flatten_json(y):
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            if "user" != name[0:4]:
                name="tweet_%s" % name
                
            out[str(name[:-1])] = str(x)

    flatten(y)
    return out

start()
