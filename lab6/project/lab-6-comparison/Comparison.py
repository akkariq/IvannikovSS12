[file name]: comparison_errors.py
[file content begin]
from dataclasses import dataclass
from typing import List, Optional, Union, Any, Tuple
from enum import Enum
import math

@dataclass
class User:
    id: int
    name: str
    email: str

@dataclass
class Product:
    id: int
    name: str
    price: float
    category: str

@dataclass
class OrderItem:
    product: Product
    quantity: int

@dataclass
class Order:
    id: int
    user: User
    items: Optional[List[OrderItem]]
    status: str

# Классы ошибок
class OrderError(Enum):
    NO_ITEMS = "Заказ не содержит товаров"
    NULL_ITEMS = "Список товаров равен None"
    INVALID_PRICE = "Некорректная цена товара"
    INVALID_QUANTITY = "Некорректное количество товара"
    CALCULATION_ERROR = "Ошибка при расчете"
    NEGATIVE_TOTAL = "Отрицательная итоговая сумма"

class CalculationException(Exception):
    """Пользовательское исключение для ошибок расчета"""
    def __init__(self, order_id: int, error_type: OrderError, details: str = ""):
        self.order_id = order_id
        self.error_type = error_type
        self.details = details
        super().__init__(f"Order {order_id}: {error_type.value}. {details}")

# Пример данных с потенциальными ошибками
users = [
    User(1, "John Doe", "john@example.com"),
    User(2, "Jane Smith", "jane@example.com")
]

products = [
    Product(1, "iPhone", 999.99, "electronics"),
    Product(2, "MacBook", 1999.99, "electronics"),
    Product(3, "T-shirt", 29.99, "clothing"),
    Product(4, "Defective", float('nan'), "electronics"),  # Некорректная цена
    Product(5, "Infinite", float('inf'), "electronics"),   # Бесконечная цена
    Product(6, "Free", 0.0, "clothing"),
    Product(7, "Negative", -10.0, "electronics"),         # Отрицательная цена
]

orders = [
    # Корректный заказ
    Order(1, users[0], [
        OrderItem(products[0], 1),
        OrderItem(products[2], 2)
    ], "completed"),
    # Заказ без товаров
    Order(2, users[1], [], "empty"),
    # Заказ с None items
    Order(3, users[0], None, "null"),
    # Заказ с некорректной ценой (NaN)
    Order(4, users[1], [
        OrderItem(products[3], 1)
    ], "error"),
    # Заказ с бесконечной ценой
    Order(5, users[0], [
        OrderItem(products[4], 1)
    ], "error"),
    # Заказ с отрицательной ценой
    Order(6, users[1], [
        OrderItem(products[6], 1)
    ], "error"),
    # Заказ с отрицательным количеством
    Order(7, users[0], [
        OrderItem(products[0], -1)
    ], "error"),
    # Заказ с нулевым количеством
    Order(8, users[1], [
        OrderItem(products[0], 0)
    ], "error"),
]

# Задание 3: Обработка ошибок в Python
# Вариант 1: try-except (традиционный подход)
def safe_calculate_total_try_except(order: Order) -> Tuple[bool, Union[float, str]]:
    """Возвращает кортеж (успех, результат/ошибка)"""
    try:
        if order.items is None:
            raise CalculationException(
                order.id, 
                OrderError.NULL_ITEMS,
                "Список товаров равен None"
            )
        
        if not order.items:
            raise CalculationException(
                order.id,
                OrderError.NO_ITEMS,
                "Список товаров пуст"
            )
        
        total = 0.0
        
        for item in order.items:
            price = item.product.price
            quantity = item.quantity
            
            # Проверка корректности цены
            if math.isnan(price):
                raise CalculationException(
                    order.id,
                    OrderError.INVALID_PRICE,
                    f"Цена NaN для товара {item.product.name}"
                )
            
            if math.isinf(price):
                raise CalculationException(
                    order.id,
                    OrderError.INVALID_PRICE,
                    f"Цена infinite для товара {item.product.name}"
                )
            
            if price < 0:
                raise CalculationException(
                    order.id,
                    OrderError.INVALID_PRICE,
                    f"Отрицательная цена {price} для товара {item.product.name}"
                )
            
            # Проверка корректности количества
            if quantity <= 0:
                raise CalculationException(
                    order.id,
                    OrderError.INVALID_QUANTITY,
                    f"Некорректное количество {quantity} для товара {item.product.name}"
                )
            
            item_total = price * quantity
            
            # Проверка на переполнение
            if math.isinf(item_total):
                raise CalculationException(
                    order.id,
                    OrderError.CALCULATION_ERROR,
                    f"Переполнение при расчете для товара {item.product.name}"
                )
            
            total += item_total
        
        if total < 0:
            raise CalculationException(
                order.id,
                OrderError.NEGATIVE_TOTAL,
                f"Отрицательная итоговая сумма {total}"
            )
        
        return True, total
        
    except CalculationException as e:
        return False, str(e)
    except Exception as e:
        return False, f"Неожиданная ошибка: {str(e)}"

# Вариант 2: Возврат None/значение
def safe_calculate_total_none(order: Order) -> Optional[float]:
    """Возвращает None в случае ошибки"""
    try:
        if order.items is None or not order.items:
            return None
        
        total = 0.0
        
        for item in order.items:
            price = item.product.price
            quantity = item.quantity
            
            if (math.isnan(price) or math.isinf(price) or 
                price < 0 or quantity <= 0):
                return None
            
            item_total = price * quantity
            
            if math.isinf(item_total):
                return None
            
            total += item_total
        
        return total if total >= 0 else None
        
    except Exception:
        return None

# Вариант 3: Функциональный подход с Either-подобным результатом
from typing import NamedTuple

class CalculationResult(NamedTuple):
    success: bool
    value: Optional[float] = None
    error: Optional[str] = None

def safe_calculate_total_functional(order: Order) -> CalculationResult:
    """Функциональный подход с явным возвратом результата"""
    if order.items is None:
        return CalculationResult(
            success=False,
            error=f"Order {order.id}: Список товаров равен None"
        )
    
    if not order.items:
        return CalculationResult(
            success=False,
            error=f"Order {order.id}: Список товаров пуст"
        )
    
    total = 0.0
    
    for item in order.items:
        price = item.product.price
        quantity = item.quantity
        
        # Проверка цены
        if math.isnan(price):
            return CalculationResult(
                success=False,
                error=f"Order {order.id}: Цена NaN для товара {item.product.name}"
            )
        
        if math.isinf(price):
            return CalculationResult(
                success=False,
                error=f"Order {order.id}: Цена infinite для товара {item.product.name}"
            )
        
        if price < 0:
            return CalculationResult(
                success=False,
                error=f"Order {order.id}: Отрицательная цена {price} для товара {item.product.name}"
            )
        
        # Проверка количества
        if quantity <= 0:
            return CalculationResult(
                success=False,
                error=f"Order {order.id}: Некорректное количество {quantity} для товара {item.product.name}"
            )
        
        item_total = price * quantity
        
        if math.isinf(item_total):
            return CalculationResult(
                success=False,
                error=f"Order {order.id}: Переполнение при расчете для товара {item.product.name}"
            )
        
        total += item_total
    
    if total < 0:
        return CalculationResult(
            success=False,
            error=f"Order {order.id}: Отрицательная итоговая сумма {total}"
        )
    
    return CalculationResult(success=True, value=total)

# Вариант 4: Использование контекстного менеджера
from contextlib import contextmanager

@contextmanager
def calculate_order_context(order: Order):
    """Контекстный менеджер для расчета заказа"""
    try:
        if order.items is None:
            raise CalculationException(order.id, OrderError.NULL_ITEMS)
        
        if not order.items:
            raise CalculationException(order.id, OrderError.NO_ITEMS)
        
        total = 0.0
        
        for item in order.items:
            price = item.product.price
            quantity = item.quantity
            
            if math.isnan(price) or math.isinf(price) or price < 0:
                raise CalculationException(
                    order.id, 
                    OrderError.INVALID_PRICE,
                    f"Цена {price} для {item.product.name}"
                )
            
            if quantity <= 0:
                raise CalculationException(
                    order.id,
                    OrderError.INVALID_QUANTITY,
                    f"Количество {quantity} для {item.product.name}"
                )
            
            item_total = price * quantity
            
            if math.isinf(item_total):
                raise CalculationException(
                    order.id,
                    OrderError.CALCULATION_ERROR,
                    f"Переполнение для {item.product.name}"
                )
            
            total += item_total
        
        if total < 0:
            raise CalculationException(order.id, OrderError.NEGATIVE_TOTAL)
        
        yield total
        
    except CalculationException as e:
        yield None, str(e)
    except Exception as e:
        yield None, f"Неожиданная ошибка: {str(e)}"

# Демонстрация обработки ошибок
def demonstrate_error_handling():
    print("\n" + "="*60)
    print("ОБРАБОТКА ОШИБОК В PYTHON")
    print("="*60)
    
    for order in orders:
        print(f"\nЗаказ #{order.id} (статус: {order.status}):")
        
        # Вариант 1: try-except
        success, result = safe_calculate_total_try_except(order)
        if success:
            print(f"  Try-Except: Успех - {result}")
        else:
            print(f"  Try-Except: Ошибка - {result}")
        
        # Вариант 2: None
        result = safe_calculate_total_none(order)
        if result is not None:
            print(f"  None-based: Успех - {result}")
        else:
            print(f"  None-based: Ошибка - невозможно вычислить")
        
        # Вариант 3: Функциональный
        calc_result = safe_calculate_total_functional(order)
        if calc_result.success:
            print(f"  Functional: Успех - {calc_result.value}")
        else:
            print(f"  Functional: Ошибка - {calc_result.error}")
        
        # Вариант 4: Контекстный менеджер
        with calculate_order_context(order) as context_result:
            if isinstance(context_result, tuple) and len(context_result) == 2:
                # Ошибка
                print(f"  Context: Ошибка - {context_result[1]}")
            else:
                # Успех
                print(f"  Context: Успех - {context_result}")

# Пример цепочки вычислений
def process_order_chain(order: Order) -> CalculationResult:
    """Обработка цепочки вычислений с учетом ошибок"""
    calc_result = safe_calculate_total_functional(order)
    
    if not calc_result.success:
        return calc_result
    
    total = calc_result.value
    discounted = total * 0.9 if total > 1000 else total
    
    if discounted < 0:
        return CalculationResult(
            success=False,
            error=f"Order {order.id}: Отрицательная сумма со скидкой {discounted}"
        )
    
    return CalculationResult(
        success=True,
        value=(total, discounted)
    )

def main():
    print("=== PYTHON - Обработка заказов с обработкой ошибок ===")
    
    demonstrate_error_handling()
    
    print("\n" + "="*60)
    print("ПРЕИМУЩЕСТВА PYTHON ДЛЯ ОБРАБОТКИ ОШИБОК")
    print("="*60)
    
    print("""
    1. try/except/finally - традиционная обработка исключений
    2. Пользовательские исключения - наследование от Exception
    3. Контекстные менеджеры - with statement
    4. Множественные except блоки - обработка разных типов ошибок
    5. else в try/except - выполнение если нет исключений
    6. Возврат кортежей (success, result) - функциональный стиль
    7. Optional типы - явное указание на возможное отсутствие значения
    """)
    
    print("\n" + "="*60)
    print("ОБРАБОТКА ЦЕПОЧКИ ВЫЧИСЛЕНИЙ")
    print("="*60)
    
    for order in orders[:2]:  # Только корректные заказы
        result = process_order_chain(order)
        if result.success:
            original, discounted = result.value
            print(f"Заказ #{order.id}: оригинал={original}, со скидкой={discounted}")
        else:
            print(f"Заказ #{order.id}: ошибка - {result.error}")
    
    print("\n" + "="*60)
    print("СРАВНЕНИЕ С ДРУГИМИ ЯЗЫКАМИ")
    print("="*60)
    
    print("""
    Python:      try/except, проверка во время выполнения, гибкость
    JavaScript:  try/catch, асинхронные ошибки через Promises
    Scala:       Try/Either/Option, функциональный стиль, проверка при компиляции
    Rust:        Result/Option, нет исключений, проверка при компиляции
    Haskell:     Either/Maybe, чисто функциональный, проверка при компиляции
    """)

if __name__ == "__main__":
    main()
[file content end]