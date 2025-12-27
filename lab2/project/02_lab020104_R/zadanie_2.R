#df <- as.data.frame(list(V1 = c(-9.7, -10, -10.5, -7.8, -8.9), 
#V2 = c(NA, -10.2, -10.1, -9.3, -12.2), V3 = c(NA, NA, -9.3, -10.9, -9.8)))

df <- as.data.frame(list(V1 = c(NA, -0.5, -0.7, -8), 
V2 = c(-0.3, NA, -2, -1.2),
V3 = c(1, 2, 3, NA)))
get_negative_values <- function(df) {
    res_listik = list()
    for (i in 1:ncol(df)) {
        
        listik <- list()
        for (j in 1:nrow(df)) {
            if (!is.na(df[j,i]) && df[j,i] < 0) {
                
                listik <- c(listik, df[j,i])

            }
        }
        
        res_listik[[colnames(df)[i]]] <- unlist(listik)
        
        #print(colnames(df)[i])
        #print(unlist(listik))
        #cat("\n")  # пустая строка для разделения
        

    }
    
    a <- sapply(res_listik, length)
    #print(a)


    if (all(a == a[1])) {
        masiv4ik <- cbind(res_listik$V1, res_listik$V2)
        colnames(masiv4ik) <- names(res_listik)
        return(masiv4ik)
    }
    else {
        return(res_listik)
    }
    
}

print(get_negative_values(df))