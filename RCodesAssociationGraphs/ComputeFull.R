# This funtion takes paricular user s_k and goes through all the non zero 
# entries in it's row for the CG
# Which is nothing but the address book of that sender.
# it finds the recPrior and sender_likelihood for each of those recs, also generates the content liklihood and
# multiplies them, 
# and then gives us top k among them

ComputeAllComponent <- function(adjacency, sender, messageBody, recPrior, k, alpha, beta, gamma){
  resultSK <- matrix(nrow = 1, ncol = ncol(adjacency))
  colnames(resultSK) <- colnames(adjacency)
  rownames(resultSK) <- sender
  
  resultSK[1, ] <- 0
  
  maxABSize <- ncol(adjacency)
  
  # go through the users to which sender sent some messsage
  for (i in colnames(adjacency)){
    if(adjacency[sender, i] != 0){
      if(maxABSize <= 0)
        break
      # print(paste("Current Receiver in AB(of",sender,") = ",i))
      # Calculate the recipient prior
      recPriorRK <- as.numeric(recPrior[i, 1])
      # Calculate the sender likelihood, no regularization
      senderLikelihood <- as.numeric(adjacency[sender, i] / sum(adjacency[ , i]))
      # Calculate the Email Likelihood
      #emailLiklihood <- as.numeric(getContentLiklihood(i, sender, messageBody, alpha, beta, gamma))
      emailLiklihood <- 1
      allComponent = as.numeric(recPriorRK * senderLikelihood * emailLiklihood)
      resultSK[sender, i] <- allComponent
      maxABSize <- maxABSize - 1
    }
  }
  tempSK = sort(resultSK[sender,], decreasing = TRUE)
  return(tempSK[1:k])
  # we can convert the Named Data with like temp = as.matrix(tempSK[1])
  # rm(adj,recPriorRK,resultSK,temp,temp1,a,i,cgComponent,ncol,nrow,senderLikelihood,tempSK)
}