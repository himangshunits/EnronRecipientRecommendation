# This script calculates the matrices needed for the email likelihood prediction
# P(w|R,S)
# select sender,rvalue,term,count(*) from communications_term_train where rtype='TO' group by sender,rvalue,term;

# for P(w|R) 
# select rvalue,term,count(*) from communications_term_train where rtype='TO' group by rvalue,term;

# for P(w)
# select term,count(*) from document_term group by term order by count(*) desc;


#load the driver and the databaase
library("DBI", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")

drv <- dbDriver("MySQL")
con <- dbConnect(drv, user="root", dbname="enron_document_term", password="test@123")
print("Fetching Receiver Word counts !")
recWordCount <- dbGetQuery(con,"select rvalue,term,count(*) from communications_term_train where rtype='TO' group by rvalue,term;")
print("Fetching Sender Receiver Word counts !")
recSendWordCount <- dbGetQuery(con,"select sender,rvalue,term,count(*) from communications_term_train where rtype='TO' group by sender,rvalue,term;")
print("Fetching Word counts !")
wordCount <- dbGetQuery(con,"select term,count(*) from document_term group by term order by count(*) desc;")

# make the matrices.
### Word prior

wordPrior <- matrix(nrow = nrow(wordCount), ncol = 1)
colnames(wordPrior) <- c("count")
rownames(wordPrior) <- c(wordCount[, 1])

wordPrior[, 1] <- wordCount[, 2]

totalWords <- sum(wordPrior[, 1])
# Now normalize
for(k in rownames(wordPrior)){
  wordPrior[k, 1] = as.numeric(wordPrior[k, 1] / totalWords)
}

rm(totalWords, k)

## Recipent Word Likelihood

adjacencyRecWord = matrix(nrow = length(usersFiltered), ncol = length(top500terms))
colnames(adjacencyRecWord)=c(top500terms)
rownames(adjacencyRecWord)=c(usersFiltered)

adjacencyRecWord[,] <- 0

for(i in 1:nrow(recWordCount)){	
  print(paste("Current processing =",nrow(recWordCount) - i));
  if(!is.na(match(recWordCount[i,1],usersFiltered)) && !is.na(match(recWordCount[i,2], top500terms))){
    adjacencyRecWord[recWordCount[i,1], recWordCount[i,2]] <- recWordCount[i,3];
  }
}

rm(i)

#cleanedAdjRecWord <- RemoveNAAdjRecWord(adjacencyRecWord, usersFiltered, top500terms)

# Sender Recipient Word Likelihood

# Sequence is sender-rvalue-term

adjacencySendRecWord = array(dim = c(length(usersSuperFiltered), length(usersFiltered), length(top500terms)))

dimnames(adjacencySendRecWord)[[1]] <- c(usersSuperFiltered)
dimnames(adjacencySendRecWord)[[2]] <- c(usersFiltered)
dimnames(adjacencySendRecWord)[[3]] <- c(top500terms)

adjacencySendRecWord[,,] <- 0

for(i in 1:nrow(recSendWordCount)){	
  print(paste("Current processing =",nrow(recSendWordCount) - i));
  if(!is.na(match(recSendWordCount[i,1],usersSuperFiltered)) && !is.na(match(recSendWordCount[i,2],usersFiltered)) && !is.na(match(recSendWordCount[i,3], top500terms))){
    adjacencySendRecWord[recSendWordCount[i,1], recSendWordCount[i,2], recSendWordCount[i,3]] <- recSendWordCount[i,4];
  }
}

rm(i)



# Clean the matrices
