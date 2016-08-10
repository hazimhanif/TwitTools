library(ggplot2)
library(stringr)
library(tm.plugin.sentiment)

#Read CSV  files
#bot <- read.csv("D:/dataset_bot_100.csv",stringsAsFactors = FALSE)
#cyborg <- read.csv("D:/dataset_cyborg_100.csv",stringsAsFactors = FALSE)
#human <- read.csv("D:/dataset_human_100.csv",stringsAsFactors = FALSE)

source("C:/Users/Hazim/OneDrive/Documents/R files/Twitter Data/Twitter-data pre proc_functions.R")

#zz <-data.frame()
#zz2<-data.frame()
c<-0

url_colnames<- names(bot)[!is.na(sapply(names(bot), function(x) str_match(x,"tweet_entities_urls_[\\d+]_expanded_url|tweet_entities_media_[\\d+]_expanded_url")))]
mention_colnames <- names(bot)[!is.na(sapply(names(bot), function(x) str_match(x,"tweet_entities_user_mentions_[\\d+]_id_str")))]

for(id in unique(bot$user_id)){
  
  tweet_text <- bot[bot$user_id==id,"tweet_text"]
  url_based <- url_length_count_subdomain(bot[bot$user_id==id,])
  sentiment <- sentiment_analysis(tweet_text)

  
  cat("\n\n User_id:",unique(bot[bot$user_id==id,"user_id"]))
  cat("\n User_screen_name_len:",nchar(unique(bot[bot$user_id==id,"user_screen_name"])))
  cat("\n User_location:",binary_features(unique(bot[bot$user_id==id,"user_location"])))
  cat("\n User_description:",binary_features(unique(bot[bot$user_id==id,"user_description"])))
  cat("\n User_followers_count:",unique(bot[bot$user_id==id,"user_followers_count"]))
  cat("\n User_friends_count:",unique(bot[bot$user_id==id,"user_friends_count"]))
  cat("\n User_listed_count:",unique(bot[bot$user_id==id,"user_listed_count"]))
  cat("\n User_favourites_count:",unique(bot[bot$user_id==id,"user_favourites_count"]))
  cat("\n User_profile_age:",profile_age(unique(bot[bot$user_id==id,"user_created_at"])))
  cat("\n Followers_following_ratio:",unique(bot[bot$user_id==id,"user_followers_count"])/unique(bot[bot$user_id==id,"user_friends_count"]))
  cat("\n Account_reputation:",unique(bot[bot$user_id==id,"user_followers_count"])/(unique(bot[bot$user_id==id,"user_followers_count"])+unique(bot[bot$user_id==id,"user_friends_count"])))
  cat("\n Account_verified:",binary_features(unique(bot[bot$user_id==id,"user_verified"])))
  cat("\n Default_profile_image:",binary_features(unique(bot[bot$user_id==id,"user_default_profile_image"])))
  cat("\n Statuses_count:",unique(bot[bot$user_id==id,"user_statuses_count"]))
  cat("\n Avg char length:",mean(nchar(tweet_text)))
  cat("\n Avg hashtag:",mean(str_count(tweet_text, '#')))
  cat("\n Avg atsign:",mean(str_count(tweet_text, '@')))
  cat("\n Avg dots:",mean(str_count(tweet_text, '[.]')))
  cat("\n Avg post hashtag first:",hashtag_first<-mean(str_count(substring(tweet_text,1,1),'#')))
  cat("\n Avg post hashtag last:", hashtag_last<-mean(str_count(substring(sapply(str_split(tweet_text," "),function(x) tail(x,n=1)),1,1),'#')))
  cat("\n Avg post hashtag aggregate:",hashtag_first + hashtag_last)
  cat("\n Avg post atsign first:",atsign_first<-mean(str_count(substring(tweet_text,1,1),'@')))
  cat("\n Avg post atsign last:", atsign_last<-mean(str_count(substring(sapply(str_split(tweet_text," "),function(x) tail(x,n=1)),1,1),'@')))
  cat("\n Avg post atsign aggregate:",atsign_first + atsign_last)
  cat("\n Avg post http first:",http_first<-mean(str_count(substring(tweet_text,1,5),'http')))
  cat("\n Avg post http last:", http_last<-mean(str_count(substring(sapply(str_split(tweet_text," "),function(x) tail(x,n=1)),1,5),'http')))
  cat("\n Avg post http aggregate:",http_first + http_last)
  cat("\n Avg url length:", url_based[1])
  cat("\n Avg url count:", url_based[2])
  cat("\n Avg url subdomain count:", url_based[3])
  cat("\n Account popularity(RT/T):", mean(bot[bot$user_id==id,"tweet_retweet_count"])/length(bot[bot$user_id==id]))
  cat("\n Avg mentions per user:", avg_mention(bot[bot$user_id==id,]))
  cat("\n Avg sentiment polarity:", sentiment[1])
  cat("\n Avg sentiment subjectivity:", sentiment[2])
  cat("\n Avg sentiment pos_refs_per_ref:", sentiment[3])
  cat("\n Avg sentiment neg_refs_per_ref:", sentiment[4])
  cat("\n Avg sentiment senti_diffs_per_ref:", sentiment[5])
  
  
  
  c<- c+1
  
  if(c==4){
    break
  }
}


