**Лабораторная работа 6. Функциональное программирование. Часть 3. JavaScript и современный фронтенд**

**Цель работы:** Изучить применение функционального программирования в JavaScript, освоить современные подходы к разработке фронтенда с использованием функциональных концепций, изучить работу с асинхронными операциями в функциональном стиле.

**Задачи:**
1. Изучить функции высшего порядка в JavaScript
2. Освоить методы работы с массивами: map, filter, reduce
3. Научиться использовать стрелочные функции и замыкания
4. Изучить иммутабельные обновления и распространение состояния
5. Освоить функциональные компоненты React и хуки

**Теоретическая часть**

**Функциональное программирование в JavaScript:**
JavaScript поддерживает функциональную парадигму и активно использует её в современных фреймворках. ES6+ добавил множество возможностей для удобной работы в функциональном стиле.

**Основные концепции:**
*   **Функции первого класса** - функции являются объектами и могут быть присвоены переменным
*   **Стрелочные функции** - компактный синтаксис для определения функций
*   **Неизменяемость (Immutability)** - создание новых объектов вместо изменения существующих
*   **Чистые функции** - функции без побочных эффектов
*   **Композиция функций** - объединение простых функций в более сложные

**Современные возможности:**
*   **Деструктуризация** - извлечение значений из объектов и массивов
*   **Spread оператор** - для создания копий объектов и массивов
*   **Модули ES6** - организация кода в отдельные модули

**Порядок выполнения работы**

**1. Функции высшего порядка и методы массивов**

Создайте файл `array-methods.js`:

```javascript
// Данные для работы
const products = [
    { id: 1, name: 'iPhone', price: 999, category: 'electronics', inStock: true },
    { id: 2, name: 'MacBook', price: 1999, category: 'electronics', inStock: false },
    { id: 3, name: 'T-shirt', price: 29, category: 'clothing', inStock: true },
    { id: 4, name: 'Jeans', price: 79, category: 'clothing', inStock: true },
    { id: 5, name: 'Book', price: 15, category: 'education', inStock: false }
];

const numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

// Map - преобразование массива
const productNames = products.map(product => product.name);
console.log('Названия продуктов:', productNames);

const discountedPrices = products.map(product => ({
    ...product,
    price: product.price * 0.9 // 10% скидка
}));
console.log('Продукты со скидкой:', discountedPrices);

// Filter - фильтрация массива
const availableProducts = products.filter(product => product.inStock);
console.log('Доступные продукты:', availableProducts);

const expensiveProducts = products.filter(product => product.price > 100);
console.log('Дорогие продукты:', expensiveProducts);

// Reduce - свертка массива
const totalPrice = products.reduce((sum, product) => sum + product.price, 0);
console.log('Общая стоимость:', totalPrice);

const productsByCategory = products.reduce((acc, product) => {
    const category = product.category;
    if (!acc[category]) {
        acc[category] = [];
    }
    acc[category].push(product);
    return acc;
}, {});
console.log('Продукты по категориям:', productsByCategory);

// Цепочка методов
const result = products
    .filter(product => product.inStock)
    .map(product => ({
        name: product.name.toUpperCase(),
        price: product.price
    }))
    .reduce((total, product) => total + product.price, 0);

console.log('Сумма доступных продуктов:', result);
```

**2. Стрелочные функции и замыкания**

Создайте файл `functions-closures.js`:

```javascript
// Стрелочные функции
const square = x => x * x;
const add = (a, b) => a + b;
const greet = name => `Hello, ${name}!`;

console.log('Square of 5:', square(5));
console.log('Add 3 and 4:', add(3, 4));
console.log(greet('John'));

// Замыкания
const createCounter = () => {
    let count = 0;
    return {
        increment: () => ++count,
        decrement: () => --count,
        getCount: () => count
    };
};

const counter = createCounter();
console.log('Counter:', counter.increment()); // 1
console.log('Counter:', counter.increment()); // 2
console.log('Counter:', counter.getCount());  // 2

// Каррирование
const multiply = a => b => a * b;
const double = multiply(2);
const triple = multiply(3);

console.log('Double 5:', double(5));   // 10
console.log('Triple 5:', triple(5));   // 15

// Функциональная композиция
const compose = (...fns) => x => fns.reduceRight((acc, fn) => fn(acc), x);
const pipe = (...fns) => x => fns.reduce((acc, fn) => fn(acc), x);

const add5 = x => x + 5;
const multiply3 = x => x * 3;
const subtract10 = x => x - 10;

const composed = compose(subtract10, multiply3, add5);
const piped = pipe(add5, multiply3, subtract10);

console.log('Composed result:', composed(5)); // (5 + 5) * 3 - 10 = 20
console.log('Piped result:', piped(5));       // (5 + 5) * 3 - 10 = 20
```

**3. Иммутабельные обновления и работа с объектами**

Создайте файл `immutability.js`:

```javascript
// Исходные данные
const user = {
    id: 1,
    name: 'John Doe',
    address: {
        city: 'New York',
        street: '123 Main St',
        coordinates: {
            lat: 40.7128,
            lng: -74.0060
        }
    },
    preferences: {
        theme: 'dark',
        notifications: true
    }
};

const cart = [
    { id: 1, name: 'Product A', quantity: 2 },
    { id: 2, name: 'Product B', quantity: 1 }
];

// Иммутабельные обновления с spread оператором
const updatedUser = {
    ...user,
    name: 'Jane Doe',
    preferences: {
        ...user.preferences,
        theme: 'light'
    }
};

console.log('Original user:', user);
console.log('Updated user:', updatedUser);

// Иммутабельное добавление в массив
const newCartItem = { id: 3, name: 'Product C', quantity: 1 };
const updatedCart = [...cart, newCartItem];
console.log('Updated cart:', updatedCart);

// Иммутабельное обновление элемента массива
const updatedCartQuantity = cart.map(item =>
    item.id === 1 ? { ...item, quantity: item.quantity + 1 } : item
);
console.log('Cart with updated quantity:', updatedCartQuantity);

// Иммутабельное удаление из массива
const filteredCart = cart.filter(item => item.id !== 2);
console.log('Cart after removal:', filteredCart);

// Глубокая иммутабельная update функция
const deepUpdate = (obj, path, value) => {
    const [key, ...rest] = path;
    
    if (rest.length === 0) {
        return { ...obj, [key]: value };
    }
    
    return {
        ...obj,
        [key]: deepUpdate(obj[key], rest, value)
    };
};

const userWithNewAddress = deepUpdate(user, ['address', 'city'], 'Boston');
console.log('User with new city:', userWithNewAddress);
```

**4. Асинхронное функциональное программирование**

Создайте файл `async-fp.js`:

```javascript
// Промисы и async/await в функциональном стиле
const fetchData = (url) => {
    return fetch(url)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        });
};

// Функциональная обработка асинхронных операций
const processUserData = async (userId) => {
    try {
        const user = await fetchData(`/api/users/${userId}`);
        const posts = await fetchData(`/api/users/${userId}/posts`);
        
        return {
            ...user,
            posts: posts.map(post => ({
                ...post,
                excerpt: post.content.substring(0, 100) + '...'
            }))
        };
    } catch (error) {
        console.error('Error processing user data:', error);
        throw error;
    }
};

// Композиция асинхронных функций
const asyncPipe = (...fns) => x => fns.reduce(async (acc, fn) => fn(await acc), x);

const validateInput = async (data) => {
    if (!data.email) throw new Error('Email is required');
    return data;
};

const sanitizeData = async (data) => ({
    ...data,
    email: data.email.toLowerCase().trim()
});

const saveToDatabase = async (data) => {
    // Симуляция сохранения в базу данных
    return new Promise(resolve => {
        setTimeout(() => {
            resolve({ ...data, id: Math.random(), createdAt: new Date() });
        }, 1000);
    });
};

const userRegistration = asyncPipe(
    validateInput,
    sanitizeData,
    saveToDatabase
);

// Демонстрация
const userData = { email: '  JOHN@EXAMPLE.COM  ', name: 'John' };
userRegistration(userData).then(result => {
    console.log('Registered user:', result);
});
```

**5. Функциональные компоненты React**

Создайте файл `react-functional.js`:

```javascript
import React, { useState, useEffect, useCallback, useMemo } from 'react';

// Функциональный компонент с хуками
const ProductList = ({ products, onProductSelect }) => {
    const [filter, setFilter] = useState('');
    const [sortOrder, setSortOrder] = useState('asc');

    // useMemo для оптимизации вычислений
    const filteredAndSortedProducts = useMemo(() => {
        const filtered = products.filter(product =>
            product.name.toLowerCase().includes(filter.toLowerCase())
        );
        
        return filtered.sort((a, b) => {
            if (sortOrder === 'asc') {
                return a.price - b.price;
            } else {
                return b.price - a.price;
            }
        });
    }, [products, filter, sortOrder]);

    // useCallback для мемоизации функций
    const handleProductSelect = useCallback((productId) => {
        onProductSelect(productId);
    }, [onProductSelect]);

    // Побочные эффекты
    useEffect(() => {
        console.log('Products updated:', filteredAndSortedProducts.length);
    }, [filteredAndSortedProducts]);

    return (
        <div>
            <input
                type="text"
                placeholder="Filter products..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
            />
            <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value)}>
                <option value="asc">Price: Low to High</option>
                <option value="desc">Price: High to Low</option>
            </select>
            
            <div>
                {filteredAndSortedProducts.map(product => (
                    <ProductItem
                        key={product.id}
                        product={product}
                        onSelect={handleProductSelect}
                    />
                ))}
            </div>
        </div>
    );
};

// Чистый функциональный компонент
const ProductItem = React.memo(({ product, onSelect }) => {
    return (
        <div 
            className="product-item"
            onClick={() => onSelect(product.id)}
            style={{ 
                border: '1px solid #ccc', 
                padding: '10px', 
                margin: '5px',
                cursor: 'pointer'
            }}
        >
            <h3>{product.name}</h3>
            <p>Price: ${product.price}</p>
            <p>Category: {product.category}</p>
            <p>{product.inStock ? 'In Stock' : 'Out of Stock'}</p>
        </div>
    );
});

// Кастомный хук
const useLocalStorage = (key, initialValue) => {
    const [value, setValue] = useState(() => {
        try {
            const item = window.localStorage.getItem(key);
            return item ? JSON.parse(item) : initialValue;
        } catch (error) {
            console.error('Error reading from localStorage:', error);
            return initialValue;
        }
    });

    const setStoredValue = useCallback((newValue) => {
        try {
            setValue(newValue);
            window.localStorage.setItem(key, JSON.stringify(newValue));
        } catch (error) {
            console.error('Error saving to localStorage:', error);
        }
    }, [key]);

    return [value, setStoredValue];
};

// Использование кастомного хука
const ShoppingCart = () => {
    const [cart, setCart] = useLocalStorage('shopping-cart', []);

    const addToCart = useCallback((product) => {
        setCart(currentCart => {
            const existingItem = currentCart.find(item => item.id === product.id);
            if (existingItem) {
                return currentCart.map(item =>
                    item.id === product.id
                        ? { ...item, quantity: item.quantity + 1 }
                        : item
                );
            } else {
                return [...currentCart, { ...product, quantity: 1 }];
            }
        });
    }, [setCart]);

    const totalItems = useMemo(() => 
        cart.reduce((sum, item) => sum + item.quantity, 0),
        [cart]
    );

    return (
        <div>
            <h2>Shopping Cart ({totalItems} items)</h2>
            {/* Реализация интерфейса корзины */}
        </div>
    );
};
```

**6. Практические задания**

**Задание 1:** Создайте функцию для обработки массива пользователей

```javascript
const processUsers = (users) => {
    // TODO: Вернуть объект с:
    // - средним возрастом пользователей
    // - количеством пользователей по городу
    // - списком email активных пользователей
};
```

**Задание 2:** Реализуйте кастомный хук для управления формой

```javascript
const useForm = (initialValues) => {
    // TODO: Реализовать хук для управления состоянием формы
    // с валидацией и обработкой submit
};
```

**Задание 3:** Создайте функцию для дебаунсинга

```javascript
const debounce = (func, delay) => {
    // TODO: Реализовать функцию дебаунсинга
};
```

**Пример выполнения программы:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>JavaScript FP Demo</title>
</head>
<body>
    <div id="app"></div>
    
    <script type="module">
        import { createCounter } from './functions-closures.js';
        import { processUsers } from './array-methods.js';
        
        // Демонстрация работы
        const counter = createCounter();
        console.log('Counter demo:');
        console.log(counter.increment());
        console.log(counter.increment());
        
        // Демонстрация обработки данных
        const users = [
            { name: 'John', age: 25, city: 'New York', active: true, email: 'john@example.com' },
            { name: 'Jane', age: 30, city: 'Boston', active: false, email: 'jane@example.com' }
        ];
        
        console.log('Processed users:', processUsers(users));
    </script>
</body>
</html>
```

**Критерии оценки**

**Удовлетворительно:**
*   Реализованы базовые операции с методами массивов
*   Использованы стрелочные функции и простые замыкания
*   Созданы простые иммутабельные обновления

**Хорошо:**
*   Корректно реализованы функции высшего порядка
*   Использованы spread оператор для иммутабельных обновлений
*   Созданы функциональные компоненты React с хуками
*   Выполнены основные практические задания

**Отлично:**
*   Эффективно использованы композиция функций и каррирование
*   Реализованы сложные асинхронные операции в функциональном стиле
*   Созданы оптимизированные React компоненты с useMemo и useCallback
*   Реализованы кастомные хуки и утилиты
*   Код хорошо структурирован и соответствует best practices

**Контрольные вопросы**
1.  Какие методы массивов в JavaScript относятся к функциям высшего порядка?
2.  Как работают замыкания и для чего они используются в React?
3.  Что такое иммутабельность и почему она важна в React?
4.  Как useMemo и useCallback помогают оптимизировать производительность?
5.  Какие преимущества дают функциональные компоненты перед классовыми?

**Рекомендованная литература**
1.  "JavaScript: The Good Parts" Douglas Crockford
2.  "Functional-Light JavaScript" Kyle Simpson
3.  "React Hooks in Action" John Larsen
4.  Официальная документация React: Hooks API Reference
5.  MDN Web Docs: Array methods, Functions