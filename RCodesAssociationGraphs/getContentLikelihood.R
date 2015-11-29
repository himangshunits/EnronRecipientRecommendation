# This fucntion computes the word vectors using python script and then indexes the probs

getContentLiklihood <- function(rvalue, sender, messageBody, alpha, beta, gamma){
  vocab <- python.call("getAccurateVocab", messageBody, top500terms)
  product <- 1
  for(term in vocab){
    # TODO : Get the accurate vocab so that the following linear check can be removed
    #if(!(term %in% top500terms))
      #next
    # handle cases when the sender receiver or word is not in the list
    # calculate P(w|X,S)(refer to report)
    # print(paste("Current Term = ",term))
    pwxs <- as.numeric(adjacencySendRecWord[sender, rvalue, term] / sum(adjacencySendRecWord[sender, rvalue, ]))
    # calculate P(w|X)
    wx <- as.numeric(adjacencyRecWord[rvalue, term] / sum(adjacencyRecWord[rvalue, ]))
    # P(w)
    w <- as.numeric(wordPrior[term, 1])
    prob <- alpha*pwxs + beta*wx + gamma*w
    product <- product * prob
  }
  return(product)
}