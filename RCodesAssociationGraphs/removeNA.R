#this fucntion removes all the NA from a matrix adjacency whose row and colum index names are in usersFiltered

RemoveNAAdjacency <- function(adjacency, usersFiltered){
  countDown = length(usersFiltered) * length(usersFiltered)
  for(i in usersFiltered){
    for(j in usersFiltered){
      print(paste(" count = ",countDown, "The i = ",i," and the j = ",j))
      countDown <- countDown - 1
      if(is.na(adjacency[i, j]))
        adjacency[i, j] <- 0
    }
  }
  return(adjacency)
}