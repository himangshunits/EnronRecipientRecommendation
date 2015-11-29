#load the driver and the databaase
library("DBI", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")

drv = dbDriver("MySQL")
con = dbConnect(drv, user="root", dbname="enron_merged", password="test@123")
#dbListTables(con)
dates = dbGetQuery(con,"select message_id,date from messages order by date")
count = 0
i = 1
while (i <= nrow(dates)){
  print(paste("Inside Training", count))
  query = paste(sep="","UPDATE messages SET split='TRAINING' WHERE message_id=", "'",dates[i,'message_id'],"'")
  dbSendQuery(con,query)
  i = i + 2
  count = count + 1
}

j = 2
while (j <= nrow(dates)){
  print(paste("Inside Testing", count))
  query = paste(sep="","UPDATE messages SET split='TESTING' WHERE message_id=", "'",dates[j,'message_id'],"'")
  dbSendQuery(con,query)
  j = j + 2
  count = count + 1
}

#housekeeping
dbDisconnect(con)
dbUnloadDriver(drv)