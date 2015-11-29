#load the driver and the databaase
library("DBI", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")

drv = dbDriver("MySQL")
con = dbConnect(drv, user="root", dbname="enron_merged", password="test@123")

countTable = dbGetQuery(con,"select sender,rvalue,count(*) from communications_train where rtype='TO' 
                            group by sender,rvalue order by count(*) desc;")


adjacency = matrix(nrow = length(usersFiltered), ncol = length(usersFiltered))
colnames(adjacency)=c(usersFiltered)
rownames(adjacency)=c(usersFiltered)


for(i in 1:nrow(countTable)){	
  print(paste("Current processing =",nrow(countTable) - i));
  if(!is.na(match(countTable[i,1],usersFiltered)) && !is.na(match(countTable[i,2], usersFiltered))){
    adjacency[countTable[i,1], countTable[i,2]] = countTable[i,3];
  }
}


rm(i)