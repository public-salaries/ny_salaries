# Merge by year

ny_2008 <- list.files("2008", full.names = T)
ny2008  <- do.call(rbind, lapply(ny_2008, read.csv))
write.csv(ny2008, file = "ny_2008.csv" , row.names = F)

ny_2009 <- list.files("2009", full.names = T)
ny2009  <- do.call(rbind, lapply(ny_2009, read.csv))
write.csv(ny2009, file = "ny_2009.csv" , row.names = F)

ny_2010 <- list.files("2010", full.names = T)
ny2010  <- do.call(rbind, lapply(ny_2010, read.csv))
write.csv(ny2010, file = "ny_2010.csv" , row.names = F)

ny_2011 <- list.files("2011", full.names = T)
ny2011  <- do.call(rbind, lapply(ny_2011, read.csv))
write.csv(ny2011, file = "ny_2011.csv" , row.names = F)

ny_2012 <- list.files("2012", full.names = T)
ny2012  <- do.call(rbind, lapply(ny_2012, read.csv))
write.csv(ny2012, file = "ny_2012.csv" , row.names = F)

ny_2013 <- list.files("2013", full.names = T)
ny2013  <- do.call(rbind, lapply(ny_2013, read.csv))
write.csv(ny2013, file = "ny_2013.csv" , row.names = F)

ny_2014 <- list.files("2014", full.names = T)
ny2014  <- do.call(rbind, lapply(ny_2014, read.csv))
write.csv(ny2014, file = "ny_2014.csv" , row.names = F)

ny_2015 <- list.files("2015", full.names = T)
ny2015  <- do.call(rbind, lapply(ny_2015, read.csv))
write.csv(ny2015, file = "ny_2015.csv" , row.names = F)

ny_2016 <- list.files("2016", full.names = T)
ny2016  <- do.call(rbind, lapply(ny_2016, read.csv))
write.csv(ny2016, file = "ny_2016.csv" , row.names = F)

ny_2017 <- list.files("2017", full.names = T)
ny2017  <- do.call(rbind, lapply(ny_2017, read.csv))
write.csv(ny2017, file = "ny_2017.csv" , row.names = F)
