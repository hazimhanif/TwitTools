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
global counter_human
global counter_bot
global counter_cyborg
global counter_drop
global url_link
global url_profile

url_profile=""
url_link=""
depth=0
counter=0
counter_human=0
counter_bot=0
counter_cyborg=0
counter_drop=0
dir_id=""


def init_auto():
    global dir_id
    global depth
    global counter
    global counter_human
    global counter_bot
    global counter_cyborg
    global counter_drop
    global url_profile
    
    dir_count()
    while depth<3:
        dir_depth = 'D:/Twitter/Depth-%d' % depth
        list_dir = os.listdir(dir_depth)
        for doc in list_dir:
            counter +=1
            dir_id = '%s/%s' % (dir_depth,str(doc))

            print("------------Classification Counter---------------")
            print("Human  : ", counter_human)
            print("Bot    : ", counter_bot)
            print("Cyborg : ", counter_cyborg)
            print("Drop   : ", counter_drop)
            print("------------------------------------------------")
            print("")
            print("User number: ",counter)
            print("User id    : ",str(doc))
            print("Depth      : ",depth)
            if(input("Get Info? (y/n) : ")=='y'):
                os.system('cls' if os.name == 'nt' else 'clear')
                xtract_user_data()
                xtract_tweet()
                check_url()
                
                if input("Open URL ? (y/n): ") == "y":
                    webbrowser.open(url_profile, new=0, autoraise=True)


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
        print("-------------------Tweets-----------------------------")
        jfile = codecs.open(dir_tweet,'rb','utf-8')
        for jdoc in jfile:
            jobj = json.loads(jdoc)
            list_url = jobj['entities']['urls']
            print("Tweet        : "+ jobj['text'])
            print("Source Device: "+ jobj['source'])
            for url in list_url:
                print("URL          : " + url['expanded_url'])
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
                
            if url_count> 490:
                break
                
        
        url_link = "%d\n%s" %(url_count,url_link)
        jfile2.close()
        print("URL Count :",url_count)
    except FileNotFoundError as e:
        print(e, " in extract tweets")

def xtract_user_data():
    global url_profile
    try:
        dir_user_profile = '%s/user_data.dump' % dir_id
        jfile = codecs.open(dir_user_profile,'rb','utf-8')
        for jdoc in jfile:
            jobj = json.loads(jdoc)
            print()
            print("-----------------User Info---------------------------")
            print("Name            : "+ jobj['name'])
            print("Screen Name     : "+ jobj['screen_name'])
            print("Created At      : " +jobj['created_at'])
            print("Friends count   : "+ str(jobj['friends_count']))
            print("Followers Count : "+str(jobj['followers_count']))
            print("Favourites Count: "+str(jobj['favourites_count']))
            print("Status Count    : "+str(jobj['statuses_count']))
            print()
            url_profile="http://www.twitter.com/%s" % jobj['screen_name']
            
    
        jfile.close()
        
    except FileNotFoundError as e:
        print(e, " in extract user data")
    
def decision(doc):
    try:
        global counter_human
        global counter_bot
        global counter_cyborg
        global counter_drop
        check=""
        inp = "o"
        while not("h" is inp or "b" is  inp or "c" is inp or "d" is inp) :
            inp = input("Please classify: Bot(b), Cyborg(c), Human(h), Drop(d): ")
         
        if inp=="b":
            dir_temp = "%s/bot" % dir_id   
            f = open(dir_temp,"wb")
            f.close()
            list_l = os.listdir(dir_id)
            dst_dir = "D:/Classify/Bot/%s" % doc
            check="bot"
            os.makedirs(dst_dir)
            for file in list_l:
                src_f = "%s/%s" %(dir_id,file)
                dst_f = "%s/%s" %(dst_dir,file)
                shutil.move(src_f, dst_f)
            os.rmdir(dir_id)
            counter_bot +=1
    
    
        elif inp=="c":   
            dir_temp = "%s/cyborg" % dir_id   
            f = open(dir_temp,"wb")
            f.close()
            list_l = os.listdir(dir_id)
            dst_dir = "D:/Classify/Cyborg/%s" % doc
            check="cyborg"
            os.makedirs(dst_dir)
            for file in list_l:
                src_f = "%s/%s" %(dir_id,file)
                dst_f = "%s/%s" %(dst_dir,file)
                shutil.move(src_f, dst_f)
            os.rmdir(dir_id)
            counter_cyborg +=1           
    
        elif inp=="h":   
            dir_temp = "%s/human" % dir_id   
            f = open(dir_temp,"wb")
            f.close()
            list_l = os.listdir(dir_id)
            dst_dir = "D:/Classify/Human/%s" % doc
            check="human"
            os.makedirs(dst_dir)
            for file in list_l:
                src_f = "%s/%s" %(dir_id,file)
                dst_f = "%s/%s" %(dst_dir,file)
                shutil.move(src_f, dst_f)
            os.rmdir(dir_id)
            counter_human +=1       
    
        else:   
            dir_temp = "%s/drop" % dir_id   
            f = open(dir_temp,"wb")
            f.close()
            list_l = os.listdir(dir_id)
            dst_dir = "D:/Classify/Drop/%s" % doc
            check="drop"
            os.makedirs(dst_dir)
            for file in list_l:
                src_f = "%s/%s" %(dir_id,file)
                dst_f = "%s/%s" %(dst_dir,file)
                shutil.move(src_f, dst_f)
            os.rmdir(dir_id)
            counter_drop +=1
            
    except FileExistsError:
        a= "File already exist in %s. Are you sure you want to delete the user %s ? (y/n): " % (check,doc)
        inp = input(a)
        if inp=="y":
            shutil.rmtree(dir_id)
        else:
            return
        
def check_url():
    try:
        data = url_link
        url= 'https://sb-ssl.google.com/safebrowsing/api/lookup?client=python&key=AIzaSyA1M7fY7G432oC9x2tdytCDWb86yAbrz0s&appver=0.2&pver=3.1'
        r= requests.post(url,data)
        print("URL Status Code: ",r.status_code)
        
        wordcount = Counter(r.text.split())
        for item in wordcount.items():
            print("{}\t{}".format(*item))
    except Exception as e:
        print("Cannot proceed for URL checking because: ",e)
        print("")
        
    
def dir_count():
    global counter
    global counter_human
    global counter_bot
    global counter_cyborg
    global counter_drop

    counter_bot = len(os.listdir("D:/Classify/Bot/"))
    counter_human = len(os.listdir("D:/Classify/Human/"))
    counter_cyborg = len(os.listdir("D:/Classify/Cyborg/"))
    counter_drop = len(os.listdir("D:/Classify/Drop/"))

    counter = counter_bot + counter_human + counter_cyborg + counter_drop
    
#Start the extractor
init_auto()



