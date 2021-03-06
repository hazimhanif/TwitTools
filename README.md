# TwitTools
TwitTools contains 6 tools: 
* TwitCrawl
* TwitClean
* TwitClassify
* TwitXtract
* BlacklistChecker
* R-Script

## TwitCrawl
A python Twitter crawler. The crawler uses Twitter API to query the data from twitter. Tweepy is used as the python Twitter API wrapper in the script.

##### How it works:
1. The script will be given a 'seed' account from the user. The seed account will act as starting point for the crawl.
2. The method of crawling is based on the Depth-First Search mechanism and techniques.
3. The script will go down the depth by taking the followers list of the seed (depth 0).
4. The seed's follower will be at Depth 1.
5. Next, the script will get the list of followers from the user in Depth 1 and perform crawling for Depth 2.
6. It goes on.
7. The crawler stops at Depth 3.

##### Prerequisites:
* Twitter API Key (Create an app key in http://dev.twitter.com)
* Tweepy package (https://github.com/tweepy/tweepy)
* Python 3.*
* Self confidence :)

##### How to use:
* Change the API key and the directory to your own respective and desired directory.
* Execute the python script.

## TwitClean
A python script that performs cleaning of the data. The data cleaning process is used as a preparation before it is being classify by TwitClassify.

##### How it works:
1. Execute the script.
3. The script will iterate every depth and check all the user data.
2. It move the user which does not have enough data:
** user_data.dump
** tweets.dump
** followers.txt
** friends.txt
3. The user is the moved to a "Drop" folder where all the "broken"/"contaminated" data were stored.

## TwitClassify
A python script that is used to classify the data collected using TwitCrawl and cleaned using TwitClean. The classification is based on the user accounts and it needs to be manually classify. The script is used for ground truth creation to manully classify a Twitter user whether he/she is a human, robot or cyborg.

##### How it works:
1. The script will fetch the first user based the depth. Depth 0 is the initial depth or the seed depth.
2. User will be asked whether the user wants to fetch the user info or not.
3. If yes, the user's basic selected info will be previewed and also the top 100 tweets are shown.
4. The user is then asked whether they want the script to open the account's twitter page or not.
5. Classification is done manually in this case since it is a ground truth creation script.
6. The process will go on with the next user.

##### How to *classify* ?
Source : Chu, Z., et al. Detecting automation of twitter accounts: Are you a human, bot, or cyborg? IEEE Transactions on Dependable and Secure Computing, 2012. 9, 811-824 DOI: 10.1109/TDSC.2012.75.
(http://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6280553)

###### Aspects to monitored:
* Visit homepage
* Check tweets
* URLs
* Tweeting device
* User profile
* No of followers
* No of friends


###### How to detect Humans:
* Turing tester communicates with an unknown subject for 5 minutes.
* The tweet content is expressed in relatively
* Human like intelligence presence in tweet

###### How to detect bots:
* The lack of intelligent or original content.
* Excessive automation of tweeting, like automatic updates of blog entries or RSS feeds.
* The abundant presence of spam or malicious URLs (i.e., phishing or malware) in tweets or the user profile.
* Repeatedly posting duplicate tweets
* Posting links with unrelated tweets.
* Aggressive following behavior

###### How to detect Cyborg:
* Evidence of both human and bot participation.
* May contain very different types of tweets(Human like intelligence + RSS Feeds/Auto Update)

## TwitXtract

###### How it works?:
1. The script will convert the raw json twitter dumps into a csv file
2. The csv file will have more than 1000+ columns due to all the sub-json structure were parsed effectively
3. Number of user and number of tweets per user is configurable.
4. It is a time consuming process.

## BlacklistChecker

###### How it works?:
1. The script will check the URL in every twitter account.
2. The URL checked is up to 490 URLs.
3. Each URL is cross checked with 3 differnt spam/malware/phishing checking tools:
* Google Safe Browsing Api
* Phishtank
* URLBlacklist
4. If any of the user's URL is detected as malicious, the user will be move into the blacklist category.

## R-Script

###### How it works?:
-Pre processing of the RAW csv created by TwitXtract.
