#load the driver and the databaase
library("DBI", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")
library("RMySQL", lib.loc="/Library/Frameworks/R.framework/Versions/3.2/Resources/library")

drv = dbDriver("MySQL")
con = dbConnect(drv, user="root", dbname="enron_merged", password="test@123")


recCount = dbGetQuery(con,"select rvalue,count(*) from communications_train where rtype = 'TO' group by rvalue order by count(*) desc;")

totalEmails = dbGetQuery(con,"select count(distinct mid) from communications_train;")