# It will check if any element in topK Named number matches
# any element in matrix actualRecipients

HasHit <- function(topK, actualRecipients){
  result <- FALSE
  topKX = rownames(as.matrix(topK))
  for(i in topKX){
    for(j in actualRecipients[, 1]){
      if(i == j)
        result <- TRUE
    }
  }
  return(result)
}


# Find the Precision@K
PrecAtK <- function(k, actual, predicted){
  count <- 0
  for(i in 1:k){
    if(predicted[i] %in% actual){
      count <- count + 1
    }
  }
  return(as.numeric(count/k))
}

# Find R-Precision
RPrec <- function(actual, predicted){
  count <- 0
  k <- length(actual)
  for(i in 1:min(k,length(predicted))){
    if(predicted[i] %in% actual){
      count <- count + 1
    }
  }
  return(as.numeric(count/k))
}