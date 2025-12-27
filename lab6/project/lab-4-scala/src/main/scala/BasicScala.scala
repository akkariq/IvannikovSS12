object BasicScala {

  // Функции первого класса
  val square: Int => Int = (x: Int) => x * x
  val add: (Int, Int) => Int = (a, b) => a + b

  // Функции высшего порядка
  def applyFunction(f: Int => Int, x: Int): Int = f(x)

  // Каррирование
  def multiply(a: Int)(b: Int): Int = a * b
  val double = multiply(2)_

  // Рекурсия
  def factorial(n: Int): Int = {
    if (n <= 1) 1
    else n * factorial(n - 1)
  }

  // Хвостовая рекурсия
  def factorialTailrec(n: Int): Int = {
    @annotation.tailrec
    def loop(acc: Int, n: Int): Int = {
      if (n <= 1) acc
      else loop(acc * n, n - 1)
    }
    loop(1, n)
  }

  def main(args: Array[String]): Unit = {
    println(s"Квадрат 5: ${square(5)}")
    println(s"Сложение 3 и 4: ${add(3, 4)}")
    println(s"Применение функции: ${applyFunction(square, 3)}")
    println(s"Удвоение 7: ${double(7)}")
    println(s"Факториал 5: ${factorial(5)}")
    println(s"Факториал хвостовой 5: ${factorialTailrec(5)}")
  }
}