# code to remove NA from AdjacencyRecWord

RemoveNAAdjRecWord <- function(adjacency, usersFiltered, top500terms){
  countDown <- length(usersFiltered)
  for(i in usersFiltered){
    print(paste(" count = ",countDown, "The User = ",i))
    countDown <- countDown - 1
    for(j in top500terms){
      if(is.na(adjacency[i, j]))
        adjacency[i, j] <- 0
    }
  }
  return(adjacency)
}
