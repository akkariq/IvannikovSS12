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