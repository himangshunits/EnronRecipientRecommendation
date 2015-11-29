tempAbSuperFiltered = subset(abCounts, abCounts[,1] > 250)
usersSuperFiltered = rownames(tempAbSuperFiltered)
write.table(usersSuperFiltered, "UserListDataSuperFiltered.txt", sep="\t")
rm(tempAbSuperFiltered)