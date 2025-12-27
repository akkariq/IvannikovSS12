
foo <- function(n) {
    if (n <= 0) {
        return(1)
    } else {
        return (n *foo(n - 1))
    }
}