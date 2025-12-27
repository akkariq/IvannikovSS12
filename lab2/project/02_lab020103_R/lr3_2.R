library(R6)

Pe4 <- R6Class("pe4",
    public = list(

        strong = NULL,
        dver = NULL,

        initialize = function(strong, dver) {
            self$strong <- strong
            self$dver <- dver
        },

        open = function() {
            if(self$dver == "open") {
                cat("Дверь и так открыта\n")
            }
            else if(self$dver == "close") {
                cat("Дверь открыта\n")
                self$dver = "open"
            }
            
        },
        close = function() {
            if(self$dver == "open") {
                cat("Дверь и так открыта\n")
                self$dver = "close"
            }
            else if(self$dver == "close") {
                cat("Дверь и так закрыта\n")
            }
            
        },

        status = function() {
            cat("Pe4': strong =", self$strong, ", dver =", self$dver, "\n")
        },

        gotovka_pishi = function() {
            cat("пища готовиться",2100 / self$strong, "\n")
            Sys.sleep(2100 / self$strong)
            cat("пища готова\n")
        }


    )
)

pe4ka <- Pe4$new(700,"open")
pe4ka2 <- Pe4$new(300,"close")

pe4ka$status()      # Печь: strong = 100, dver = open
pe4ka$close()
pe4ka$gotovka_pishi()

pe4ka2$close()
pe4ka2$gotovka_pishi()