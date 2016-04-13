'''
Created on Mar 21, 2016

@author: Hazim
'''

import json
import codecs
import os
import shutil
import webbrowser
import requests
from collections import Counter


global depth
global dir_id
global counter
global url_link

url_link=""
depth=0
counter=0
dir_id=""


def init_auto():
    global dir_id
    global depth
    global counter
    while depth<3:
        dir_depth = 'D:/Twitter/Depth-%d' % depth
        list_dir = os.listdir(dir_depth)
        for doc in list_dir:
            counter +=1
            dir_id = '%s/%s' % (dir_depth,str(doc))
            
            skip=clean(doc)
            if skip == True:
                continue;
            
            res=check_file()
            if res == True:
                continue;
            
            print("User number: ",counter)
            print("User id: ",str(doc))
            print("Depth: ",depth)
            if(input("Get Info? (y/n) : ")=='y'):
                os.system('cls' if os.name == 'nt' else 'clear')
                xtract_user_data()
                xtract_tweet()
                check_url()
                decision(doc)
                print()
                print("----------------Done for user: ",doc)
                print()
            else:
                print("Program End ! ")
                return
            
        depth +=1

def xtract_tweet():
    global url_link
    url_link=""
    try:
        url_count=0
        c=0
        dir_tweet = '%s/tweets.dump' % dir_id
        print("----Tweets--------")
        jfile = codecs.open(dir_tweet,'rb','utf-8')
        for jdoc in jfile:
            jobj = json.loads(jdoc)
            list_url = jobj['entities']['urls']
            print("Tweet: "+ jobj['text'])
            print("Source Device: "+ jobj['source'])
            for url in list_url:
                print("URL: " + url['expanded_url'])
            print()
            c+=1
            if c==100:
                break
        jfile.close()
        
        jfile2 = codecs.open(dir_tweet,'rb','utf-8')
        for jdoc in jfile2:
            jobj = json.loads(jdoc)
            list_url = jobj['entities']['urls']
            for url in list_url:
                url_link = url_link + str(url['expanded_url'])+"\n"
                url_count+=1
                
        
        url_link = "%d\n%s" %(url_count,url_link)
        jfile2.close()
        print("URL Count :",url_count)
    except FileNotFoundError as e:
        print(e, " in extract tweets")

def xtract_user_data():

    try:
        dir_user_profile = '%s/user_data.dump' % dir_id
        jfile = codecs.open(dir_user_profile,'rb','utf-8')
        for jdoc in jfile:
            jobj = json.loads(jdoc)
            print()
            print("-----User Info------")
            print("Name: "+ jobj['name'])
            print("Screen Name: "+ jobj['screen_name'])
            print("Created At: " +jobj['created_at'])
            print("Friends count: "+ str(jobj['friends_count']))
            print("Followers Count: "+str(jobj['followers_count']))
            print("Favourites Count: "+str(jobj['favourites_count']))
            print("Status Count: "+str(jobj['statuses_count']))
            print()
            url="http://www.twitter.com/%s" % jobj['screen_name']
            
            if input("Open URL ? (y/n)") == "y":
                webbrowser.open(url, new=0, autoraise=True)
    
        jfile.close()
        
    except FileNotFoundError as e:
        print(e, " in extract user data")
    
def decision(doc):
    inp = "o"
    while not("h" is inp or "b" is  inp or "c" is inp or "d" is inp) :
        inp = input("Please classify: Bot(b), Cyborg(c), Human(h), Drop(d): ")
     
    if inp=="b":
        dir_temp = "%s/bot" % dir_id   
        f = open(dir_temp,"wb")
        f.close()
        list_l = os.listdir(dir_id)
        dst_dir = "D:/Classify/Bot/%s" % doc
        os.makedirs(dst_dir)
        for file in list_l:
            src_f = "%s/%s" %(dir_id,file)
            dst_f = "%s/%s" %(dst_dir,file)
            shutil.move(src_f, dst_f)
        os.rmdir(dir_id)


    elif inp=="c":   
        dir_temp = "%s/cyborg" % dir_id   
        f = open(dir_temp,"wb")
        f.close()
        list_l = os.listdir(dir_id)
        dst_dir = "D:/Classify/Cyborg/%s" % doc
        os.makedirs(dst_dir)
        for file in list_l:
            src_f = "%s/%s" %(dir_id,file)
            dst_f = "%s/%s" %(dst_dir,file)
            shutil.move(src_f, dst_f)
        os.rmdir(dir_id)           

    elif inp=="h":   
        dir_temp = "%s/human" % dir_id   
        f = open(dir_temp,"wb")
        f.close()
        list_l = os.listdir(dir_id)
        dst_dir = "D:/Classify/Human/%s" % doc
        os.makedirs(dst_dir)
        for file in list_l:
            src_f = "%s/%s" %(dir_id,file)
            dst_f = "%s/%s" %(dst_dir,file)
            shutil.move(src_f, dst_f)
        os.rmdir(dir_id)       

    else:   
        dir_temp = "%s/drop" % dir_id   
        f = open(dir_temp,"wb")
        f.close()
        list_l = os.listdir(dir_id)
        dst_dir = "D:/Classify/Drop/%s" % doc
        os.makedirs(dst_dir)
        for file in list_l:
            src_f = "%s/%s" %(dir_id,file)
            dst_f = "%s/%s" %(dst_dir,file)
            shutil.move(src_f, dst_f)
        os.rmdir(dir_id)   

def clean(doc):
    list_file = os.listdir(dir_id)
    if not("followers.txt" in list_file and "friends.txt" in list_file and "tweets.dump" in list_file and "user_data.dump" in list_file):
        dir_temp = "%s/drop" % dir_id   
        f = open(dir_temp,"wb")
        f.close()
        dst_dir = "D:/Classify/Drop/%s" % doc
        os.makedirs(dst_dir)
        for file in list_file:
            src_f = "%s/%s" %(dir_id,file)
            dst_f = "%s/%s" %(dst_dir,file)
            shutil.move(src_f, dst_f)
        os.rmdir(dir_id)
        return True   
    else:
        return False


def check_file():
    list_file = os.listdir(dir_id)
    if("bot" in list_file or "cyborg" in list_file or "human" in list_file or "drop" in list_file):
        return True
    else:
        return False

def check_url():
    data = url_link
    url= 'https://sb-ssl.google.com/safebrowsing/api/lookup?client=python&key=AIzaSyA1M7fY7G432oC9x2tdytCDWb86yAbrz0s&appver=0.2&pver=3.1'
    r= requests.post(url,data)
    print("URL Status Code: ",r.status_code)
    
    wordcount = Counter(r.text.split())
    for item in wordcount.items():
        print("{}\t{}".format(*item))
    


#Start the extractor
init_auto()



