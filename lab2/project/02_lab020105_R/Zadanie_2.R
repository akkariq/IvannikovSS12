library(datasets)
library(purrr)

a <- list(1:10)
b <- 1:10
c <- c("a","b","v")
d <- -5:5
map(a,sum)

map_if(b, function(x) x %% 2 != 0, print)
print(" ")
map_at(c, c(1,3), print)
print(" ")

res <- map_lgl(d, function(x) (x > 0))
print(res)

print(" ")

res_chr <- map_chr(b, as.character)
print(res_chr)

print(" ")

res_int <- map_int(res_chr, as.integer)
print(res_int)

print(" ")

map_dbl(b, function(x) x / 3)

print(" ")

df_list <- list(
  data.frame(x = 1:2, y = c("a", "b")),
  data.frame(x = 3:4, y = c("c", "d")),
  data.frame(x = 5:6, y = c("e", "f"))
)

result <- map_dfr(df_list, identity, .id = "source")
result2 <- map_dfr(df_list, identity)
print(result)
print(result2)

df_list2 <- list(
  data.frame(a = 1:3, b = 4:6),
  data.frame(c = 7:9, d = 10:12),
  data.frame(e = 13:15, f = 16:18),
  data.frame(g = 19:21, h = 22:24)
)

result3 <- map_dfc(df_list2, identity)
print(result3)

walk(b,print)
walk(b,function(x) print(x * 10))
#print(cars)
#map(cars[["speed"]])
#print(cars[["speed"]])

