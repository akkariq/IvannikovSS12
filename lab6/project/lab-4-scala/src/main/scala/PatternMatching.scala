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
      s"Обработка кредитной карты: ${number.takeRight(4)} (до $expiry)"
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