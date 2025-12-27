# Подключение пакета, определение количества ядер
library(parallel)

# Создание кластера





mean_of_rnorm <- function(n) {
  random_numbers <- rnorm(n)
  mean(random_numbers)
}

ncores <- detectCores(logical = FALSE)
n <- ncores:1
cl <- makeCluster(ncores)

clusterExport(cl, "mean_of_rnorm")

clusterEvalQ(cl, {
  paste("Узел", Sys.getpid(), "готов")
})

result <- vector("list", 50)

for (iter in seq_len(50)){
  result[[iter]] <- mean_of_rnorm(10000)
  print(result[[iter]])
}


result2 <- parLapply(cl, 1:50, function(x) mean_of_rnorm(10000))
print(result2)


stopCluster(cl)

