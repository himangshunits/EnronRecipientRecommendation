#load the driver and the databaase
library("DBI", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")

drv = dbDriver("MySQL")
con = dbConnect(drv, user="root", dbname="enron_merged", password="test@123")

countTableCC = dbGetQuery(con,"select sender,rvalue,count(*) from communications_train where rtype='CC' 
                        group by sender,rvalue order by count(*) desc;")


adjacencyCC = matrix(nrow = length(usersFiltered), ncol = length(usersFiltered))
colnames(adjacencyCC)=c(usersFiltered)
rownames(adjacencyCC)=c(usersFiltered)

adjacencyCC[ , ] <- 0

for(i in 1:nrow(countTableCC)){	
  print(paste("Current processing =",nrow(countTableCC) - i));
  if(!is.na(match(countTableCC[i,1],usersFiltered)) && !is.na(match(countTableCC[i,2], usersFiltered))){
    adjacencyCC[countTableCC[i,1], countTableCC[i,2]] <- countTableCC[i,3];
  }
}


rm(i)