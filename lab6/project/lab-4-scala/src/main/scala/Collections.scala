object Collections {

  // Данные для работы
  case class Product(id: Int, name: String, price: Double, category: String, inStock: Boolean)

  val products = List(
    Product(1, "iPhone", 999.99, "electronics", true),
    Product(2, "MacBook", 1999.99, "electronics", false),
    Product(3, "T-shirt", 29.99, "clothing", true),
    Product(4, "Jeans", 79.99, "clothing", true),
    Product(5, "Book", 15.99, "education", false)
  )

  val numbers = List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

  def demonstrateCollections(): Unit = {
    println("=== Работа с коллекциями ===")

    // Map
    val productNames = products.map(_.name)
    println(s"Названия продуктов: $productNames")

    val discountedPrices = products.map(p => p.copy(price = p.price * 0.9))
    println(s"Продукты со скидкой: $discountedPrices")

    // Filter
    val availableProducts = products.filter(_.inStock)
    println(s"Доступные продукты: $availableProducts")

    val expensiveProducts = products.filter(_.price > 100)
    println(s"Дорогие продукты: $expensiveProducts")

    // Reduce
    val totalPrice = products.map(_.price).reduce(_ + _)
    println(s"Общая стоимость: $totalPrice")

    // Fold
    val totalStockValue = products.foldLeft(0.0)((acc, p) => acc + p.price)
    println(s"Общая стоимость через fold: $totalStockValue")

    // GroupBy
    val productsByCategory = products.groupBy(_.category)
    println(s"Продукты по категориям: $productsByCategory")

    // For-comprehension
    val result = for {
      product <- products
      if product.inStock && product.price > 50
    } yield product.name.toUpperCase()

    println(s"Результат for-comprehension: $result")

    // Цепочка преобразований
    val chainResult = products
      .filter(_.inStock)
      .map(p => (p.name, p.price * 0.8)) // 20% скидка
      .sortBy(-_._2) // Сортировка по убыванию цены
      .take(3) // Топ-3

    println(s"Цепочка преобразований: $chainResult")
  }

  def main(args: Array[String]): Unit = {
    demonstrateCollections()
  }
}