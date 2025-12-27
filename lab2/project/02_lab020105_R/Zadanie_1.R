library(purrr)
library(repurrrsive)

title <- map_chr(sw_films, "title")
named_films <- set_names(sw_films, title)

named_films[["A New Hope"]]$release_date
  
named_films2 <- sw_films %>% 
  set_names(map_chr(., "title"))

named_films2[["A New Hope"]]$title
