# code to generate recipient prior from the adjacency matrix for evry receiver.
# it consideers only those senders which is in the UsersSuperFiltered List

recPrior <- matrix(nrow = length(usersFiltered), ncol = 1)
rownames(recPrior) <- c(usersFiltered)
colnames(recPrior) <- c("prior")
recPrior[,1] <- 0
count <- length(usersFiltered) ** 2

for(j in usersFiltered){
  #sprintf("The current Recipient = %s and Countdown = %d", j, count)
  print(paste("Count = ",count))
  for(i in usersFiltered){
    if(!is.na(match(i, usersSuperFiltered)))
      recPrior[j, 1] <- recPrior[j, 1] + adjacencyClean[i, j]
    count <- count - 1
  }
}
totalEmails <- sum(recPrior[, 1])
# Now normalize
for(k in rownames(recPrior)){
  recPrior[k, 1] = as.numeric(recPrior[k, 1] / totalEmails)
}

rm(i,j,k, count,totalEmails)