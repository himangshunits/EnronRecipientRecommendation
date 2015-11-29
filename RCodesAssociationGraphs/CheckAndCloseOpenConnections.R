# Checks and closes all the open connections

CloseConnect <- function(){
  all_cons <- dbListConnections(MySQL())
  for(con in all_cons){
    dbDisconnect(con)
  }
}