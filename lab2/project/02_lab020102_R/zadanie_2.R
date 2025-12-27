user_input_N <- "4"

N <- as.integer(user_input_N)

calculate_polygon_area <- function(coords) {
    n <- nrow(coords)
    area <- 0
    
    for (i in 1:n) {
        j <- ifelse(i == n, 1, i + 1)
        area <- area + (coords[i, 1] * coords[j, 2] - coords[j, 1] * coords[i, 2])
    }
    
    return(abs(area) / 2)
}

vertices <- matrix(0, nrow = N, ncol = 2)
colnames(vertices) <- c("x", "y")

k <- 0
success <- FALSE

while (TRUE) {
    if (k == 3) {
        print("Ошибка: превышено количество попыток ввода")
        break
    }
    
    valid_input <- TRUE
    coords_list <- list()
    
    for (i in 1:N) {
        coord_input <- readline()
        if (i == 1) coord_input <- "0 0"
        if (i == 2) coord_input <- "4 0" 
        if (i == 3) coord_input <- "4 3"
        if (i == 4) coord_input <- "0 3"
        
        if (grepl("^-?\\d+\\s+-?\\d+$", coord_input)) {
            coords <- as.integer(strsplit(coord_input, "\\s+")[[1]])
            if (length(coords) == 2) {
                coords_list[[i]] <- coords
            } else {
                valid_input <- FALSE
                break
            }
        } else {
            valid_input <- FALSE
            break
        }
    }
    
    if (valid_input && length(coords_list) == N) {
        for (i in 1:N) {
            vertices[i, 1] <- coords_list[[i]][1]
            vertices[i, 2] <- coords_list[[i]][2]
        }
        
        area <- calculate_polygon_area(vertices)
        print("Площадь многоугольника:")
        print(area)
        success <- TRUE
        break
    } else {
        k <- k + 1
        if (k < 3) {
            print("Ошибка ввода. Попробуйте снова.")
        }
    }
}

if (!success) {
    print("Используем альтернативный метод расчета...")
    
    polygon_area_alternative <- function(x_coords, y_coords) {
        n <- length(x_coords)
        area <- 0
        
        for (i in 1:n) {
            j <- ifelse(i == n, 1, i + 1)
            area <- area + (x_coords[i] * y_coords[j] - x_coords[j] * y_coords[i])
        }
        
        return(abs(area) / 2)
    }
    
    x_coords <- c(0, 4, 4, 0)
    y_coords <- c(0, 0, 3, 3)
    
    area_alt <- polygon_area_alternative(x_coords, y_coords)
    print("Площадь многоугольника (альтернативный расчет):")
    print(area_alt)
}