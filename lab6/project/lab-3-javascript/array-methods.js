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