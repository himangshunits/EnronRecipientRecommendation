# This script will fetch each and evry user's mails and test them with the
# ComputeAllComponent function
# go thorugh all the senders
TestAllComponent <- function(k, sampleSize, doSampling){
  library("DBI", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
  library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
  python.load("getVocab.py", get.exception = TRUE)
  drv <- dbDriver("MySQL")
  con <- dbConnect(drv, user="root", dbname="enron_document_term", password="test@123")
  
  #define a matrix to find hits per user, i.e. no of emails in which it has a hit
  resultSetSK <- matrix(ncol = 1, nrow = length(usersSuperFiltered))
  rownames(resultSetSK) <- c(usersSuperFiltered)
  colnames(resultSetSK) <- c("hits")
  # set all rows to zero
  resultSetSK[, 1] <- 0
  totalMessagesProcessed <- 0
  
  for(userSK in usersSuperFiltered[1:41]){
    print(paste("Current Sender = ",userSK))
    # get the message ids for the sender userSK
    # select distinct(mid) from communications_test where 
    # sender ='jeff.dasovich@enron.com' AND rtype='TO'
    query <- paste("select distinct(mid) from communications_test where sender ='",userSK,"' AND rtype='TO';",sep = "")
    messagesSK <- dbGetQuery(con,query)
    
    #sample out a subset from messages
    print(nrow(messagesSK))
    print(sampleSize)
    # if doSampling is false, then pick the top "sample Size messages and do it"
    if(!doSampling)
      sampledMessages <- messagesSK[1:min(sampleSize, nrow(messagesSK)), 1]
    else
      sampledMessages <- sample(messagesSK[, 1], min(sampleSize, nrow(messagesSK)), replace = FALSE)
    
    # get the top 10 prediction of this sender
    count <- length(sampledMessages)
    
    # iterate through all the messages
    for(message in sampledMessages){
      print(paste("Mesages Left = ",count))
      count <- count - 1
      # get the message
      query <- paste("select body from messages where mid = ",message,";",sep = "")
      messageRetrieved <- dbGetQuery(con,query)
      messageBody <- as.character(messageRetrieved)
      
      # adjacency, sender, messageBody, recPrior, k, alpha, beta, gamma
      topK <- ComputeAllComponent(adjacencyClean, userSK, messageBody, recPrior, k, 0.60, 0.20, 0.20)
      
      # get the slice
      #select rvalue from communications_test where mid = 296785 AND sender ='jeff.dasovich@enron.com' AND rtype='TO';
      query <- paste("select rvalue from communications_test where mid = ",message, " AND sender ='", userSK, "' AND rtype='TO';",sep = "")
      actualRecipients <- dbGetQuery(con,query)
      totalMessagesProcessed <- totalMessagesProcessed + 1
      # find if this message has a hit
      #if(HasHit(topK, actualRecipients)){
      #  resultSetSK[userSK, 1] <- resultSetSK[userSK, 1] + 1
      #}
      # Find MAP
      topKX = rownames(as.matrix(topK))
      ap_message = apk(k, actualRecipients[, 1], topKX)
      #ap_message = PrecAtK(k, actualRecipients[, 1], topKX)
      #ap_message = RPrec(actualRecipients[, 1], topKX)
      print(paste("The AP is = ",ap_message))
      resultSetSK[userSK, 1] <- resultSetSK[userSK, 1] + ap_message
    }
  }
  
  print(paste("Total =" , totalMessagesProcessed))
  print(paste("Sum of Hits =" , sum(resultSetSK[,1])))
  
  #rm(actualRecipients, messagesSK, resultSetSK,resultSK,all_cons,con, drv, count, message, query,temp, topK, topKX, totalEmails, userSK)
  return(resultSetSK)
}