# This funtion takes paricular user s_k and goes through all the non zero 
# entries in it's row for the CG
# Which is nothing but the address book of that sender.
# it finds the recPrior and sender_likelihood for each of those recs, multiplies them, 
# and then gives us top k among them

ComputeCGComponent <- function(adjacency, sender, recPrior, k){
  resultSK <- matrix(nrow = 1, ncol = ncol(adjacency))
  colnames(resultSK) <- colnames(adjacency)
  rownames(resultSK) <- sender
  # go through the users to which sender sent some messsage
  for (i in colnames(adjacency)){
    if(adjacency[sender, i] != 0){
      # Calculate the recipient prior
      recPriorRK <- as.numeric(recPrior[i, 1])
      # Calculate the sender likelihood, no regularization
      senderLikelihood <- as.numeric(adjacency[sender, i] / sum(adjacency[ , i]))
      cgComponent = as.numeric(recPriorRK * senderLikelihood)
      resultSK[sender, i] <- cgComponent
    }
    else{
      resultSK[sender, i] <- 0
    }
  }
  tempSK = sort(resultSK[sender,], decreasing = TRUE)
  return(tempSK[1:k])
  # we can convert the Named Data with like temp = as.matrix(tempSK[1])
  # rm(adj,recPriorRK,resultSK,temp,temp1,a,i,cgComponent,ncol,nrow,senderLikelihood,tempSK)
} 
