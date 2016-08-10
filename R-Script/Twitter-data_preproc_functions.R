
binary_features <-function(x){
  
  if(is.na(x)==TRUE | x=="False" | x=="None" | x ==""){
    return(0)
  }else{
    return(1)
  }
  
}

profile_age <- function(x){
  
  diff_date <- as.numeric(difftime(as.Date(Sys.time(),format="%a %b %d %T %z %Y"),as.Date(x,format="%a %b %d %T %z %Y")))
  return((diff_date/30)/12)
}

url_length_count_subdomain <- function(x){
  
  mean_per_obs_length <-c()
  mean_per_obs_count <-c()
  mean_per_obs_subdomain <-c()
  
  for(obs in 1:nrow(x)){
    
    length_out <- mean(nchar(x[obs,url_colnames][!is.na(x[obs,url_colnames])]))
    count_out <- length(x[obs,url_colnames][!is.na(x[obs,url_colnames])])
    
    
    #subdomain function start

    temp_split <- str_split( x[obs,url_colnames][!is.na(x[obs,url_colnames])],"/")
    temp_subd<- c()
    
    if(length(temp_split)==0){
      subdomain_out <- 0
    }else{
      
      for(i in range(1,length(temp_split))){
        temp_subd <- c(temp_subd,(length(str_split(temp_split[[i]][3],"[.]")[[1]])-2))
      }
      subdomain_out <- mean(temp_subd)
      
    }
    #subdomain function ends
    
    if(is.nan(length_out)==TRUE){
      length_out<-0
    }
    
    if(is.nan(count_out)==TRUE){
      count_out<-0
    }
    
    if(is.nan(subdomain_out)==TRUE){
      subdomain_out<-0
    }
    
    
    mean_per_obs_length <- c(mean_per_obs_length,length_out)
    mean_per_obs_count <- c(mean_per_obs_count,count_out)
    mean_per_obs_subdomain <- c(mean_per_obs_subdomain,subdomain_out)
    
    
  }

  return(c(mean(mean_per_obs_length),mean(mean_per_obs_count),mean(mean_per_obs_subdomain)))
}

avg_mention <- function(x){
  
  mention_per_obs<- c()
  
  for(obs in 1:nrow(x)){
    
    mention_per_obs <- c(mention_per_obs,length(x[obs,mention_colnames][!is.na(x[obs,mention_colnames])]))
    
  }
  
  return(mean(mention_per_obs))
}

sentiment_analysis <- function(x){
  
  text.corpus <- Corpus(VectorSource(c(x)))
  text.corpus <- score(text.corpus)
  
  #Polarity, subjectivity, pos_refs_per_ref, neg_refs_per_ref, senti_diffs_per_ref
  return(c(mean(meta(text.corpus)[[1]]),mean(meta(text.corpus)[[2]]),mean(meta(text.corpus)[[3]]),mean(meta(text.corpus)[[4]]),mean(meta(text.corpus)[[5]])))
  
  
}
