#[derive(Debug, Clone)]
struct Product {
    id: u32,
    name: String,
    price: f64,
    category: String,
    in_stock: bool,
}

impl Product {
    fn new(id: u32, name: &str, price: f64, category: &str, in_stock: bool) -> Self {
        Product {
            id,
            name: name.to_string(),
            price,
            category: category.to_string(),
            in_stock,
        }
    }
}

fn analyze_products(products: &[Product]) -> (f64, usize, Vec<&Product>) {
    // Вычисляем среднюю цену
    let total_price: f64 = products.iter().map(|p| p.price).sum();
    let avg_price = if products.is_empty() {
        0.0
    } else {
        total_price / products.len() as f64
    };
    
    // Считаем количество доступных продуктов
    let available_count = products.iter().filter(|p| p.in_stock).count();
    
    // Собираем список дорогих продуктов (цена > 100)
    let expensive_products: Vec<&Product> = products
        .iter()
        .filter(|p| p.price > 100.0)
        .collect();
    
    (avg_price, available_count, expensive_products)
}

// Добавляем необходимые структуры для валидации заказов
#[derive(Debug)]
struct Order {
    id: u32,
    amount: f64,
    status: String,
}

impl Order {
    fn new(id: u32, amount: f64, status: &str) -> Self {
        Order {
            id,
            amount,
            status: status.to_string(),
        }
    }
}

#[derive(Debug)]
enum OrderError {
    InvalidAmount(u32, f64),
    InvalidStatus(u32, String),
}

type OrderValidator = fn(&Order) -> Result<(), OrderError>;

// Добавляем явное указание времени жизни
fn validate_orders_with_custom<'a>(
    orders: &'a [Order], 
    validators: &[OrderValidator]
) -> Result<Vec<&'a Order>, OrderError> {
    orders
        .iter()
        .try_fold(Vec::new(), |mut acc, order| {
            for validator in validators {
                validator(order)?;
            }
            acc.push(order);
            Ok(acc)
        })
}

// Примеры валидаторов
fn validate_amount(order: &Order) -> Result<(), OrderError> {
    if order.amount <= 0.0 || order.amount > 10_000.0 {
        Err(OrderError::InvalidAmount(order.id, order.amount))
    } else {
        Ok(())
    }
}

fn validate_status(order: &Order) -> Result<(), OrderError> {
    let valid = ["pending", "processing", "shipped", "delivered", "cancelled"];
    if valid.contains(&order.status.as_str()) {
        Ok(())
    } else {
        Err(OrderError::InvalidStatus(order.id, order.status.clone()))
    }
}

struct Fibonacci {
    current: u64,
    next: u64,
}

impl Fibonacci {
    fn new() -> Self {
        Fibonacci { current: 0, next: 1 }
    }
}

impl Iterator for Fibonacci {
    type Item = u64;
    
    fn next(&mut self) -> Option<Self::Item> {
        let current = self.current;
        
        // Вычисляем следующее число
        self.current = self.next;
        self.next = current + self.next;
        
        Some(current)
    }
}

fn main() {
    // Часть 1: Анализ продуктов
    println!("=== Анализ продуктов ===");
    let products = vec![
        Product::new(1, "iPhone", 999.99, "electronics", true),
        Product::new(2, "MacBook", 1999.99, "electronics", false),
        Product::new(3, "T-shirt", 29.99, "clothing", true),
        Product::new(4, "Jeans", 79.99, "clothing", true),
        Product::new(5, "Book", 15.99, "education", false),
    ];
    
    let (avg_price, available_count, expensive_products) = analyze_products(&products);
    
    println!("Средняя цена: {:.2}", avg_price);
    println!("Доступно продуктов: {}", available_count);
    println!("Дорогих продуктов (> 100):");
    for product in expensive_products {
        println!("  - {}: ${:.2}", product.name, product.price);
    }
    
    // Часть 2: Валидация заказов
    println!("\n=== Валидация заказов ===");
    let orders = vec![
        Order::new(1, 99.99, "pending"),
        Order::new(2, 15000.0, "processing"), // Невалидная сумма
        Order::new(3, 50.0, "invalid_status"),
    ];
    
    let validators: [OrderValidator; 2] = [validate_amount, validate_status];
    
    match validate_orders_with_custom(&orders, &validators) {
        Ok(valid_orders) => {
            println!("Все заказы валидны!");
            for order in valid_orders {
                println!("  - Заказ {}: ${:.2}, статус: {}", 
                    order.id, order.amount, order.status);
            }
        }
        Err(error) => {
            println!("Ошибка валидации: {:?}", error);
        }
    }
    
    // Часть 3: Итератор Фибоначчи
    println!("\n=== Числа Фибоначчи ===");
    
    // Создаем итератор
    let fib = Fibonacci::new();
    
    // Берем первые 10 чисел
    let first_10: Vec<u64> = fib.take(10).collect();
    println!("Первые 10 чисел Фибоначчи: {:?}", first_10);
    
    // Еще примеры использования итератора
    println!("Каждое 3-е число из первых 15:");
    let fib2 = Fibonacci::new();
    for (i, num) in fib2.take(15).enumerate() {
        if i % 3 == 0 {
            println!("  F[{}] = {}", i, num);
        }
    }
    
    // Находим первое число Фибоначчи > 1000
    let fib3 = Fibonacci::new();
    if let Some(num) = fib3.skip_while(|&x| x <= 1000).next() {
        println!("Первое число Фибоначчи > 1000: {}", num);
    }
    
    // Сумма первых 20 чисел Фибоначчи
    let fib4 = Fibonacci::new();
    let sum: u64 = fib4.take(20).sum();
    println!("Сумма первых 20 чисел Фибоначчи: {}", sum);
}