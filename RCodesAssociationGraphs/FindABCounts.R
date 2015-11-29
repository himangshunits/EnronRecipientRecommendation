#must have usersFiltered present

abCounts = matrix(nrow = length(usersFiltered), ncol = 1)
rownames(abCounts) = c(usersFiltered)
colnames(abCounts) = c("count")
for(i in usersFiltered)
  abCounts[i, 1] = 0

countDown = length(usersFiltered) * length(usersFiltered)
for(i in usersFiltered){
  for(j in usersFiltered){
    print(paste(" count = ",countDown, "The i = ",i," and the j = ",j))
    countDown = countDown - 1
    if(!is.na(adjacency[i, j]))
      #print("HIT !!!")
      abCounts[i, 1] = abCounts[i, 1] + 1
  }
}    
#rm(i,j, abCounts)