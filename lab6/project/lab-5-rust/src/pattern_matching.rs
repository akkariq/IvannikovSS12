// Алгебраические типы данных
#[derive(Debug)]
enum PaymentMethod {
    CreditCard { number: String, expiry: String },
    PayPal { email: String },
    Crypto { wallet: String },
}

#[derive(Debug)]
enum OrderStatus {
    Pending,
    Processing,
    Shipped(String), // tracking number
    Delivered(String), // delivery date
    Cancelled { reason: String },
}

#[derive(Debug)]
struct Order {
    #[allow(dead_code)]
    id: u32,
    #[allow(dead_code)]
    amount: f64,
    payment: PaymentMethod,
    status: OrderStatus,
}

impl Order {
    fn new(id: u32, amount: f64, payment: PaymentMethod, status: OrderStatus) -> Self {
        Order { id, amount, payment, status }
    }
}

fn process_payment(payment: &PaymentMethod) -> String {
    match payment {
        PaymentMethod::CreditCard { number, expiry } => {
            let last_four = number.chars().rev().take(4).collect::<String>();
            format!("Обработка кредитной карты: ****{} (до {})", last_four, expiry)
        }
        PaymentMethod::PayPal { email } => {
            format!("Обработка PayPal: {}", email)
        }
        PaymentMethod::Crypto { wallet } => {
            let shortened = wallet.chars().take(10).collect::<String>();
            format!("Обработка криптовалюты: {}...", shortened)
        }
    }
}

fn can_cancel_order(status: &OrderStatus) -> bool {
    match status {
        OrderStatus::Pending | OrderStatus::Processing => true,
        OrderStatus::Shipped(_) | OrderStatus::Delivered(_) | OrderStatus::Cancelled { .. } => false,
    }
}

fn update_order_status(order: Order, new_status: OrderStatus) -> Order {
    Order { status: new_status, ..order }
}

fn demonstrate_pattern_matching() {
    println!("\n=== Pattern Matching ===");
    
    let orders = vec![
        Order::new(
            1, 
            99.99, 
            PaymentMethod::CreditCard { 
                number: "1234567812345678".to_string(), 
                expiry: "12/25".to_string() 
            }, 
            OrderStatus::Pending
        ),
        Order::new(
            2, 
            149.99, 
            PaymentMethod::PayPal { 
                email: "user@example.com".to_string() 
            }, 
            OrderStatus::Processing
        ),
        Order::new(
            3, 
            199.99, 
            PaymentMethod::Crypto { 
                wallet: "1A2b3C4d5E6f7G8h9I0j".to_string() 
            }, 
            OrderStatus::Shipped("TRACK123".to_string())
        ),
    ];
    
    // Обработка заказов с pattern matching
    for order in &orders {
        let payment_info = process_payment(&order.payment);
        let cancelable = if can_cancel_order(&order.status) { 
            "можно отменить" 
        } else { 
            "нельзя отменить" 
        };
        println!("Заказ {}: {} - {}", order.id, payment_info, cancelable);
    }
    
    // Деструктуризация в if let
    for order in orders {
        if let OrderStatus::Shipped(tracking) = &order.status {
            println!("Заказ {} отправлен, трекинг: {}", order.id, tracking);
        }
        
        // Сопоставление с несколькими паттернами
        match order.status {
            OrderStatus::Delivered(date) => {
                println!("Заказ {} доставлен {}", order.id, date);
            }
            OrderStatus::Cancelled { reason } => {
                println!("Заказ {} отменен: {}", order.id, reason);
            }
            _ => {} // Игнорируем другие статусы
        }
    }
}

fn main() {
    
    demonstrate_pattern_matching();
}