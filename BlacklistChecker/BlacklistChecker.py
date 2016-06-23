'''
Created on Jun 10, 2016

@author: Hazim
'''
import json
import codecs
import os
import shutil
import requests
from collections import Counter


global depth
global dir_id
global counter
global counter_blacklist
global url_link
global url_profile
global total_list
global google_status
global phishtank_status
global urlblacklist_status

url_profile=""
url_link=""
total_list=[]
depth=1
counter=0
counter_blacklist=0
dir_id=""
google_status = False
phishtank_status = False
urlblacklist_status = False

def init_auto():
    global dir_id
    global depth
    global counter
    global counter_blacklist
    global url_profile
    global google_status
    global phishtank_status
    global urlblacklist_status
    
    while depth<3:
        dir_depth = 'D:/Twitter/Depth-%d' % depth
        list_dir = os.listdir(dir_depth)
        for doc in list_dir:
            ## Initialize/Reset the condition flags.
            google_status = False
            phishtank_status = False
            urlblacklist_status = False
            dir_count()
            counter +=1
            dir_id = '%s/%s' % (dir_depth,str(doc))
            os.system('cls' if os.name == 'nt' else 'clear')
            print("------------Classification Counter---------------")
            print("Blacklist     : ", counter_blacklist)
            print("------------------------------------------------")
            print("")
            print("User number: ",counter)
            print("User id    : ",str(doc))
            print("Depth      : ",depth)
            xtract_url()
            google_safebrowsing() #Check Google Safe Browsing
            if decision(doc)==True:
                continue
            
            phishtank() #Check Phishtank
            if decision(doc)==True:
                continue
            
            urlblacklist() #Check UrlBlackList
            if decision(doc)==True:
                continue
        
        depth +=1

def xtract_url():
    global url_link
    global total_list
    total_list = []
    url_link=""
    try:
        url_count=0
        c=0
        dir_tweet = '%s/tweets.dump' % dir_id
        jfile2 = codecs.open(dir_tweet,'rb','utf-8')
        print("Extracting URL from tweets.... (Max: 490)")
        print("Resolving URL......")
        for jdoc in jfile2:
            jobj = json.loads(jdoc)
            list_url = jobj['entities']['urls']
            for url in list_url:
                #try:
                #    r = requests.get(url['expanded_url'])
                #except:
                #    continue
                #url = r.url
                url = str(url['expanded_url'])
                total_list.append(url)
                url_link = url_link + url+"\n"
                url_count+=1
                
            if url_count> 490:
                break
                
        url_link = "%d\n%s" %(url_count,url_link)
        jfile2.close()
        print("URL Count :",url_count)
        print("")
    except FileNotFoundError as e:
        print(e, " in extract tweets")
        
def google_safebrowsing():
    global google_status
    print("Checking url in Google Safe Browsing")
    try:
        data = url_link
        url= 'https://sb-ssl.google.com/safebrowsing/api/lookup?client=python&key=AIzaSyA1M7fY7G432oC9x2tdytCDWb86yAbrz0s&appver=0.2&pver=3.1'
        r= requests.post(url,data)
        print("URL Status Code: ",r.status_code)
        print("")
        
        if int(r.status_code)==200:
            google_status=True
            return
            
        wordcount = Counter(r.text.split())
        for item in wordcount.items():
            print("{}\t{}".format(*item))

    except Exception as e:
        print("Cannot proceed for URL checking because: ",e)
        print("")

def phishtank():
    global phishtank_status
    print("Checking url in Phishtank")
    print("")
    jsonfile = codecs.open("D:/phishtank.json")
    pyjson = json.load(jsonfile)
    for url_check in total_list:
        for doc in pyjson:
            if url_check in doc['url']:
                phishtank_status=True
                return
        jsonfile.close()

def urlblacklist():
    global urlblacklist_status
    print("Checking url in URLBlacklist")
    print("")
    list_dir = os.listdir("D:/urlblacklists")
    for url_check in total_list:
        for doc in list_dir:
            dir1 = "D:/urlblacklists/%s/urls" % doc
            try:
                file1 = codecs.open(dir1)
            except FileNotFoundError:
                continue
            
            for url in file1:
                if url_check in url:
                    urlblacklist_status=True
                    return
            
            file1.close()
            
        for doc in list_dir:
            dir2 = "D:/urlblacklists/%s/domains" % doc
            try:
                file2 = codecs.open(dir2)
            except FileNotFoundError:
                continue
            
            for domain in file2:
                if domain in url_check:
                    urlblacklist_status=True
                    return

            file2.close()
    
def dir_count():
    global counter_blacklist

    counter_blacklist = len(os.listdir("D:/Classify/Blacklist/"))

def decision(user):
    if (google_status is True) or (phishtank_status is True) or (urlblacklist_status is True):
        list_l = os.listdir(dir_id)
        dst_dir = "D:/Classify/Blacklist/%s" % user
        os.makedirs(dst_dir)
        for file in list_l:
            src_f = "%s/%s" %(dir_id,file)
            dst_f = "%s/%s" %(dst_dir,file)
            shutil.move(src_f, dst_f)
        os.rmdir(dir_id)
        return True

init_auto()
