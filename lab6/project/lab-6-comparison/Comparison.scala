[file name]: Comparison.scala
[file content begin]
object Comparison {
  
  import scala.annotation.tailrec
  import scala.util.{Try, Success, Failure}
  import scala.concurrent.duration._
  
  // Модель данных
  case class User(id: Int, name: String, email: String)
  case class Product(id: Int, name: String, price: Double, category: String)
  case class OrderItem(product: Product, quantity: Int)
  case class Order(id: Int, user: User, items: List[OrderItem], status: String)
  
  // Пример данных (с возможными ошибками)
  val users = List(
    User(1, "John Doe", "john@example.com"),
    User(2, "Jane Smith", "jane@example.com")
  )
  
  val products = List(
    Product(1, "iPhone", 999.99, "electronics"),
    Product(2, "MacBook", 1999.99, "electronics"),
    Product(3, "T-shirt", 29.99, "clothing"),
    Product(4, "Defective", Double.NaN, "electronics"), // Потенциальная ошибка
    Product(5, "Free", 0.0, "clothing")
  )
  
  val orders = List(
    Order(1, users(0), List(OrderItem(products(0), 1), OrderItem(products(2), 2)), "completed"),
    Order(2, users(1), List(OrderItem(products(1), 1)), "pending"),
    Order(3, users(0), List(OrderItem(products(3), 1)), "error"), // Заказ с ошибкой
    Order(4, users(1), List(), "empty"), // Пустой заказ
    Order(5, users(0), null, "null") // Null заказ
  )
  
  // Базовая функция расчета (без обработки ошибок)
  def calculateOrderTotal(order: Order): Double = 
    order.items.map(item => item.product.price * item.quantity).sum
  
  // Задание 3: Обработка ошибок в Scala
  // Вариант 1: Использование Try (функциональный стиль)
  def safeCalculateTotalTry(order: Order): Try[Double] = {
    Try {
      // Может выбросить исключение если items == null
      order.items.map(item => item.product.price * item.quantity).sum
    }
  }
  
  // Вариант 2: Использование Option (если не нужно знать причину ошибки)
  def safeCalculateTotalOption(order: Order): Option[Double] = {
    if (order.items == null) None
    else {
      val total = order.items.foldLeft(Option(0.0)) { (acc, item) =>
        for {
          sum <- acc
          price = item.product.price
          // Проверка на некорректные значения
          if !price.isNaN && !price.isInfinite
          quantity = item.quantity
          if quantity >= 0
        } yield sum + (price * quantity)
      }
      total.filter(_ >= 0) // Исключаем отрицательные суммы
    }
  }
  
  // Вариант 3: Использование Either (с информацией об ошибке)
  def safeCalculateTotalEither(order: Order): Either[String, Double] = {
    if (order.items == null) 
      Left(s"Order ${order.id}: items list is null")
    else if (order.items.isEmpty)
      Left(s"Order ${order.id}: items list is empty")
    else {
      order.items.foldLeft(Right(0.0): Either[String, Double]) { (acc, item) =>
        acc.flatMap { sum =>
          val price = item.product.price
          val quantity = item.quantity
          
          if (price.isNaN || price.isInfinite)
            Left(s"Order ${order.id}: invalid price ${price} for product ${item.product.name}")
          else if (quantity < 0)
            Left(s"Order ${order.id}: negative quantity ${quantity} for product ${item.product.name}")
          else
            Right(sum + (price * quantity))
        }
      }
    }
  }
  
  // Вариант 4: Использование собственного типа ошибок
  sealed trait CalculationError
  case object NullItems extends CalculationError
  case object EmptyItems extends CalculationError
  case class InvalidPrice(productName: String, price: Double) extends CalculationError
  case class InvalidQuantity(productName: String, quantity: Int) extends CalculationError
  
  def safeCalculateTotalCustom(order: Order): Either[CalculationError, Double] = {
    if (order.items == null) Left(NullItems)
    else if (order.items.isEmpty) Left(EmptyItems)
    else {
      order.items.foldLeft(Right(0.0): Either[CalculationError, Double]) { (acc, item) =>
        acc.flatMap { sum =>
          val price = item.product.price
          val quantity = item.quantity
          
          if (price.isNaN || price.isInfinite)
            Left(InvalidPrice(item.product.name, price))
          else if (quantity < 0)
            Left(InvalidQuantity(item.product.name, quantity))
          else
            Right(sum + (price * quantity))
        }
      }
    }
  }
  
  // Пример использования разных подходов
  def demonstrateErrorHandling(): Unit = {
    println("\n" + "="*60)
    println("ОБРАБОТКА ОШИБОК В SCALA")
    println("="*60)
    
    orders.foreach { order =>
      println(s"\nЗаказ #${order.id} (статус: ${order.status}):")
      
      // Вариант 1: Try
      safeCalculateTotalTry(order) match {
        case Success(total) => println(s"  Try: Успех - $total")
        case Failure(exception) => println(s"  Try: Ошибка - ${exception.getMessage}")
      }
      
      // Вариант 2: Option
      safeCalculateTotalOption(order) match {
        case Some(total) => println(s"  Option: Успех - $total")
        case None => println(s"  Option: Ошибка - невозможно вычислить")
      }
      
      // Вариант 3: Either
      safeCalculateTotalEither(order) match {
        case Right(total) => println(s"  Either: Успех - $total")
        case Left(error) => println(s"  Either: Ошибка - $error")
      }
      
      // Вариант 4: Пользовательские ошибки
      safeCalculateTotalCustom(order) match {
        case Right(total) => println(s"  Custom: Успех - $total")
        case Left(NullItems) => println(s"  Custom: Ошибка - список товаров null")
        case Left(EmptyItems) => println(s"  Custom: Ошибка - список товаров пуст")
        case Left(InvalidPrice(name, price)) => println(s"  Custom: Ошибка - некорректная цена $price для $name")
        case Left(InvalidQuantity(name, quantity)) => println(s"  Custom: Ошибка - некорректное количество $quantity для $name")
      }
    }
  }
  
  // Обработка ошибок в цепочке вычислений
  def processOrderChain(order: Order): Either[String, (Double, Double)] = {
    for {
      total <- safeCalculateTotalEither(order)
      discounted = if (total > 1000) total * 0.9 else total // Скидка 10% для заказов > 1000
      _ <- Either.cond(discounted >= 0, (), "Отрицательная итоговая сумма")
    } yield (total, discounted)
  }
  
  def main(args: Array[String]): Unit = {
    println("=== SCALA - Обработка заказов с ошибками ===")
    
    // Демонстрация обработки ошибок
    demonstrateErrorHandling()
    
    // Пример обработки цепочки
    println("\n" + "="*60)
    println("ОБРАБОТКА ЦЕПОЧКИ ВЫЧИСЛЕНИЙ")
    println("="*60)
    
    orders.take(2).foreach { order =>
      processOrderChain(order) match {
        case Right((original, discounted)) =>
          println(s"Заказ #${order.id}: оригинал = $original, со скидкой = $discounted")
        case Left(error) =>
          println(s"Заказ #${order.id}: ошибка - $error")
      }
    }
    
    println("\n" + "="*60)
    println("ПРЕИМУЩЕСТВА SCALA ДЛЯ ОБРАБОТКИ ОШИБОК")
    println("="*60)
    println("""
    1. Try/Success/Failure - функциональная обработка исключений
    2. Option - для значений, которые могут отсутствовать
    3. Either - возвращает либо результат, либо ошибку
    4. For-comprehension - удобная композиция операций с ошибками
    5. Паттерн-матчинг - декларативная обработка разных случаев
    6. Компилятор заставляет обрабатывать все варианты
    """)
  }
}
[file content end]