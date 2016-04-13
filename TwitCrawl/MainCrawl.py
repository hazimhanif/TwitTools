'''
Created on Mar 3, 2016

@author: Hazim
'''
import tweepy
import requests
import json
import os
import time
import sys
import codecs
import csv
from timeit import default_timer as timer
from lib2to3.fixer_util import Newline


#Global Instances    
global user_count
global user_id
global depth_num
global api
global path
global status
global maxid
global rev

#Instances initialization
rev=0
status=""
path=""
api=""
user_count=0
depth_num=0
user_id=""

#476625431 = Aisyah Syakirah
#447718618 = Mirza Khairuddin
#1021562084 = pidot

def oauth_connect():
    global api
    consumer_key="PcJE2NzulRd5ybchUHhMKm50x"
    consumer_secret="XeVGRKwFjHFsobO291xkNqaDlW2kLt32r52EABJ28VAaqr5UVz"
    access_token="473112171-OwYKT310UGyABB7pjA4Oq9MVlbBHu7IvL87Ufz82"
    access_token_secret="1fSEbRjZtmJnM2Y1BUwYXHqeq7VwvqRy2AkdtnUU4rKb1"
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.secure = True
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())


def depth_update():
    global depth_num
    depth_num += 1
    print(depth_num)
    
def get_user_init():
    global status
    global path
    global rev
    try:
        path = 'D:/Twitter/Depth-%d/%s' % (depth_num,str(user_id))
        try:
            os.makedirs(path)
        except FileExistsError:
            print("Folder already exist")
            status="skip"
            return
        
        data = api.get_user(user_id)
        if data['protected']==False:
            get_user(data)
            rev=1
        else:
            status="skip"
            print("Protected")
            
    except tweepy.RateLimitError:
        countdown(960)
        get_user_init()

    except tweepy.TweepError as e:
            if tweepy.TweepError is "[{'message': 'Over capacity', 'code': 130}]" or e[0]['code'] is 130:
                countdown_te(600,e)
                get_user_init()
            elif tweepy.TweepError is "[{'message': 'User not found.', 'code':50}]" or e[0]['code'] is 50:
                status="skip"
                return
            else:
                print(e)


def get_user(output_data_from_get_init):
    data = output_data_from_get_init
    path_local="%s/user_data.dump" % (path)
    with codecs.open(path_local,'wb','utf-8') as fp:
        json.dump(data,fp)
    
    fp.close()
    
    
def get_followers_list():
    path_local="%s/followers.txt" % (path)
    f=codecs.open(path_local,'w',"utf-8")
    for doc in limit_handler(tweepy.Cursor(api.followers_ids,id=user_id).pages()):
        for data in doc['ids']:
            f.write(str(data))
            f.write("\n")
            
    f.close()

def get_friends_list():
    path_local="%s/friends.txt" % (path)
    f=codecs.open(path_local,'w',"utf-8")
    for doc in limit_handler(tweepy.Cursor(api.friends_ids,id=user_id).pages()):
        for data in doc['ids']:
            f.write(str(data))
            f.write("\n")

    f.close()
    
def get_tweet():
    global maxid
    i_page=0
    path_local="%s/tweets.dump" % (path)
    try:
        tc=0
        data = api.user_timeline(id=user_id,count=200)
        with codecs.open(path_local,'wb','utf-8') as fp:
            for doc in data:
                json.dump(doc,fp)
                fp.write('\n')
                tc+=1
            i_page +=1
            
            if tc>195:
                while i_page<6:
                    tc=0
                    maxid=data[-1]['id_str']
                    data = api.user_timeline(id=user_id,max_id=maxid,include_rts=True,count=200)
                    for doc in data:
                            json.dump(doc,fp)
                            fp.write('\n')
                            tc+=1
                
                    i_page+=1
                    
                    if tc<196:
                        fp.close
                        return
            
            else:
                fp.close()
                return
        
        fp.close

    except tweepy.RateLimitError:
        countdown(960)
        
        if(i_page==0):
            get_tweet()
        else:
            fp.close
            
            with codecs.open(path_local,'ab','utf-8') as fp:
                while i_page<6:
                    tc=0
                    data = api.user_timeline(id=user_id,max_id=maxid,include_rts=True,count=200)
                    for doc in data:
                            json.dump(doc,fp)
                            fp.write('\n')
                            tc+=1
                
                    i_page+=1
                    maxid=data[-1]['id_str']
                    
                    if tc<196:
                        fp.close
                        return   
            
            fp.close
        
    except tweepy.TweepError as e:
            if tweepy.TweepError is "[{u'message': u'Over capacity', u'code': 130}]" or e is "[{u'message': u'Over capacity', u'code': 130}]":
                countdown_te(600,e)
                get_tweet()
            else:
                print(e)

 
def get_id(sn):
    try:
        return(api.get_user(screen_name=sn)['id'])
    except tweepy.RateLimitError:
        countdown(960)
        get_id(sn)
        
    except tweepy.TweepError as e:
            if tweepy.TweepError is "[{u'message': u'Over capacity', u'code': 130}]" or e is "[{u'message': u'Over capacity', u'code': 130}]":
                countdown_te(600,e)
                get_id(sn)
            else:
                print(e)


def limit_handler(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            countdown(960)
        except tweepy.TweepError as e:
            if tweepy.TweepError is "[{u'message': u'Over capacity', u'code': 130}]" or e is "[{u'message': u'Over capacity', u'code': 130}]":
                countdown_te(600,e)
            else:
                print(e)
            
def countdown(t): # in seconds
    for i in range(t,0,-1):
        print('Rate Limit Exceeded(error 88),for user number',user_count,' now sleeping for',i,' seconds')
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')

def countdown_te(t,e): # in seconds
    for i in range(t,0,-1):
        print(e,' error,for user number',user_count,' now sleeping for',i,' seconds')
        time.sleep(1)
        os.system('cls' if os.name == 'nt' else 'clear')
                  
def start_crawl():
    global user_count
    global status
    user_count += 1
    logo()
    print("Current depth: ",depth_num)
    print("Current user count: ",user_count)
    print("Current user ID: ",user_id)
    print("Get user info:")
    get_user_init()
    print("[DONE]")
    
    if rev==0:
        user_count += 1
    
    if status=="skip":
        user_count = user_count - 1
        status=""
        return
    
    print("Get followers list:")
    get_followers_list()
    print("[DONE]")
    
    print("Get tweet list:")
    get_tweet()
    print("[DONE]")

    print("Get friends list:")
    get_friends_list()
    print("[DONE]")
 
        
def init_crawl():

    global user_id
    logo()
    oauth_connect()
    user_id=str(get_id(input("Enter the 'seed' Twitter screen name: ")))
    print("Crawl starting..")
    start = timer()
    start_crawl()
    depth_update()
    
    while depth_num <3:
        dir_path = 'D:/Twitter/Depth-%d' % (depth_num-1)
        for filename in os.listdir(dir_path):
            if str(filename) == ".DS_Store":
                continue
            else:
                try:
                    path_file = '%s/%s/followers.txt' % (dir_path,filename)
                    file = open(path_file, 'r')
                    for id in file:
                        id_temp = str(id)
                        user_id=id_temp[:-1]
                        os.system('cls' if os.name == 'nt' else 'clear')
                        start_crawl() 
                    
                    file.close()
                except FileNotFoundError:
                    continue
                    
        depth_update()
    
    end = timer()
    print("\n\n Crawl finished. The time elapsed is: %s" % str(end - start))
    print("Total number of user: %d" % user_count)

def logo():
    print("=================Welcome to TwitCrawl 1.0=================")
    print("__________________________________________________________")
    print("_++++++++++++++___________++_______+++____________________")
    print("______++_______________++______________+++________________")
    print("______++_____________++__________________+++______________")
    print("______++__________++______________________++______________")
    print("______++____________++_____________+++++++________________")
    print("______++______________++_________________+++______________")
    print("______++________________++________________++______________")
    print("______++_________________++_________++++++________________")
    print("__________________________________________________________")
    print("=====================By @hazimfrodo=======================")
    print("\n")

def welcome():
    
    logo()
    print("Please choose your next action (number):-")
    print("1. Looking for someone's ID ?")
    print("2. CRAWLLLINGGG IN MYY SKINNNN!!! ")
    
    if (int(input())==1):
        print("The user ID is", str(get_id(input("Enter the desired Twitter user screen name(@thisname): "))))
        print("\n")
        print("Do you want to continue? (Y/N)")
        input_local=input()
        if input_local=='Y' or input_local=='y':
            os.system('cls' if os.name == 'nt' else 'clear')
            welcome()
        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            sys.exit()
    
    else:
        os.system('cls' if os.name == 'nt' else 'clear')
        init_crawl()


oauth_connect()
welcome()
# get_user_init()
#get_tweet()
# get_followers_list()   
# get_friends_list() 
#depth_update()
#print(get_id('fami5143'))

# kk=0
# data=api.user_timeline(id=3942319513,count=150)
# for doc in data:
#     print(doc)
#     kk+=1
# 
# print(kk)
    
# with open('D:/user.dump','w') as outfile:
#     json.dump(data,outfile)
# outfile.close

# os.makedirs('D:/a/b/c')
# f=open('D:/a/z.txt','w')
# f.write('a')
# f.write('\n')
# f.write('b')
# f.close
#704380966534418432

# # Reserved codes for future references
#     data_dumps=json.dumps(api.get_user(user_id))
#     data=json.loads(data_dumps)
