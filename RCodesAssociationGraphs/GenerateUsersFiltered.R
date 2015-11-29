#load the driver and the databaase
library("DBI", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")

drv = dbDriver("MySQL")
con = dbConnect(drv, user="root", dbname="enron_merged", password="test@123")

senderCount = dbGetQuery(con,"select sender,count(*) from messages group by sender order by count(*) desc;")
recCount = dbGetQuery(con,"select rvalue,count(*) from communications group by rvalue order by count(*) desc;")

tempRec = subset(recCount, recCount[,2] > 100)
tempSend = subset(senderCount, senderCount[,2] > 100)
temp2 = c(tempSend[,1],tempRec[,1])

usersFiltered = unique(temp2)
rm(tempRec,tempSend,temp2,recCount,senderCount)
temp = paste(usersFiltered,collapse = '","')
write.table(temp, "UserListData.txt", sep="\t")
rm(temp)