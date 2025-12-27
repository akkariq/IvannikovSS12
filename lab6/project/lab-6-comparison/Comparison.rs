[file name]: Comparison.rs
[file content begin]
use std::time::Instant;
use std::fmt;
use std::error::Error;

// Модель данных
#[derive(Debug, Clone)]
struct User {
    id: u32,
    name: String,
    email: String,
}

#[derive(Debug, Clone)]
struct Product {
    id: u32,
    name: String,
    price: f64,
    category: String,
}

#[derive(Debug, Clone)]
struct OrderItem {
    product: Product,
    quantity: i32, // Изменено на i32 для демонстрации ошибок
}

#[derive(Debug, Clone)]
struct Order {
    id: u32,
    user: User,
    items: Option<Vec<OrderItem>>, // Option для демонстрации обработки ошибок
    status: String,
}

#[derive(Debug)]
enum OrderError {
    NoItems,
    InvalidPrice(String, f64),
    InvalidQuantity(String, i32),
    CalculationOverflow,
    NegativeTotal,
}

impl fmt::Display for OrderError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match self {
            OrderError::NoItems => write!(f, "Заказ не содержит товаров"),
            OrderError::InvalidPrice(name, price) => 
                write!(f, "Некорректная цена {} для товара {}", price, name),
            OrderError::InvalidQuantity(name, quantity) => 
                write!(f, "Некорректное количество {} для товара {}", quantity, name),
            OrderError::CalculationOverflow => 
                write!(f, "Переполнение при расчете"),
            OrderError::NegativeTotal => 
                write!(f, "Отрицательная итоговая сумма"),
        }
    }
}

impl Error for OrderError {}

impl User {
    fn new(id: u32, name: &str, email: &str) -> Self {
        User {
            id,
            name: name.to_string(),
            email: email.to_string(),
        }
    }
}

impl Product {
    fn new(id: u32, name: &str, price: f64, category: &str) -> Self {
        Product {
            id,
            name: name.to_string(),
            price,
            category: category.to_string(),
        }
    }
}

impl OrderItem {
    fn new(product: Product, quantity: i32) -> Self {
        OrderItem { product, quantity }
    }
}

impl Order {
    fn new(id: u32, user: User, items: Option<Vec<OrderItem>>, status: &str) -> Self {
        Order {
            id,
            user,
            items,
            status: status.to_string(),
        }
    }
}

// Задание 3: Обработка ошибок в Rust
// Вариант 1: Result с пользовательскими ошибками
fn safe_calculate_total_result(order: &Order) -> Result<f64, OrderError> {
    let items = order.items.as_ref().ok_or(OrderError::NoItems)?;
    
    if items.is_empty() {
        return Err(OrderError::NoItems);
    }
    
    let mut total = 0.0;
    
    for item in items {
        let price = item.product.price;
        let quantity = item.quantity;
        
        // Проверка корректности данных
        if price.is_nan() || price.is_infinite() || price < 0.0 {
            return Err(OrderError::InvalidPrice(
                item.product.name.clone(), 
                price
            ));
        }
        
        if quantity <= 0 {
            return Err(OrderError::InvalidQuantity(
                item.product.name.clone(), 
                quantity
            ));
        }
        
        // Проверка на переполнение
        let item_total = price * quantity as f64;
        if item_total.is_infinite() {
            return Err(OrderError::CalculationOverflow);
        }
        
        total += item_total;
    }
    
    if total < 0.0 {
        Err(OrderError::NegativeTotal)
    } else {
        Ok(total)
    }
}

// Вариант 2: Option (если не нужна информация об ошибке)
fn safe_calculate_total_option(order: &Order) -> Option<f64> {
    order.items.as_ref().and_then(|items| {
        if items.is_empty() {
            return None;
        }
        
        let mut total = 0.0;
        
        for item in items {
            let price = item.product.price;
            let quantity = item.quantity;
            
            // Проверка корректности
            if price.is_nan() || price.is_infinite() || price < 0.0 {
                return None;
            }
            
            if quantity <= 0 {
                return None;
            }
            
            let item_total = price * quantity as f64;
            if item_total.is_infinite() {
                return None;
            }
            
            total += item_total;
        }
        
        if total >= 0.0 {
            Some(total)
        } else {
            None
        }
    })
}

// Вариант 3: Использование unwrap и expect (небезопасно, но иногда удобно)
fn unsafe_calculate_total(order: &Order) -> f64 {
    let items = order.items.as_ref().expect("Order has no items!");
    
    items.iter()
        .map(|item| {
            let price = item.product.price;
            let quantity = item.quantity;
            
            // Паника при некорректных данных
            assert!(!price.is_nan() && !price.is_infinite() && price >= 0.0,
                "Invalid price for {}", item.product.name);
            assert!(quantity > 0,
                "Invalid quantity for {}", item.product.name);
            
            price * quantity as f64
        })
        .sum()
}

// Вариант 4: Обработка ошибок в цепочке с ?
fn process_order_chain(order: &Order) -> Result<(f64, f64), OrderError> {
    let total = safe_calculate_total_result(order)?;
    
    // Применяем скидку если сумма > 1000
    let discounted = if total > 1000.0 {
        total * 0.9
    } else {
        total
    };
    
    // Проверяем что итоговая сумма не отрицательная
    if discounted < 0.0 {
        return Err(OrderError::NegativeTotal);
    }
    
    Ok((total, discounted))
}

// Демонстрация разных подходов к обработке ошибок
fn demonstrate_error_handling() {
    println!("\n{}", "=".repeat(60));
    println!("ОБРАБОТКА ОШИБОК В RUST");
    println!("{}", "=".repeat(60));
    
    // Создаем тестовые данные с потенциальными ошибками
    let users = vec![
        User::new(1, "John Doe", "john@example.com"),
        User::new(2, "Jane Smith", "jane@example.com"),
    ];
    
    let products = vec![
        Product::new(1, "iPhone", 999.99, "electronics"),
        Product::new(2, "MacBook", 1999.99, "electronics"),
        Product::new(3, "Defective", f64::NAN, "electronics"), // Некорректная цена
        Product::new(4, "Free", 0.0, "clothing"),
    ];
    
    let orders = vec![
        // Корректный заказ
        Order::new(
            1, 
            users[0].clone(), 
            Some(vec![
                OrderItem::new(products[0].clone(), 1),
                OrderItem::new(products[3].clone(), 2)
            ]), 
            "completed"
        ),
        // Заказ без товаров
        Order::new(
            2, 
            users[1].clone(), 
            Some(vec![]), 
            "empty"
        ),
        // Заказ с null items
        Order::new(
            3, 
            users[0].clone(), 
            None, 
            "null"
        ),
        // Заказ с некорректной ценой
        Order::new(
            4, 
            users[1].clone(), 
            Some(vec![
                OrderItem::new(products[2].clone(), 1) // Цена NaN
            ]), 
            "error"
        ),
        // Заказ с отрицательным количеством
        Order::new(
            5, 
            users[0].clone(), 
            Some(vec![
                OrderItem::new(products[0].clone(), -1) // Отрицательное количество
            ]), 
            "error"
        ),
    ];
    
    for order in &orders {
        println!("\nЗаказ #{} (статус: {}):", order.id, order.status);
        
        // Вариант 1: Result
        match safe_calculate_total_result(order) {
            Ok(total) => println!("  Result: Успех - {:.2}", total),
            Err(err) => println!("  Result: Ошибка - {}", err),
        }
        
        // Вариант 2: Option
        match safe_calculate_total_option(order) {
            Some(total) => println!("  Option: Успех - {:.2}", total),
            None => println!("  Option: Ошибка - невозможно вычислить"),
        }
        
        // Вариант 3: Небезопасный (только для корректных заказов)
        if order.id == 1 {
            let total = unsafe_calculate_total(order);
            println!("  Unsafe: Успех - {:.2}", total);
        }
        
        // Вариант 4: Цепочка вычислений
        match process_order_chain(order) {
            Ok((original, discounted)) => 
                println!("  Chain: оригинал={:.2}, со скидкой={:.2}", original, discounted),
            Err(err) => println!("  Chain: Ошибка - {}", err),
        }
    }
}

fn main() {
    println!("=== RUST - Обработка заказов с обработкой ошибок ===");
    
    demonstrate_error_handling();
    
    println!("\n{}", "=".repeat(60));
    println!("ПРЕИМУЩЕСТВА RUST ДЛЯ ОБРАБОТКИ ОШИБОК");
    println!("{}", "=".repeat(60));
    
    println!("
    1. Result<T, E> - основной тип для обработки ошибок
    2. ? оператор - удобное распространение ошибок
    3. Option<T> - для значений, которые могут отсутствовать
    4. match - исчерпывающая проверка всех вариантов
    5. panic! и unwrap() - для невосстановимых ошибок
    6. Компилятор проверяет обработку всех возможных ошибок
    7. Нет исключений (exceptions) - только паника или Result
    8. Система владения предотвращает многие ошибки времени выполнения
    ");
    
    println!("\n{}", "=".repeat(60));
    println!("СРАВНЕНИЕ С ДРУГИМИ ЯЗЫКАМИ");
    println!("{}", "=".repeat(60));
    
    println!("
    Rust:    Result/Option, проверка при компиляции, нет исключений
    Scala:   Try/Either/Option, функциональный стиль, есть исключения
    Python:  try/except, исключения, проверка во время выполнения
    ");
}
[file content end]