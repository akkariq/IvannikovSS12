library(janeaustenr)
library(parallel)
library(stringr)

extract_words <- function(book_name) {
  text <- subset(austen_books(), book == book_name)$text
  str_extract_all(text, boundary("word")) %>% unlist %>% tolower
}
janeausten_words <- function() {
  books <- austen_books()$book %>% unique %>% as.character
  words <- sapply(books, extract_words) %>% unlist
  words
}
max_frequency <- function(letter, words, min_length = 1) {
  w <- select_words(letter, words = words, min_length = min_length)
  frequency <- table(w) 
  frequency[which.max(frequency)]
}
select_words <- function(letter, words, min_length = 1) {
  min_length_words <- words[nchar(words) >= min_length]
  grep(paste0("^", letter), min_length_words, value = TRUE)
}


a <- janeausten_words()

letters <- letters

print(letters)

b <- sapply(letters, function(letter) max_frequency(letter,a,min_length = 5))

print(b)


print(barplot(b, las = 2))
