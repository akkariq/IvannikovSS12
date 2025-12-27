**Лабораторная работа 6. Функциональное программирование. Часть 4. Scala и большие данные**

**Цель работы:** Изучить применение функционального программирования в Scala, освоить работу с коллекциями, option-типами и монадическими операциями. Изучить применение ФП в контексте обработки больших данных и высоконагруженных систем.

**Задачи:**
1. Изучить базовый синтаксис Scala и систему типов
2. Освоить работу с коллекциями и функциями высшего порядка
3. Научиться использовать option-типы и Either для обработки ошибок
4. Изучить case classes и pattern matching
5. Освоить базовые принципы работы с Apache Spark в функциональном стиле

**Теоретическая часть**

**Scala как гибридный язык:**
Scala сочетает объектно-ориентированное и функциональное программирование, работая на JVM. Широко используется в Big Data экосистеме (Apache Spark, Kafka, Akka).

**Основные концепции ФП в Scala:**
*   **Иммутабельность по умолчанию** - val вместо var, иммутабельные коллекции
*   **Case classes** - для создания неизменяемых данных
*   **Pattern matching** - мощный механизм декомпозиции данных
*   **For-comprehensions** - синтаксический сахар для работы с монадами
*   **Type inference** - компилятор автоматически выводит типы

**Экосистема Big Data:**
*   **Apache Spark** - фреймворк для распределенной обработки данных
*   **Функциональные преобразования** - map, filter, reduce на распределенных данных
*   **Ленивые вычисления** - оптимизация выполнения операций

**Порядок выполнения работы**

**1. Базовый синтаксис и функции**

Создайте файл `BasicScala.scala`:

```scala
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
```

**2. Коллекции и функции высшего порядка**

Создайте файл `Collections.scala`:

```scala
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
```

**3. Option и Either для обработки ошибок**

Создайте файл `ErrorHandling.scala`:

```scala
object ErrorHandling {
  
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
  
  def findUser(id: Int): Option[User] = users.get(id)
  
  def validateUser(user: User): Either[String, User] = {
    if (user.email.contains("@")) Right(user)
    else Left(s"Invalid email for user ${user.name}")
  }
  
  def processOrder(order: Order): Either[String, (User, Order)] = {
    for {
      user <- findUser(order.userId).toRight(s"User ${order.userId} not found")
      validatedUser <- validateUser(user)
    } yield (validatedUser, order)
  }
  
  def demonstrateErrorHandling(): Unit = {
    println("=== Обработка ошибок ===")
    
    // Option
    val user1 = findUser(1)
    val user3 = findUser(3)
    
    println(s"Пользователь 1: $user1")
    println(s"Пользователь 3: $user3")
    
    // Работа с Option
    user1.foreach(user => println(s"Найден пользователь: ${user.name}"))
    val userName = user3.getOrElse("Неизвестный пользователь")
    println(s"Имя пользователя 3: $userName")
    
    // Map и flatMap с Option
    val userEmail = findUser(1).map(_.email)
    println(s"Email пользователя 1: $userEmail")
    
    // Either
    val validUser = validateUser(User(1, "John", "john@example.com"))
    val invalidUser = validateUser(User(2, "Jane", "invalid-email"))
    
    println(s"Валидный пользователь: $validUser")
    println(s"Невалидный пользователь: $invalidUser")
    
    // Обработка заказов
    val orderResults = orders.map(processOrder)
    orderResults.foreach {
      case Right((user, order)) => 
        println(s"Успешно обработан заказ для ${user.name}: $${order.amount}")
      case Left(error) => 
        println(s"Ошибка обработки заказа: $error")
    }
    
    // For-comprehension с Either
    val combinedResult = for {
      user1 <- findUser(1).toRight("User 1 not found")
      user2 <- findUser(2).toRight("User 2 not found")
    } yield s"Оба пользователя найдены: ${user1.name} и ${user2.name}"
    
    println(s"Комбинированный результат: $combinedResult")
  }
  
  def main(args: Array[String]): Unit = {
    demonstrateErrorHandling()
  }
}
```

**4. Case classes и pattern matching**

Создайте файл `PatternMatching.scala`:

```scala
object PatternMatching {
  
  // Алгебраические типы данных
  sealed trait PaymentMethod
  case class CreditCard(number: String, expiry: String) extends PaymentMethod
  case class PayPal(email: String) extends PaymentMethod
  case class Crypto(wallet: String) extends PaymentMethod
  
  sealed trait OrderStatus
  case object Pending extends OrderStatus
  case object Processing extends OrderStatus
  case class Shipped(trackingNumber: String) extends OrderStatus
  case class Delivered(deliveryDate: String) extends OrderStatus
  case class Cancelled(reason: String) extends OrderStatus
  
  case class Order(id: Int, amount: Double, payment: PaymentMethod, status: OrderStatus)
  
  def processPayment(payment: PaymentMethod): String = payment match {
    case CreditCard(number, expiry) => 
      s"Обработка кредитной карты: ${number.takeLast(4)} (до $expiry)"
    case PayPal(email) => 
      s"Обработка PayPal: $email"
    case Crypto(wallet) => 
      s"Обработка криптовалюты: ${wallet.take(10)}..."
  }
  
  def canCancelOrder(status: OrderStatus): Boolean = status match {
    case Pending | Processing => true
    case Shipped(_) | Delivered(_) | Cancelled(_) => false
  }
  
  def updateOrderStatus(order: Order, newStatus: OrderStatus): Order = {
    order.copy(status = newStatus)
  }
  
  def demonstratePatternMatching(): Unit = {
    println("=== Pattern Matching ===")
    
    val orders = List(
      Order(1, 99.99, CreditCard("1234567812345678", "12/25"), Pending),
      Order(2, 149.99, PayPal("user@example.com"), Processing),
      Order(3, 199.99, Crypto("1A2b3C4d5E6f7G8h9I0j"), Shipped("TRACK123")),
      Order(4, 79.99, CreditCard("8765432187654321", "06/24"), Delivered("2024-01-15"))
    )
    
    // Обработка платежей
    orders.foreach { order =>
      val paymentInfo = processPayment(order.payment)
      val cancelable = if (canCancelOrder(order.status)) "можно отменить" else "нельзя отменить"
      println(s"Заказ ${order.id}: $paymentInfo - $cancelable")
    }
    
    // Деструктуризация в for-comprehension
    val pendingCreditCardOrders = for {
      order <- orders
      CreditCard(number, _) <- Some(order.payment) if canCancelOrder(order.status)
    } yield order
    
    println(s"Ожидающие заказы с кредитными картами: $pendingCreditCardOrders")
    
    // Сопоставление с образцом в map
    val statusDescriptions = orders.map {
      case Order(id, amount, _, Shipped(tracking)) => 
        s"Заказ $id отправлен, трекинг: $tracking"
      case Order(id, amount, _, Delivered(date)) => 
        s"Заказ $id доставлен $date"
      case Order(id, amount, _, status) => 
        s"Заказ $id в статусе: $status"
    }
    
    statusDescriptions.foreach(println)
  }
  
  def main(args: Array[String]): Unit = {
    demonstratePatternMatching()
  }
}
```

**5. Работа с Apache Spark**

Создайте файл `SparkExample.scala`:

```scala
import org.apache.spark.sql.{SparkSession, DataFrame}
import org.apache.spark.sql.functions._

object SparkExample {
  
  case class SalesRecord(product: String, category: String, amount: Double, date: String)
  
  def createSparkSession(): SparkSession = {
    SparkSession.builder()
      .appName("ScalaFPSparkExample")
      .master("local[*]")
      .getOrCreate()
  }
  
  def demonstrateSparkOperations(spark: SparkSession): Unit = {
    import spark.implicits._
    
    println("=== Apache Spark Operations ===")
    
    // Создание тестовых данных
    val salesData = Seq(
      SalesRecord("iPhone", "electronics", 999.99, "2024-01-15"),
      SalesRecord("MacBook", "electronics", 1999.99, "2024-01-15"),
      SalesRecord("T-shirt", "clothing", 29.99, "2024-01-16"),
      SalesRecord("Jeans", "clothing", 79.99, "2024-01-16"),
      SalesRecord("iPhone", "electronics", 999.99, "2024-01-17"),
      SalesRecord("Book", "education", 15.99, "2024-01-17")
    )
    
    val salesDF = salesData.toDF()
    
    println("Исходные данные:")
    salesDF.show()
    
    // Функциональные преобразования с Spark
    val result = salesDF
      .filter(col("amount") > 50) // Фильтрация
      .groupBy("category") // Группировка
      .agg(
        sum("amount").as("total_sales"),
        avg("amount").as("avg_sale"),
        count("*").as("transaction_count")
      )
      .orderBy(desc("total_sales")) // Сортировка
    
    println("Агрегированные результаты:")
    result.show()
    
    // Использование функций высшего порядка
    val expensiveProducts = salesDF
      .map(row => (row.getAs[String]("product"), row.getAs[Double]("amount")))
      .filter { case (product, amount) => amount > 500 }
      .collect()
    
    println("Дорогие продукты:")
    expensiveProducts.foreach(println)
    
    // Обработка с использованием case classes
    val processedData = salesDF
      .as[SalesRecord]
      .map(record => record.copy(amount = record.amount * 1.1)) // 10% надбавка
      .filter(_.category != "education")
      .collect()
    
    println("Обработанные данные (без образования, +10%):")
    processedData.foreach(println)
  }
  
  def main(args: Array[String]): Unit = {
    val spark = createSparkSession()
    
    try {
      demonstrateSparkOperations(spark)
    } finally {
      spark.stop()
    }
  }
}
```

**6. Практические задания**

**Задание 1:** Реализуйте функцию для анализа продаж

```scala
def analyzeSales(sales: List[SalesRecord]): Map[String, (Double, Int)] = {
  // TODO: Вернуть Map[категория -> (общая сумма, количество продаж)]
  // Использовать groupBy и mapValues
}
```

**Задание 2:** Создайте тип для обработки цепочки операций с ошибками

```scala
def processOrderPipeline(order: Order): Either[String, Double] = {
  // TODO: Реализовать цепочку: проверка пользователя -> проверка платежа -> расчет скидки
  // Использовать for-comprehension с Either
}
```

**Задание 3:** Реализуйте Spark job для анализа данных

```scala
def createSalesReport(df: DataFrame): DataFrame = {
  // TODO: Создать отчет с: общей выручкой по дням, популярными товарами, средней ценой по категориям
}
```

**Пример выполнения программы:**

```scala
// Main.scala
object Main {
  def main(args: Array[String]): Unit = {
    println("=== Scala Функциональное Программирование ===")
    
    // Базовые операции
    BasicScala.main(Array())
    
    // Коллекции
    Collections.demonstrateCollections()
    
    // Обработка ошибок
    ErrorHandling.demonstrateErrorHandling()
    
    // Pattern matching
    PatternMatching.demonstratePatternMatching()
    
    // Spark (требует установленного Spark)
    // SparkExample.main(Array())
  }
}
```

**Зависимости для build.sbt:**

```scala
name := "scala-fp-lab"
version := "1.0"
scalaVersion := "2.13.10"

libraryDependencies ++= Seq(
  "org.apache.spark" %% "spark-core" % "3.4.0",
  "org.apache.spark" %% "spark-sql" % "3.4.0"
)
```

**Критерии оценки**

**Удовлетворительно:**
*   Реализованы базовые функции и работа с коллекциями
*   Использованы case classes и простой pattern matching
*   Выполнены простые операции с Option

**Хорошо:**
*   Корректно реализованы функции высшего порядка
*   Использованы for-comprehensions и Either для обработки ошибок
*   Созданы сложные pattern matching с case classes
*   Выполнены основные практические задания

**Отлично:**
*   Эффективно использованы монадические операции и композиция
*   Реализованы оптимизированные преобразования с хвостовой рекурсией
*   Созданы распределенные вычисления с Apache Spark
*   Код хорошо структурирован и использует лучшие практики Scala
*   Реализованы все практические задания и дополнительные задачи

**Контрольные вопросы**
1.  Чем отличается var от val в Scala и почему рекомендуется использовать val?
2.  Как работают for-comprehensions и какие типы можно в них использовать?
3.  В чем преимущество использования Option и Either вместо исключений?
4.  Как pattern matching помогает в функциональном программировании?
5.  Какие преимущества дает использование ФП подходов в Apache Spark?

**Рекомендованная литература**
1.  "Programming in Scala" Martin Odersky, Lex Spoon, Bill Venners
2.  "Functional Programming in Scala" Paul Chiusano, Rúnar Bjarnason
3.  "Scala with Cats" Noel Welsh, Dave Gurnell
4.  Официальная документация Apache Spark
5.  "Spark: The Definitive Guide" Bill Chambers, Matei Zaharia