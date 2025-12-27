import org.apache.spark.sql.{DataFrame, SparkSession}
import org.apache.spark.sql.functions._

object Zadanie {

  case class SalesRecord(product: String, category: String, amount: Double, date: String)
  val salesData = List(
    SalesRecord("iPhone", "electronics", 999.99, "2024-01-15"),
    SalesRecord("MacBook", "electronics", 1999.99, "2024-01-15"),
    SalesRecord("T-shirt", "clothing", 29.99, "2024-01-16"),
    SalesRecord("Jeans", "clothing", 79.99, "2024-01-16"),
    SalesRecord("iPhone", "electronics", 999.99, "2024-01-17"),
    SalesRecord("Book", "education", 15.99, "2024-01-17")
  )

  case class User(id: Int, name: String, email: String)
  case class Order(userId: Int, amount: Double, status: String)

  val users = Map(
    1 -> User(1, "John Doe", "john@example.com"),
    2 -> User(2, "Jane Smith", "jane@example.com")
  )

  val orders = List(
    Order(1, 99.99, "completed"),
    Order(2, 149.99, "pending"),
    Order(3, 199.99, "shipped") // Пользователя с id=3 не существует
  )

  val spark: SparkSession = SparkSession.builder()
    .appName("SalesReport")
    .master("local[*]")
    .getOrCreate()

  import spark.implicits._

  def analyzeSales(sales: List[SalesRecord]): Map[String, (Double, Int)] = {
    val productNames = sales.map(_.product)
    println(s"Названия продуктов: $productNames")

    sales.groupBy(_.category)
      .mapValues { records =>
        (records.map(_.amount).sum, records.size)
      }
      .toMap
  }

  def processOrderPipeline(order: Order): Either[String, Double] = {
    for {
      user <- validateUser(order.userId)
      validOrder <- validatePayment(order)
      finalAmount <- calculateDiscount(validOrder)
    } yield finalAmount
  }

  def validateUser(userId: Int): Either[String, User] = {
    users.get(userId) match {
      case Some(user) => Right(user)
      case None => Left(s"Пользователь с id=$userId не найден")
    }
  }

  def validatePayment(order: Order): Either[String, Order] = {
    if (order.amount > 0) {
      Right(order)
    } else {
      Left("Неверная сумма платежа")
    }
  }

  def calculateDiscount(order: Order): Either[String, Double] = {
    val discount = if (order.amount > 100) order.amount * 0.9 else order.amount
    Right(discount)
  }

  def createSalesReport(df: DataFrame): DataFrame = {
    df
      .groupBy("date")
      .agg(sum("amount").as("daily_revenue"))
      .orderBy("date")
  }

  def createDetailedSalesReport(df: DataFrame): DataFrame = {
    df
      .groupBy("date", "category")
      .agg(
        sum("amount").as("total_revenue"),
        count("*").as("transaction_count"),
        avg("amount").as("avg_price"),
        collect_list("product").as("products_sold")
      )
      .orderBy(desc("total_revenue"))
  }

  def createPopularProductsReport(df: DataFrame): DataFrame = {
    df
      .groupBy("product")
      .agg(
        sum("amount").as("total_revenue"),
        count("*").as("sales_count")
      )
      .orderBy(desc("total_revenue"))
  }

  def main(args: Array[String]): Unit = {
    println("=== Анализ продаж (чистая Scala) ===")
    val result = analyzeSales(salesData)
    println(result)

    println("\n=== Обработка заказов ===")
    orders.foreach { order =>
      val processed = processOrderPipeline(order)
      processed match {
        case Right(amount) => println(s"Заказ пользователя ${order.userId}: успешно обработан, итоговая сумма: $$${amount}")
        case Left(error) => println(s"Заказ пользователя ${order.userId}: ошибка - $error")
      }
    }

    println("\n" + "="*50)
    println("=== SPARK ОТЧЕТЫ ===")
    println("="*50)

    // Создаем DataFrame из salesData
    val salesDF = salesData.toDF()

    println("\n1. Исходные данные:")
    salesDF.show()

    println("\n2. Выручка по дням:")
    val dailyReport = createSalesReport(salesDF)
    dailyReport.show()

    println("\n3. Детальный отчет по категориям:")
    val detailedReport = createDetailedSalesReport(salesDF)
    detailedReport.show()

    println("\n4. Популярные товары:")
    val popularProducts = createPopularProductsReport(salesDF)
    popularProducts.show()

    // Дополнительные анализы
    println("\n5. Дополнительная аналитика:")

    // Топ категории по выручке
    val topCategories = salesDF
      .groupBy("category")
      .agg(
        sum("amount").as("total_revenue"),
        avg("amount").as("avg_price"),
        count("*").as("sales_count")
      )
      .orderBy(desc("total_revenue"))

    println("Топ категории по выручке:")
    topCategories.show()

    // Ежедневная статистика
    val dailyStats = salesDF
      .groupBy("date")
      .agg(
        sum("amount").as("daily_revenue"),
        count("*").as("daily_transactions"),
        avg("amount").as("avg_transaction_size")
      )
      .orderBy("date")

    println("Ежедневная статистика:")
    dailyStats.show()


    // Останавливаем Spark сессию
    spark.stop()
  }
}