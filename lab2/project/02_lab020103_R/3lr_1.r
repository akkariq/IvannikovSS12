library(R6)


# создаём обобщённую функцию
my_summary <- function(object, ...) {
    UseMethod('my_summary')
}

my_summary.default <- function(object) {
    length(object)
  
}


# Создаём R6 класс
Figyra <- R6Class("Figyra",
    public = list(
        parameters = NULL,
        initialize = function(parameters) {
            self$parameters <- parameters
        },

        calculate_area = function() {
            warning("Невозможно обработать данные: неизвестный тип фигуры")
            return(NA)
        }
    )
)

# Создаём S3 метод для этого класса
calculate_area <- function(shape) {
    UseMethod("calculate_area")
}

calculate_area.Figyra <- function(shape, ...) {
    shape$calculate_area()
}

Circle <- R6Class(
    "Circle",
    inherit = Figyra,
    public = list(
        initialize = function(radius) {
        if (radius <= 0) stop("Радиус должен быть положительным")
        super$initialize(c(radius = radius))
        },
        
        calculate_area = function() {
        radius <- self$parameters["radius"]
        area <- pi * radius^2
        cat("Площадь круга с радиусом", radius, "=", round(area, 2), "\n")
        return(area)
        }
    )
)

Kvadrat <- R6Class(
    "Kvadrat",
    inherit = Figyra,
    public = list(
        initialize = function(storona) {
        if (storona <= 0) stop("Сторона должна быть положительной")
        super$initialize(c(storona = storona))
        },
        
        calculate_area = function() {
        storona <- self$parameters["storona"]
        area <- storona^2
        cat("Площадь квадрата с стороной", storona, "=", round(area, 2), "\n")
        return(area)
        }
    )
)

circle <- Circle$new(5)
kvadrat <- Kvadrat$new(5)
calculate_area(circle)
calculate_area(kvadrat)