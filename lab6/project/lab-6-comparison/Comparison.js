[file name]: Comparison.js
[file content begin]
// Модель данных
class User {
    constructor(id, name, email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }
}

class Product {
    constructor(id, name, price, category) {
        this.id = id;
        this.name = name;
        this.price = price;
        this.category = category;
    }
}

class OrderItem {
    constructor(product, quantity) {
        this.product = product;
        this.quantity = quantity;
    }
}

class Order {
    constructor(id, user, items, status) {
        this.id = id;
        this.user = user;
        this.items = items;
        this.status = status;
    }
}

// Пример данных с потенциальными ошибками
const users = [
    new User(1, "John Doe", "john@example.com"),
    new User(2, "Jane Smith", "jane@example.com")
];

const products = [
    new Product(1, "iPhone", 999.99, "electronics"),
    new Product(2, "MacBook", 1999.99, "electronics"),
    new Product(3, "T-shirt", 29.99, "clothing"),
    new Product(4, "Defective", NaN, "electronics"), // Некорректная цена
    new Product(5, "Free", 0.0, "clothing"),
    new Product(6, "Invalid", "not a number", "electronics") // Не число
];

const orders = [
    // Корректный заказ
    new Order(1, users[0], [
        new OrderItem(products[0], 1),
        new OrderItem(products[2], 2)
    ], "completed"),
    // Заказ без товаров
    new Order(2, users[1], [], "empty"),
    // Заказ с null items
    new Order(3, users[0], null, "null"),
    // Заказ с undefined items
    new Order(4, users[1], undefined, "undefined"),
    // Заказ с некорректной ценой
    new Order(5, users[0], [
        new OrderItem(products[3], 1) // Цена NaN
    ], "error"),
    // Заказ с нечисловой ценой
    new Order(6, users[1], [
        new OrderItem(products[5], 1) // Цена - строка
    ], "error"),
    // Заказ с отрицательным количеством
    new Order(7, users[0], [
        new OrderItem(products[0], -1)
    ], "error"),
    // Заказ с нулевым количеством
    new Order(8, users[1], [
        new OrderItem(products[0], 0)
    ], "error"),
];

// Задание 3: Обработка ошибок в JavaScript
// Вариант 1: try-catch (традиционный подход)
function safeCalculateTotalTryCatch(order) {
    try {
        if (!order.items) {
            throw new Error(`Order ${order.id}: items is ${order.items}`);
        }
        
        if (!Array.isArray(order.items)) {
            throw new Error(`Order ${order.id}: items is not an array`);
        }
        
        if (order.items.length === 0) {
            throw new Error(`Order ${order.id}: items array is empty`);
        }
        
        let total = 0;
        
        for (const item of order.items) {
            if (!item.product || typeof item.product.price !== 'number') {
                throw new Error(`Order ${order.id}: invalid product price`);
            }
            
            if (typeof item.quantity !== 'number') {
                throw new Error(`Order ${order.id}: invalid quantity type`);
            }
            
            if (isNaN(item.product.price)) {
                throw new Error(`Order ${order.id}: price is NaN for product ${item.product.name}`);
            }
            
            if (!isFinite(item.product.price)) {
                throw new Error(`Order ${order.id}: price is infinite for product ${item.product.name}`);
            }
            
            if (item.quantity <= 0) {
                throw new Error(`Order ${order.id}: invalid quantity ${item.quantity} for product ${item.product.name}`);
            }
            
            const itemTotal = item.product.price * item.quantity;
            
            if (!isFinite(itemTotal)) {
                throw new Error(`Order ${order.id}: calculation overflow for product ${item.product.name}`);
            }
            
            total += itemTotal;
        }
        
        if (total < 0) {
            throw new Error(`Order ${order.id}: negative total ${total}`);
        }
        
        return { success: true, data: total, error: null };
        
    } catch (error) {
        return { success: false, data: null, error: error.message };
    }
}

// Вариант 2: Возврат null/undefined (не рекомендуется)
function safeCalculateTotalNullable(order) {
    if (!order.items || !Array.isArray(order.items) || order.items.length === 0) {
        return null;
    }
    
    let total = 0;
    
    for (const item of order.items) {
        if (!item || !item.product || 
            typeof item.product.price !== 'number' ||
            typeof item.quantity !== 'number' ||
            isNaN(item.product.price) ||
            !isFinite(item.product.price) ||
            item.quantity <= 0) {
            return null;
        }
        
        const itemTotal = item.product.price * item.quantity;
        
        if (!isFinite(itemTotal)) {
            return null;
        }
        
        total += itemTotal;
    }
    
    return total >= 0 ? total : null;
}

// Вариант 3: Promise-based подход (асинхронный)
function safeCalculateTotalPromise(order) {
    return new Promise((resolve, reject) => {
        if (!order.items) {
            reject(new Error(`Order ${order.id}: items is ${order.items}`));
            return;
        }
        
        if (!Array.isArray(order.items)) {
            reject(new Error(`Order ${order.id}: items is not an array`));
            return;
        }
        
        if (order.items.length === 0) {
            reject(new Error(`Order ${order.id}: items array is empty`));
            return;
        }
        
        let total = 0;
        
        for (const item of order.items) {
            if (!item.product || typeof item.product.price !== 'number') {
                reject(new Error(`Order ${order.id}: invalid product price`));
                return;
            }
            
            if (typeof item.quantity !== 'number') {
                reject(new Error(`Order ${order.id}: invalid quantity type`));
                return;
            }
            
            if (isNaN(item.product.price)) {
                reject(new Error(`Order ${order.id}: price is NaN for product ${item.product.name}`));
                return;
            }
            
            if (!isFinite(item.product.price)) {
                reject(new Error(`Order ${order.id}: price is infinite for product ${item.product.name}`));
                return;
            }
            
            if (item.quantity <= 0) {
                reject(new Error(`Order ${order.id}: invalid quantity ${item.quantity} for product ${item.product.name}`));
                return;
            }
            
            const itemTotal = item.product.price * item.quantity;
            
            if (!isFinite(itemTotal)) {
                reject(new Error(`Order ${order.id}: calculation overflow for product ${item.product.name}`));
                return;
            }
            
            total += itemTotal;
        }
        
        if (total < 0) {
            reject(new Error(`Order ${order.id}: negative total ${total}`));
            return;
        }
        
        resolve(total);
    });
}

// Вариант 4: Функциональный подход с объектом результата
function safeCalculateTotalFunctional(order) {
    if (!order.items) {
        return { type: 'error', message: `Order ${order.id}: items is ${order.items}` };
    }
    
    if (!Array.isArray(order.items)) {
        return { type: 'error', message: `Order ${order.id}: items is not an array` };
    }
    
    if (order.items.length === 0) {
        return { type: 'error', message: `Order ${order.id}: items array is empty` };
    }
    
    let total = 0;
    
    for (const item of order.items) {
        if (!item.product || typeof item.product.price !== 'number') {
            return { type: 'error', message: `Order ${order.id}: invalid product price` };
        }
        
        if (typeof item.quantity !== 'number') {
            return { type: 'error', message: `Order ${order.id}: invalid quantity type` };
        }
        
        if (isNaN(item.product.price)) {
            return { type: 'error', message: `Order ${order.id}: price is NaN for product ${item.product.name}` };
        }
        
        if (!isFinite(item.product.price)) {
            return { type: 'error', message: `Order ${order.id}: price is infinite for product ${item.product.name}` };
        }
        
        if (item.quantity <= 0) {
            return { type: 'error', message: `Order ${order.id}: invalid quantity ${item.quantity} for product ${item.product.name}` };
        }
        
        const itemTotal = item.product.price * item.quantity;
        
        if (!isFinite(itemTotal)) {
            return { type: 'error', message: `Order ${order.id}: calculation overflow for product ${item.product.name}` };
        }
        
        total += itemTotal;
    }
    
    if (total < 0) {
        return { type: 'error', message: `Order ${order.id}: negative total ${total}` };
    }
    
    return { type: 'success', value: total };
}

// Демонстрация обработки ошибок
async function demonstrateErrorHandling() {
    console.log("\n" + "=".repeat(60));
    console.log("ОБРАБОТКА ОШИБОК В JAVASCRIPT");
    console.log("=".repeat(60));
    
    for (const order of orders) {
        console.log(`\nЗаказ #${order.id} (статус: ${order.status}):`);
        
        // Вариант 1: try-catch
        const result1 = safeCalculateTotalTryCatch(order);
        if (result1.success) {
            console.log(`  Try-Catch: Успех - ${result1.data}`);
        } else {
            console.log(`  Try-Catch: Ошибка - ${result1.error}`);
        }
        
        // Вариант 2: null/undefined
        const result2 = safeCalculateTotalNullable(order);
        if (result2 !== null) {
            console.log(`  Nullable: Успех - ${result2}`);
        } else {
            console.log(`  Nullable: Ошибка - невозможно вычислить`);
        }
        
        // Вариант 3: Promise
        try {
            const result3 = await safeCalculateTotalPromise(order);
            console.log(`  Promise: Успех - ${result3}`);
        } catch (error) {
            console.log(`  Promise: Ошибка - ${error.message}`);
        }
        
        // Вариант 4: Функциональный
        const result4 = safeCalculateTotalFunctional(order);
        if (result4.type === 'success') {
            console.log(`  Functional: Успех - ${result4.value}`);
        } else {
            console.log(`  Functional: Ошибка - ${result4.message}`);
        }
    }
}

// Пример цепочки вычислений с обработкой ошибок
async function processOrderChain(order) {
    try {
        const total = await safeCalculateTotalPromise(order);
        const discounted = total > 1000 ? total * 0.9 : total;
        
        if (discounted < 0) {
            throw new Error(`Order ${order.id}: negative discounted total ${discounted}`);
        }
        
        return { original: total, discounted };
    } catch (error) {
        return { error: error.message };
    }
}

// Основная функция
async function main() {
    console.log("=== JAVASCRIPT - Обработка заказов с обработкой ошибок ===");
    
    await demonstrateErrorHandling();
    
    console.log("\n" + "=".repeat(60));
    console.log("ПРЕИМУЩЕСТВА JAVASCRIPT ДЛЯ ОБРАБОТКИ ОШИБОК");
    console.log("=".repeat(60));
    
    console.log(`
    1. try-catch - традиционная обработка исключений
    2. Promises - асинхронная обработка ошибок с .catch()
    3. async/await - синхронный стиль для асинхронного кода
    4. throw - генерация исключений
    5. finally - выполнение кода независимо от результата
    6. Object-based - возврат объектов {success, data, error}
    `);
    
    console.log("\n" + "=".repeat(60));
    console.log("ПРОБЛЕМЫ JAVASCRIPT С ОБРАБОТКОЙ ОШИБОК");
    console.log("=".repeat(60));
    
    console.log(`
    1. Динамическая типизация - ошибки обнаруживаются только при выполнении
    2. Нет проверок при компиляции
    3. Легко пропустить обработку ошибок
    4. Исключения могут "просачиваться" через несколько уровней
    5. Нет гарантии обработки всех возможных ошибок
    6. Много кода для проверки типов и корректности данных
    `);
    
    // Пример цепочки вычислений
    console.log("\n" + "=".repeat(60));
    console.log("ОБРАБОТКА ЦЕПОЧКИ ВЫЧИСЛЕНИЙ");
    console.log("=".repeat(60));
    
    for (const order of orders.slice(0, 2)) {
        const result = await processOrderChain(order);
        if (result.error) {
            console.log(`Заказ #${order.id}: ошибка - ${result.error}`);
        } else {
            console.log(`Заказ #${order.id}: оригинал=${result.original}, со скидкой=${result.discounted}`);
        }
    }
}

// Запуск
main().catch(console.error);
[file content end]