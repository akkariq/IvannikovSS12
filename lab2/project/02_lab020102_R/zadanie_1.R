user_input <- readline()
user_input <- "Эллипс"
spis <- c("Круг","Квадрат","Прямоугольник","Треугольник","Параллелограмм","Ромб","Трапеция","Эллипс")




Kryg <- function(r){
    number <- as.integer(a)
    pi <- 3.14
    return(number * r^2)
}


for (i in spis){
    if (user_input == i){
        if (i == "Квадрат"){
            k <- 0
            while(TRUE){
                if (k == 3){
                    print("1234")
                    break
                }
                a <- readline()
                a <- "5"
                if (grepl("^\\d+$", a)){
                    number <- as.integer(a)
                    print("S Квадрат")
                    print(number^2)
                    break
                }
                else{
                    k <- k + 1
                }
            }
            
        }
        if (i == "Круг"){
            k <- 0
            while(TRUE){
                if (k == 3){
                    print("1234")
                    break
                }
                r <- readline()
                r <- "5"
                if (grepl("^\\d+$", r)){
                    pi <- 3.14
                    number <- as.integer(r)
                    print("S Круг")
                    print(pi * number^2)
                    break
                }
                else{
                    k <- k + 1
                }
            }
            
        }
        if (i == "Прямоугольник"){
            k <- 0
            while(TRUE){
                if (k == 3){
                    print("1234")
                    break
                }
                a <- readline()
                a <- "5"
                b <- readline()
                b <- "10"
                if (grepl("^\\d+$", a) & grepl("^\\d+$", b)){
                    
                    a_int <- as.integer(a)
                    b_int <- as.integer(b)
                    print("S Прямоугольник")
                    print(a_int * b_int)
                    break
                }
                else{
                    k <- k + 1
                }
            }
            
        }
        if (i == "Треугольник"){
            k <- 0
            while(TRUE){
                if (k == 3){
                    print("1234")
                    break
                }
                a <- readline()
                a <- "5"
                h <- readline()
                h <- "10"
                if (grepl("^\\d+$", a) & grepl("^\\d+$", h)){
                    
                    a_int <- as.integer(a)
                    h_int <- as.integer(h)
                    print("S Треугольник")
                    print(0.5 * a_int * h_int)
                    break
                }
                else{
                    k <- k + 1
                }
            }
            
        }
        if (i == "Параллелограмм"){
            k <- 0
            while(TRUE){
                if (k == 3){
                    print("1234")
                    break
                }
                a <- readline()
                a <- "5"
                h <- readline()
                h <- "10"
                if (grepl("^\\d+$", a) & grepl("^\\d+$", h)){
                    
                    a_int <- as.integer(a)
                    h_int <- as.integer(h)
                    print("S Параллелограмм")
                    print(a_int * h_int)
                    break
                }
                else{
                    k <- k + 1
                }
            }
            
        }
        if (i == "Ромб"){
            k <- 0
            while(TRUE){
                if (k == 3){
                    print("1234")
                    break
                }
                a <- readline()
                a <- "5"
                h <- readline()
                h <- "10"
                if (grepl("^\\d+$", a) & grepl("^\\d+$", h)){
                    
                    a_int <- as.integer(a)
                    h_int <- as.integer(h)
                    print("S Ромб")
                    print(a_int * h_int)
                    break
                }
                else{
                    k <- k + 1
                }
            }
            
        }
        if (i == "Трапеция"){
            k <- 0
            while(TRUE){
                if (k == 3){
                    print("1234")
                    break
                }
                a <- readline()
                a <- "5"
                b <- readline()
                b <- "10"
                h <- readline()
                h <- "10"
                if (grepl("^\\d+$", a) & grepl("^\\d+$", h) & grepl("^\\d+$", b)){
                    
                    a_int <- as.integer(a)
                    b_int <- as.integer(b)
                    h_int <- as.integer(h)
                    print("S Трапеция")
                    print((a_int + b_int) * h_int * 0.5)
                    break
                }
                else{
                    k <- k + 1
                }
            }
            
        }
        if (i == "Эллипс"){
            k <- 0
            while(TRUE){
                if (k == 3){
                    print("1234")
                    break
                }
                a <- readline()
                a <- "5"
                b <- readline()
                b <- "10"
                
                if (grepl("^\\d+$", a) & grepl("^\\d+$", b)){
                    pi = 3.14
                    a_int <- as.integer(a)
                    b_int <- as.integer(b)
                    
                    print("S Эллипс")
                    print(a_int * b_int * pi)
                    break
                }
                else{
                    k <- k + 1
                }
            }
            
        }
    }
}
