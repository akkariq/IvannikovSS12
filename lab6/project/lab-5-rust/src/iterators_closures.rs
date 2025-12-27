#[derive(Debug, Clone)]
struct Product {
    #[allow(dead_code)]
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