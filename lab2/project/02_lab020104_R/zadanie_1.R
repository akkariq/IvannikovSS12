my_vector <- c(21, 18, 21, 19, 25, 20, 17, 17, 18, 22, 17, 18, 18, 19, 19, 27, 21, 20,
24, 17, 15, 24, 24, 29, 19, 14, 21, 17, 19, 18, 18, 20, 21, 21, 19, 17, 21, 13, 17, 13,
23, 15, 23, 24, 16, 17, 25, 24, 22)

sred <- mean(my_vector)
a <- sd(my_vector)

my_vector2 <- c()

for (i in my_vector) {
    if (abs(sred - i) < a) {
        my_vector2 <- c(my_vector2, i)
    }
}


print(my_vector2)