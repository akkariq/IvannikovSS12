**Лабораторная работа 6. Функциональное программирование. Часть 5. Rust и системное программирование**

**Цель работы:** Изучить применение функционального программирования в Rust, освоить работу с системой владения, заимствования и временами жизни. Изучить функциональные подходы в контексте низкоуровневого и безопасного программирования.

**Задачи:**
1. Изучить базовый синтаксис Rust и систему типов
2. Освоить систему владения (ownership) и заимствования (borrowing)
3. Научиться работать с итераторами и замыканиями
4. Изучить алгебраические типы данных и pattern matching
5. Освоить обработку ошибок с помощью Result и Option

**Теоретическая часть**

**Rust как системный функциональный язык:**
Rust сочетает производительность системных языков с безопасностью и выразительностью функциональных языков. Гарантии безопасности памяти проверяются на этапе компиляции.

**Основные концепции ФП в Rust:**
*   **Иммутабельность по умолчанию** - переменные неизменяемы без ключевого слова `mut`
*   **Система владения** - гарантии безопасности памяти без сборщика мусора
*   **Трейты** - аналоги type classes из Haskell
*   **Алгебраические типы данных** - enum с данными
*   **Сопоставление с образцом** - exhaustive pattern matching

**Ключевые особенности:**
*   **Нулевая стоимость абстракций** - функциональные конструкции не добавляют runtime накладных расходов
*   **Отсутствие исключений** - обработка ошибок через Result и Option
*   **Ленивые итераторы** - эффективные цепочки преобразований

**Порядок выполнения работы**

**1. Базовый синтаксис и система владения**

Создайте файл `ownership.rs`:

```rust
// Базовые функции
fn square(x: i32) -> i32 {
    x * x
}

fn add(a: i32, b: i32) -> i32 {
    a + b
}

// Функции высшего порядка
fn apply_function<F>(f: F, x: i32) -> i32 
where 
    F: Fn(i32) -> i32,
{
    f(x)
}

// Демонстрация системы владения
fn demonstrate_ownership() {
    println!("=== Система владения ===");
    
    let s1 = String::from("hello");
    let s2 = s1; // Перемещение владения, s1 больше не валидна
    // println!("{}", s1); // Ошибка компиляции!
    println!("s2 = {}", s2);
    
    // Клонирование для глубокого копирования
    let s3 = s2.clone();
    println!("s2 = {}, s3 = {}", s2, s3);
    
    // Заимствование (borrowing)
    let len = calculate_length(&s3);
    println!("Длина '{}' = {}", s3, len);
    
    // Изменяемое заимствование
    let mut s4 = String::from("hello");
    modify_string(&mut s4);
    println!("После модификации: {}", s4);
}

fn calculate_length(s: &String) -> usize {
    s.len()
}

fn modify_string(s: &mut String) {
    s.push_str(", world!");
}

// Каррирование
fn multiply(a: i32) -> impl Fn(i32) -> i32 {
    move |b| a * b
}

fn main() {
    println!("Квадрат 5: {}", square(5));
    println!("Сложение 3 и 4: {}", add(3, 4));
    println!("Применение функции: {}", apply_function(square, 3));
    
    let double = multiply(2);
    println!("Удвоение 7: {}", double(7));
    
    demonstrate_ownership();
}
```

**2. Итераторы и замыкания**

Создайте файл `iterators_closures.rs`:

```rust
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

fn demonstrate_iterators() {
    println!("\n=== Итераторы и замыкания ===");
    
    let products = vec![
        Product::new(1, "iPhone", 999.99, "electronics", true),
        Product::new(2, "MacBook", 1999.99, "electronics", false),
        Product::new(3, "T-shirt", 29.99, "clothing", true),
        Product::new(4, "Jeans", 79.99, "clothing", true),
        Product::new(5, "Book", 15.99, "education", false),
    ];
    
    let numbers = vec![1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
    
    // Map
    let product_names: Vec<String> = products.iter().map(|p| p.name.clone()).collect();
    println!("Названия продуктов: {:?}", product_names);
    
    // Filter
    let available_products: Vec<&Product> = products.iter().filter(|p| p.in_stock).collect();
    println!("Доступные продукты: {:?}", available_products);
    
    // Fold (аналог reduce)
    let total_price: f64 = products.iter().map(|p| p.price).fold(0.0, |acc, price| acc + price);
    println!("Общая стоимость: {:.2}", total_price);
    
    // Цепочка преобразований
    let expensive_available: Vec<String> = products
        .iter()
        .filter(|p| p.in_stock && p.price > 50.0)
        .map(|p| p.name.to_uppercase())
        .collect();
    println!("Дорогие доступные: {:?}", expensive_available);
    
    // Замыкания с захватом переменных
    let min_price = 50.0;
    let filtered_products: Vec<&Product> = products
        .iter()
        .filter(|p| p.price >= min_price) // Захват min_price
        .collect();
    println!("Продукты дороже {}: {:?}", min_price, filtered_products);
    
    // Ленивые итераторы
    let squares: Vec<i32> = numbers
        .iter()
        .map(|x| {
            println!("Вычисление квадрата для {}", x);
            x * x
        })
        .take(3) // Без collect вычисления не выполняются
        .collect();
    println!("Квадраты первых 3 чисел: {:?}", squares);
}

// Функция, принимающая замыкание
fn process_products<F>(products: &[Product], predicate: F) -> Vec<&Product>
where
    F: Fn(&Product) -> bool,
{
    products.iter().filter(|p| predicate(p)).collect()
}

fn main() {
    demonstrate_iterators();
    
    let products = vec![
        Product::new(1, "iPhone", 999.99, "electronics", true),
        Product::new(2, "MacBook", 1999.99, "electronics", false),
    ];
    
    // Использование функции с замыканием
    let electronics = process_products(&products, |p| p.category == "electronics");
    println!("Электроника: {:?}", electronics);
}
```

**3. Алгебраические типы данных и pattern matching**

Создайте файл `pattern_matching.rs`:

```rust
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
    id: u32,
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
```

**4. Обработка ошибок с Result и Option**

Создайте файл `error_handling.rs`:

```rust
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

fn process_order(db: &UserDatabase, order: &Order) -> Result<(&User, &Order), String> {
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
    let user_1_email = find_user(&user_db, 1)
        .map(|user| &user.email)
        .unwrap_or(&"Unknown".to_string());
    println!("Email пользователя 1: {}", user_1_email);
    
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

fn process_order_advanced(db: &UserDatabase, order: &Order) -> Result<String, OrderError> {
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
```

**5. Функциональные структуры данных**

Создайте файл `functional_data_structures.rs`:

```rust
use std::rc::Rc;

// Функциональный список
#[derive(Debug, Clone)]
enum List<T> {
    Empty,
    Cons(T, Rc<List<T>>),
}

impl<T> List<T> {
    fn new() -> Self {
        List::Empty
    }
    
    fn prepend(&self, elem: T) -> Self {
        List::Cons(elem, Rc::new(self.clone()))
    }
    
    fn head(&self) -> Option<&T> {
        match self {
            List::Cons(head, _) => Some(head),
            List::Empty => None,
        }
    }
    
    fn tail(&self) -> Option<&List<T>> {
        match self {
            List::Cons(_, tail) => Some(tail),
            List::Empty => None,
        }
    }
    
    fn iter(&self) -> ListIter<T> {
        ListIter { current: self }
    }
}

// Итератор для функционального списка
struct ListIter<'a, T> {
    current: &'a List<T>,
}

impl<'a, T> Iterator for ListIter<'a, T> {
    type Item = &'a T;
    
    fn next(&mut self) -> Option<Self::Item> {
        match self.current {
            List::Cons(head, tail) => {
                self.current = tail;
                Some(head)
            }
            List::Empty => None,
        }
    }
}

fn demonstrate_functional_structures() {
    println!("\n=== Функциональные структуры данных ===");
    
    // Создание списка в функциональном стиле
    let list = List::new()
        .prepend(3)
        .prepend(2)
        .prepend(1);
    
    println!("Функциональный список: {:?}", list);
    
    // Итерация по списку
    println!("Элементы списка:");
    for elem in list.iter() {
        println!("- {}", elem);
    }
    
    // Голова и хвост
    if let Some(head) = list.head() {
        println!("Голова списка: {}", head);
    }
    
    if let Some(tail) = list.tail() {
        println!("Хвост списка: {:?}", tail);
    }
}

// Неизменяемая структура данных
#[derive(Debug, Clone)]
struct ImmutablePoint {
    x: f64,
    y: f64,
}

impl ImmutablePoint {
    fn new(x: f64, y: f64) -> Self {
        ImmutablePoint { x, y }
    }
    
    // Вместо мутации возвращаем новую структуру
    fn translate(&self, dx: f64, dy: f64) -> Self {
        ImmutablePoint {
            x: self.x + dx,
            y: self.y + dy,
        }
    }
    
    fn distance(&self, other: &ImmutablePoint) -> f64 {
        ((self.x - other.x).powi(2) + (self.y - other.y).powi(2)).sqrt()
    }
}

fn main() {
    demonstrate_functional_structures();
    
    // Демонстрация неизменяемой точки
    let point1 = ImmutablePoint::new(0.0, 0.0);
    let point2 = point1.translate(3.0, 4.0);
    
    println!("Расстояние между {:?} и {:?} = {:.2}", point1, point2, point1.distance(&point2));
}
```

**6. Практические задания**

**Задание 1:** Реализуйте функцию для обработки вектора продуктов

```rust
fn analyze_products(products: &[Product]) -> (f64, usize, Vec<&Product>) {
    // TODO: Вернуть кортеж: (средняя цена, количество доступных, список дорогих продуктов > 100)
}
```

**Задание 2:** Создайте функцию для валидации цепочки заказов

```rust
fn validate_orders(orders: &[Order]) -> Result<Vec<&Order>, OrderError> {
    // TODO: Проверить все заказы, вернуть только валидные или первую ошибку
}
```

**Задание 3:** Реализуйте итератор для генерации последовательности

```rust
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
        // TODO: Реализовать генерацию чисел Фибоначчи
    }
}
```

**Пример выполнения программы:**

```rust
// main.rs
mod ownership;
mod iterators_closures;
mod pattern_matching;
mod error_handling;
mod functional_data_structures;

fn main() {
    println!("=== Rust Функциональное Программирование ===\n");
    
    // Базовые операции и система владения
    ownership::main();
    
    // Итераторы и замыкания
    iterators_closures::demonstrate_iterators();
    
    // Pattern matching
    pattern_matching::demonstrate_pattern_matching();
    
    // Обработка ошибок
    error_handling::demonstrate_error_handling();
    
    // Функциональные структуры данных
    functional_data_structures::demonstrate_functional_structures();
}
```

**Cargo.toml:**

```toml
[package]
name = "rust-fp-lab"
version = "1.0.0"
edition = "2021"

[dependencies]
```

**Критерии оценки**

**Удовлетворительно:**
*   Реализованы базовые функции и работа с системой владения
*   Использованы простые итераторы и замыкания
*   Выполнены простые операции с Option и Result

**Хорошо:**
*   Корректно реализованы функции высшего порядка
*   Использованы алгебраические типы данных и pattern matching
*   Созданы цепочки итераторов с map/filter/fold
*   Выполнены основные практические задания

**Отлично:**
*   Эффективно использованы продвинутые возможности системы типов
*   Реализованы кастомные итераторы и функциональные структуры данных
*   Созданы сложные цепочки обработки ошибок
*   Код безопасен и эффективен, использует лучшие практики Rust
*   Реализованы все практические задания

**Контрольные вопросы**
1.  Как система владения Rust обеспечивает безопасность памяти?
2.  В чем разница между `&T` и `&mut T`?
3.  Как работают ленивые итераторы в Rust?
4.  Какие преимущества дают алгебраические типы данных и pattern matching?
5.  Почему Rust предпочитает Result и Option вместо исключений?

**Рекомендованная литература**
1.  "The Rust Programming Language" (The Book)
2.  "Programming Rust" by Jim Blandy and Jason Orendorff
3.  "Rust for Functional Programmers" (официальная документация)
4.  "Hands-On Functional Programming in Rust" by Andrew Johnson
5.  Официальная документация Rust: https://doc.rust-lang.org/book/