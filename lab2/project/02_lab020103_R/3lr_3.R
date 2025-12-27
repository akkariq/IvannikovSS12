library(R6)

Kopilka <- R6Class("Kopilka",
	public = list(
		symma = NULL,

		initialize = function(symma, sostoaine, popolnenie) {
			self$symma <- symma
		},

		balance = function() {
			cat("В копилке",self$symma,"\n")
		},

		dep = function(popolnenie) {
			self$symma = self$symma + popolnenie
		}

	)	
)

kopilo4ka <- Kopilka$new(0)

kopilo4ka$balance()
kopilo4ka$dep(100)
kopilo4ka$balance()