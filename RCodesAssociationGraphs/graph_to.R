#load the driver and the databaase
library("DBI", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")

drv = dbDriver("MySQL")
con = dbConnect(drv, user="root", dbname="enron_merged", password="test@123")
#dbListTables(con)
#countTable = dbGetQuery(con,"select sender,rvalue,count(*) from communications_train where rtype='TO' 
#group by sender,rvalue order by count(*) desc;")

#do below for drawing on the whole set
countTable = dbGetQuery(con,"select sender,rvalue,count(*) from communications where rtype='TO' 
                        group by sender,rvalue order by count(*) desc;")

#setwd("/Users/Himangshu/Desktop/EnronDataset/R_Data/")


#countTable = dbGetQuery(con, "select c.sender,c.rvalue,count(*) from communications c,messages m where c.mid=m.mid AND m.split='TRAINING' AND c.rtype='TO' group by c.sender,c.rvalue")


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