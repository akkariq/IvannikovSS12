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