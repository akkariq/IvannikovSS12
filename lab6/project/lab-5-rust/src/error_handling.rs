use std::collections::HashMap;

#[derive(Debug, Clone)]
struct User {
    id: u32,
    name: String,
    email: String,
}

#[derive(Debug)]
struct Order {
    user_id: u32,
    amount: f64,
    status: String,
}

impl User {
    fn new(id: u32, name: &str, email: &str) -> Self {
        User {
            id,
            name: name.to_string(),
            email: email.to_string(),
        }
    }
}

type UserDatabase = HashMap<u32, User>;

fn find_user(db: &UserDatabase, id: u32) -> Option<&User> {
    db.get(&id)
}

fn validate_user(user: &User) -> Result<&User, String> {
    if user.email.contains('@') {
        Ok(user)
    } else {
        Err(format!("Invalid email for user {}", user.name))
    }
}

// Добавляем явное указание времен жизни
fn process_order<'a>(db: &'a UserDatabase, order: &'a Order) -> Result<(&'a User, &'a Order), String> {
    let user = find_user(db, order.user_id)
        .ok_or_else(|| format!("User {} not found", order.user_id))?;
    
    let validated_user = validate_user(user)?;
    
    Ok((validated_user, order))
}

fn demonstrate_error_handling() {
    println!("\n=== Обработка ошибок ===");
    
    let mut user_db = UserDatabase::new();
    user_db.insert(1, User::new(1, "John Doe", "john@example.com"));
    user_db.insert(2, User::new(2, "Jane Smith", "jane@example.com"));
    user_db.insert(3, User::new(3, "Invalid User", "invalid-email")); // Невалидный email
    
    let orders = vec![
        Order { user_id: 1, amount: 99.99, status: "completed".to_string() },
        Order { user_id: 2, amount: 149.99, status: "pending".to_string() },
        Order { user_id: 4, amount: 199.99, status: "shipped".to_string() }, // Несуществующий пользователь
        Order { user_id: 3, amount: 79.99, status: "processing".to_string() }, // Пользователь с невалидным email
    ];
    
    // Обработка заказов с обработкой ошибок
    for order in &orders {
        match process_order(&user_db, order) {
            Ok((user, order)) => {
                println!("✅ Успешно обработан заказ для {}: ${}", user.name, order.amount);
            }
            Err(error) => {
                println!("❌ Ошибка обработки заказа: {}", error);
            }
        }
    }
    
    // Комбинаторы Option и Result
    // Решение 1: Создаем переменную с достаточным временем жизни
    let unknown_email = "Unknown".to_string();
    let user_1_email = find_user(&user_db, 1)
        .map(|user| &user.email)
        .unwrap_or(&unknown_email);
    println!("Email пользователя 1: {}", user_1_email);
    
    // Решение 2: Используем статическую строку
    let user_2_email = find_user(&user_db, 2)
        .map(|user| user.email.as_str())
        .unwrap_or("Unknown");
    println!("Email пользователя 2: {}", user_2_email);
    
    // Решение 3: Используем owned String вместо ссылки
    let user_3_email = find_user(&user_db, 3)
        .map(|user| user.email.clone())
        .unwrap_or_else(|| "Unknown".to_string());
    println!("Email пользователя 3: {}", user_3_email);
    
    // and_then для цепочки операций
    let result = find_user(&user_db, 1)
        .and_then(|user| validate_user(user).ok())
        .map(|user| user.name.clone());
    println!("Результат цепочки: {:?}", result);
}

// Кастомный тип ошибки
#[derive(Debug)]
enum OrderError {
    UserNotFound(u32),
    InvalidUser(String),
    PaymentFailed(String),
}

impl std::fmt::Display for OrderError {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        match self {
            OrderError::UserNotFound(id) => write!(f, "User {} not found", id),
            OrderError::InvalidUser(msg) => write!(f, "Invalid user: {}", msg),
            OrderError::PaymentFailed(msg) => write!(f, "Payment failed: {}", msg),
        }
    }
}

// Для этой функции тоже нужно указать время жизни
fn process_order_advanced<'a>(db: &'a UserDatabase, order: &'a Order) -> Result<String, OrderError> {
    let user = find_user(db, order.user_id)
        .ok_or(OrderError::UserNotFound(order.user_id))?;
    
    validate_user(user)
        .map_err(|e| OrderError::InvalidUser(e))?;
    
    // Симуляция проверки платежа
    if order.amount > 1000.0 {
        return Err(OrderError::PaymentFailed("Amount too large".to_string()));
    }
    
    Ok(format!("Order processed for {}", user.name))
}

fn main() {
    demonstrate_error_handling();
    
    // Демонстрация расширенной обработки ошибок
    let mut user_db = UserDatabase::new();
    user_db.insert(1, User::new(1, "John Doe", "john@example.com"));
    
    let large_order = Order { user_id: 1, amount: 1500.0, status: "pending".to_string() };
    
    match process_order_advanced(&user_db, &large_order) {
        Ok(success) => println!("{}", success),
        Err(error) => println!("Расширенная ошибка: {}", error),
    }
}